"""Pinned SKY130HD inputs and structural checks for experimental ASIC mapping."""
import hashlib
import json
from pathlib import Path
import re
import urllib.request

from prepare_standalone import ROOT, digest


LOCK = ROOT / 'tools/asic_cells.lock.json'
CACHE = ROOT / '.cache/sky130hd'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_bytes(data, record):
    require(len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256'],
            'ASIC upstream size/SHA256 mismatch: ' + record['path'])
    blob = b'blob ' + str(len(data)).encode() + b'\0' + data
    require(hashlib.sha1(blob).hexdigest() == record['git_blob_sha1'],
            'ASIC upstream Git blob mismatch: ' + record['path'])


def inputs():
    lock = json.loads(LOCK.read_text())
    require(lock['schema_version'] == 1 and lock['platform'] == 'sky130hd', 'unknown ASIC lock format')
    CACHE.mkdir(parents=True, exist_ok=True)
    result = {}
    for key, record in lock['files'].items():
        path = CACHE / record['cache_name']
        require(path.parent == CACHE and re.fullmatch('[0-9a-f]{40}', record['revision']),
                'unsafe ASIC cache name or unpinned revision')
        if not path.exists():
            url = 'https://raw.githubusercontent.com/' + '/'.join(
                [record['repository'], record['revision'], record['path']])
            with urllib.request.urlopen(url, timeout=60) as response:
                data = response.read(record['bytes'] + 1)
            verify_bytes(data, record)
            temporary = path.with_name(path.name + '.download')
            temporary.write_bytes(data)
            temporary.replace(path)
        verify_bytes(path.read_bytes(), record)
        result[key] = path
    return result


def cell_blocks(text):
    """Find balanced cell groups in the pinned, quoted-name Liberty format."""
    spans = []
    for match in re.finditer(r'^[ \t]*cell\s*\(\s*"([A-Za-z0-9_]+)"\s*\)\s*\{', text, re.M):
        depth, cursor = 0, match.end() - 1
        while cursor < len(text):
            if text.startswith('/*', cursor):
                end = text.find('*/', cursor + 2)
                require(end >= 0, 'unterminated Liberty comment')
                cursor = end + 2
                continue
            if text.startswith('//', cursor):
                cursor = text.find('\n', cursor + 2)
                require(cursor >= 0, 'unterminated Liberty cell before line comment')
                continue
            if text[cursor] == '"':
                cursor += 1
                while cursor < len(text):
                    if text[cursor] == '\\':
                        cursor += 2
                        continue
                    if text[cursor] == '"':
                        cursor += 1
                        break
                    cursor += 1
                else:
                    raise ValueError('unterminated Liberty string')
                continue
            if text[cursor] == '{':
                depth += 1
            elif text[cursor] == '}':
                depth -= 1
                if depth == 0:
                    spans.append((match.start(), cursor + 1, match.group(1)))
                    break
            cursor += 1
        else:
            raise ValueError('unterminated Liberty cell')
    require(len({name for _, _, name in spans}) == len(spans), 'duplicate Liberty cell')
    require(all(a[1] <= b[0] for a, b in zip(spans, spans[1:])), 'overlapping Liberty cells')
    return spans


def without_cells(text, spans, removed):
    parts, cursor = [], 0
    for start, end, name in spans:
        if name in removed:
            parts.append(text[cursor:start])
            cursor = end
    return ''.join(parts) + text[cursor:]


