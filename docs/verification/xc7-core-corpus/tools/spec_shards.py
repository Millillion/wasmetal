"""Strict ownership and independence checks for official-script CI partitions."""
import hashlib
from pathlib import Path

from wasm_image import Module

PARTITIONABLE = {'return_call.wast', 'return_call_indirect.wast', 'return_call_ref.wast'}
ERROR_COUNTS = ('failed', 'unsupported', 'conversion_errors', 'blocked', 'runner_errors')
# Deliberately conservative: control, locals, immutable reads, scalar arithmetic,
# and function references. No stores, allocation, table writes or segment drops.
PURE_OPS = set(range(0x41, 0xc5)) | {
    0, 1, 2, 3, 4, 5, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x1a, 0x1b, 0x1c,
    0x20, 0x21, 0x22, 0x23, 0x25, 0xd0, 0xd1, 0xd2, 0xd3, 0xd4,
}
CONSTANT_OPS = {0x0b, 0x41, 0x42, 0x43, 0x44, 0xd0, 0xd2}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent_module(module, fixture):
    require(not module.memories and not module.data and not module.tags and module.start is None,
            'command partition requires no memory, data, tags or start function')
    require(all(not mutable for _, mutable, _ in module.globals), 'mutable global in partitioned module')
    for origin, name, kind, type_index in module.imports:
        require((origin, name, kind) == ('spectest', 'print_i32_f32', 0), 'stateful or unknown import')
        export_kind, index = fixture.exports[name]
        require(not fixture.imports and export_kind == 0, 'unexpected spectest implementation')
        require(fixture.bodies[index][0] == 0 and [i.op for i in fixture.bodies[index][1]] == [0x0b],
                'spectest print must be an empty function')
        require(module.types[type_index] == fixture.types[fixture.function_types[index]], 'spectest type mismatch')
    require(all(i.op in PURE_OPS for _, body in module.bodies for i in body),
            'stateful or unreviewed instruction in partitioned module')
    initializers = [code for _, _, code in module.globals]
    initializers += [code for _, _, code in module.tables if code is not None]
    for _, _, offset, elements in module.elements:
        if offset is not None:
            initializers.append(offset)
        initializers.extend(elements)
    require(all(i.op in CONSTANT_OPS for code in initializers for i in code),
            'unreviewed initializer in partitioned module')


def independent_script(name, target, commands, fixture_path):
    require(name in PARTITIONABLE, 'only reviewed tail-call scripts may be partitioned by command')
    fixture = Module(Path(fixture_path).read_bytes())
    for command in commands:
        kind = command['type']
        require(kind in {'module', 'assert_return', 'assert_trap', 'assert_invalid', 'assert_malformed'},
                'stateful or unreviewed script command')
        if kind == 'module':
            independent_module(Module((target.parent/command['filename']).read_bytes()), fixture)
        elif kind in {'assert_return', 'assert_trap'}:
            action = command['action']
            require(action['type'] == 'invoke' and 'module' not in action, 'nonlocal action in partitioned script')
            require(all(v['type'] in {'i32', 'i64', 'f32', 'f64'} for v in action['args']),
                    'reference arguments may retain state between commands')


def validate_plan(plan, sources_hash, command_counts):
    require(plan.get('version') == 1, 'unsupported partition plan')
    require(plan.get('official_sources_sha256') == sources_hash, 'partition plan source mismatch')
    require(plan.get('command_counts') == command_counts, 'partition plan command counts mismatch')
    ids = [s['id'] for s in plan['shards']]
    require(ids and len(ids) == len(set(ids)), 'missing or duplicate shard id')
    require(all(isinstance(i, str) and len(i) == 2 and i.isascii() and i.isdigit() for i in ids),
            'invalid shard id')
    coverage = {name: set() for name in command_counts}
    for shard in plan['shards']:
        require(shard['entries'], 'empty shard')
        names = set()
        for entry in shard['entries']:
            name = entry['suite']
            require(name in coverage and name not in names, 'unknown or duplicate suite entry')
            names.add(name)
            selected = entry['commands']
            if selected is None:
                selected = list(range(command_counts[name]))
            else:
                require(name in PARTITIONABLE, 'command partition for an unreviewed suite')
            require(selected and all(type(i) is int and 0 <= i < command_counts[name] for i in selected),
                    'invalid command ownership')
            require(len(selected) == len(set(selected)), 'duplicate command ownership')
            require(selected == sorted(selected), 'command ownership must preserve script order')
            require(not coverage[name].intersection(selected), 'command owned by multiple shards')
            coverage[name].update(selected)
    require(all(coverage[name] == set(range(count)) for name, count in command_counts.items()),
            'partition plan omits official commands')


def clean_report(report):
    require('identity_error' in report and report['identity_error'] is None, 'report identity failure')
    require(all(type(v) is int and v >= 0 for v in report['totals'].values()), 'invalid report counts')
    require(not any(report['totals'].get(k, 0) for k in ERROR_COUNTS), 'report contains errors')
    require(not any(s['failures'] for s in report['suites']), 'suite contains failures')
    require(all(type(v) is int and v >= 0 for s in report['suites'] for v in s['counts'].values()), 'invalid suite counts')
    require(len(report['suites']) == report['suite_files'], 'suite count mismatch')
    require(len({s['suite'] for s in report['suites']}) == len(report['suites']), 'duplicate suite report')