def filter_library(paths, directory):
    text = paths['library'].read_bytes().decode('utf-8')
    config = paths['platform_policy'].read_text()
    require(config.count('export DONT_USE_CELLS +=') == 1, 'ambiguous platform exclusion list')
    policy = config.split('export DONT_USE_CELLS +=', 1)[1].split('\n#', 1)[0]
    forbidden = set(re.findall(r'sky130_fd_sc_hd__[A-Za-z0-9_]+', policy))
    remainder = re.sub(r'sky130_fd_sc_hd__[A-Za-z0-9_]+', '', policy)
    require(not remainder.replace('\\', '').strip(), 'unsupported platform exclusion syntax')
    spans = cell_blocks(text)
    blocks = {name: text[start:end] for start, end, name in spans}
    require(len(blocks) == 428 and len(forbidden) == 36 and forbidden <= set(blocks),
            'pinned library/policy cell inventory changed')
    filtered = without_cells(text, spans, forbidden)
    retained = cell_blocks(filtered)
    retained_blocks = {name: filtered[start:end] for start, end, name in retained}
    require(retained_blocks == {name: block for name, block in blocks.items() if name not in forbidden},
            'filter changed a retained Liberty cell')
    require(without_cells(text, spans, set(blocks)) == without_cells(filtered, retained, set(retained_blocks)),
            'filter changed non-cell library data')
    directory.mkdir(parents=True, exist_ok=True)
    library = directory / 'cells.lib'
    library.write_bytes(filtered.encode('utf-8'))
    report = {'policy': 'Remove exactly the pinned platform DONT_USE_CELLS; preserve every other byte.',
              'original_sha256': digest(paths['library']), 'filtered_sha256': digest(library),
              'original_cell_count': len(blocks), 'retained_cell_count': len(retained_blocks),
              'excluded_cells': sorted(forbidden),
              'original_cell_block_sha256': {name: hashlib.sha256(block.encode()).hexdigest()
                                            for name, block in blocks.items()}}
    (directory / 'filter.json').write_text(json.dumps(report, indent=2) + '\n')
    return library, report


def connectivity(module):
    """Canonical pin incidence, independent of JSON bit numbers and wire aliases."""
    nets = {}
    for name, port in module['ports'].items():
        for index, bit in enumerate(port['bits']):
            require(type(bit) is int, 'ASIC port has an unmapped constant or unknown bit')
            nets.setdefault(bit, []).append(('port', '', name, index, port['direction']))
    for name, cell in module['cells'].items():
        for pin, bits in cell['connections'].items():
            for index, bit in enumerate(bits):
                require(type(bit) is int, 'ASIC cell has an unmapped constant or unknown bit')
                nets.setdefault(bit, []).append(('cell', name, pin, index, cell['port_directions'][pin]))
    return {'nets': sorted(sorted(points) for points in nets.values()),
            'cells': {name: {'type': cell['type'], 'parameters': cell['parameters'],
                             'directions': cell['port_directions']} for name, cell in module['cells'].items()}}


def audit_circuit(module, library_modules, excluded):
    counts = {}
    for name, net in module['netnames'].items():
        require('init' not in net['attributes'], 'ASIC circuit depends on power-on initialization: ' + name)
    drivers, loads = {}, set()
    for port in module['ports'].values():
        if port['direction'] == 'input':
            for bit in port['bits']:
                drivers[bit] = drivers.get(bit, 0) + 1
        else:
            loads.update(port['bits'])
    for name, cell in module['cells'].items():
        kind = cell['type']
        require(kind in library_modules and kind not in excluded and kind.startswith('sky130_fd_sc_hd__'),
                'unmapped, forbidden or unknown ASIC cell: ' + kind)
        require(not cell['parameters'], 'unexpected standard-cell parameters')
        counts[kind] = counts.get(kind, 0) + 1
        ports = library_modules[kind]['ports']
        require(set(cell['connections']) <= set(ports), 'unknown standard-cell pin')
        for pin, port in ports.items():
            if port['direction'] == 'input':
                require(pin in cell['connections'], 'missing standard-cell input pin')
        for pin, bits in cell['connections'].items():
            direction = ports[pin]['direction']
            require(len(bits) == len(ports[pin]['bits']) and cell['port_directions'][pin] == direction,
                    'standard-cell pin width/direction mismatch')
            require(all(type(bit) is int for bit in bits), 'unmapped standard-cell constant')
            if direction == 'input':
                loads.update(bits)
            else:
                for bit in bits:
                    drivers[bit] = drivers.get(bit, 0) + 1
        if kind == 'sky130_fd_sc_hd__dfxtp_1':
            require(cell['connections']['CLK'] == module['ports']['clk']['bits'], 'standard-cell clock changed')
    require(all(drivers.get(bit) == 1 for bit in loads), 'undriven or multiply driven ASIC signal')
    connectivity(module)
    return counts
