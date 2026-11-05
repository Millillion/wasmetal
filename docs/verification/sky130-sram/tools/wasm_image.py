"""Validated Wasm binary -> execution image. No function-body interpretation.

Instruction identity is retained. Only immediates, indices and structured-control
targets are decoded. Instantiation expressions and execution use the RTL.
"""
from dataclasses import dataclass, field


class Unsupported(Exception):
    pass


class ImageError(Exception):
    pass


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def take(self, count):
        end = self.pos + count
        if count < 0 or end > len(self.data):
            raise ImageError("truncated binary")
        value = self.data[self.pos:end]
        self.pos = end
        return value

    def byte(self):
        return self.take(1)[0]

    def leb(self, signed=False, bits=64):
        value, shift = 0, 0
        while True:
            byte = self.byte()
            value |= (byte & 127) << shift
            shift += 7
            if not byte & 128:
                if signed and byte & 64:
                    value -= 1 << shift
                return value
            if shift >= bits + 7:
                raise ImageError("overlong LEB128")

    def name(self):
        return self.take(self.leb()).decode("utf-8")

    def vector(self, function):
        return [function(self) for _ in range(self.leb())]

    def remaining(self):
        return len(self.data) - self.pos


def value_type(r):
    kind = r.byte()
    return (kind, r.leb(True, 33)) if kind in (0x63, 0x64) else kind


def limits(r):
    flags = r.leb()
    if flags & ~7:
        raise Unsupported(f"limits flags {flags:#x}")
    minimum = r.leb()
    maximum = r.leb() if flags & 1 else None
    return minimum, maximum, bool(flags & 4)


@dataclass
class TypeDefinition:
    kind: int
    final: bool
    parents: list
    params: list = field(default_factory=list)
    results: list = field(default_factory=list)
    fields: list = field(default_factory=list)


def subtype(r):
    kind = r.byte()
    final, parents = True, []
    if kind in (0x4f, 0x50):
        final = kind == 0x4f
        parents = r.vector(lambda b: b.leb())
        kind = r.byte()
    t = TypeDefinition(kind, final, parents)
    if kind == 0x60:
        t.params, t.results = r.vector(value_type), r.vector(value_type)
    elif kind == 0x5f:
        t.fields = r.vector(lambda b: (value_type(b), b.byte()))
    elif kind == 0x5e:
        t.fields = [(value_type(r), r.byte())]
    else:
        raise Unsupported(f"type form {kind:#x}")
    return t


def storage_width(storage):
    if isinstance(storage, int):
        return {0x78: 8, 0x77: 16, 0x7f: 32, 0x7e: 64, 0x7d: 32, 0x7c: 64, 0x7b: 128}.get(storage, 128)
    return 128


@dataclass
class Instruction:
    op: int
    x: int = 0
    y: int = 0
    z: int = 0
    w: int = 0
    imm: int = 0
    targets: list = field(default_factory=list)
    handlers: list = field(default_factory=list)


def expression(r, types, stop_at_end=False):
    code, controls = [], []
    while r.remaining():
        op = r.byte()
        if op in (0xfb, 0xfc, 0xfd, 0xfe):
            op = (op << 16) | r.leb()
        i = Instruction(op)
        if op in (2, 3, 4, 0x1f):
            block_type = r.leb(True, 33)
            if block_type == -64:
                params, results = [], []
            elif block_type < 0:
                if block_type in (-28, -29):
                    r.leb(True, 33)  # heap type in an explicit reference block result
                params, results = [], [block_type]
            else:
                params, results = types[block_type]
            i.x, i.y = len(params), len(results)
            if op == 0x1f:
                for _ in range(r.leb()):
                    kind = r.byte()
                    tag = r.leb() if kind < 2 else 0
                    i.handlers.append((kind, tag, r.leb()))
            controls.append(len(code))
        elif op == 5:
            code[controls[-1]].w = len(code) + 1
        elif op == 0x0b:
            if controls:
                start = controls.pop()
                code[start].z = len(code)
                if code[start].op == 4 and not code[start].w:
                    code[start].w = len(code)
            elif stop_at_end:
                code.append(i)
                return code
        elif op in (0x08, 0x0c, 0x0d, 0x10, 0x12, 0x14, 0x15,
                    0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26,
                    0x3f, 0x40, 0xd2, 0xd5, 0xd6):
            i.x = r.leb()
        elif op in (0x11, 0x13):
            i.x, i.y = r.leb(), r.leb()
        elif op == 0x0e:
            count = r.leb()
            i.targets = [r.leb() for _ in range(count+1)]
            i.y = count
        elif op == 0x1c:
            r.vector(value_type)
        elif 0x28 <= op <= 0x3e or 0xfd0000 <= op <= 0xfd000b or 0xfd0054 <= op <= 0xfd005d:
            align = r.leb()
            i.x = r.leb() if align & 64 else 0
            i.imm = r.leb()
            if 0xfd0054 <= op <= 0xfd005b:
                i.y = r.byte()
        elif op in (0x41, 0x42):
            width = 32 if op == 0x41 else 64
            i.imm = r.leb(True, width) & ((1 << width)-1)
        elif op in (0x43, 0x44):
            i.imm = int.from_bytes(r.take(4 if op == 0x43 else 8), "little")
        elif op == 0xd0:
            i.imm = r.leb(True, 33) & ((1 << 64)-1)
        elif op in (0xfd000c, 0xfd000d):
            i.imm = int.from_bytes(r.take(16), "little")
        elif 0xfd0015 <= op <= 0xfd0022:
            i.x = r.byte()
        elif op in (0xfc0008, 0xfc000a, 0xfc000c, 0xfc000e):
            i.x, i.y = r.leb(), r.leb()
        elif op in (0xfc0009, 0xfc000b, 0xfc000d, 0xfc000f, 0xfc0010, 0xfc0011):
            i.x = r.leb()
        elif 0xfb0000 <= op <= 0xfb001e:
            sub = op & 0xffff
            if sub in (0, 1, 6, 7, 11, 12, 13, 14, 16):
                i.x = r.leb()
            elif sub in (2, 3, 4, 5, 8, 9, 10, 17, 18, 19):
                i.x, i.y = r.leb(), r.leb()
            elif sub in (20, 21, 22, 23):
                i.x = r.leb(True, 33)
            elif sub in (24, 25):
                i.w = r.byte()
                i.x, i.y, i.z = r.leb(), r.leb(True, 33), r.leb(True, 33)
        elif op >= 0xfe0000:
            raise Unsupported(f"instruction extension {op:#x}")
        elif op not in (0, 1, 0x0a, 0x0f, 0x1a, 0x1b, 0xd1, 0xd3, 0xd4) and not (
            0x45 <= op <= 0xc4 or 0xfc0000 <= op <= 0xfc0007 or 0xfd000e <= op <= 0xfd0113
        ):
            raise Unsupported(f"instruction {op:#x}")
        code.append(i)
    if controls:
        raise ImageError("unterminated control structure")
    return code


class Module:
    def __init__(self, data):
        r = Reader(data)
        if r.take(8) != b"\0asm\x01\0\0\0":
            raise ImageError("bad Wasm header")
        self.types = []
        self.type_defs = []
        self.rec_groups = []
        self.function_types = []
        self.bodies = []
        self.imports = []
        self.memories = []
        self.tables = []
        self.globals = []
        self.exports = {}
        self.data = []
        self.elements = []
        self.start = None
        self.tags = []
        while r.remaining():
            section = r.byte()
            s = Reader(r.take(r.leb()))
            if section == 0:
                continue
            if section == 1:
                for _ in range(s.leb()):
                    base = len(self.type_defs)
                    if s.data[s.pos] == 0x4e:
                        s.byte()
                        group = s.vector(subtype)
                    else:
                        group = [subtype(s)]
                    self.type_defs.extend(group)
                    self.types.extend((t.params, t.results) for t in group)
                    self.rec_groups.append((base, len(group)))
            elif section == 2:
                for _ in range(s.leb()):
                    module, name, kind = s.name(), s.name(), s.byte()
                    if kind == 0:
                        desc = s.leb()
                    elif kind == 1:
                        desc = value_type(s), limits(s)
                    elif kind == 2:
                        desc = limits(s)
                    elif kind == 3:
                        desc = value_type(s), s.byte()
                    elif kind == 4:
                        s.byte()
                        desc = s.leb()
                    else:
                        raise Unsupported(f"import kind {kind}")
                    self.imports.append((module, name, kind, desc))
            elif section == 3:
                self.function_types = s.vector(lambda b: b.leb())
            elif section == 4:
                for _ in range(s.leb()):
                    explicit = s.data[s.pos] == 0x40
                    if explicit:
                        s.take(2)  # validated 0x40 0x00 initializer prefix
                    ty, size = value_type(s), limits(s)
                    init = expression(s, self.types, True) if explicit else None
                    self.tables.append((ty, size, init))
            elif section == 5:
                self.memories = s.vector(limits)
            elif section == 6:
                for _ in range(s.leb()):
                    ty, mutable = value_type(s), s.byte()
                    self.globals.append((ty, mutable, expression(s, self.types, True)))
            elif section == 7:
                for _ in range(s.leb()):
                    name = s.name()
                    self.exports[name] = s.byte(), s.leb()
            elif section == 8:
                self.start = s.leb()
            elif section == 9:
                for _ in range(s.leb()):
                    flags = s.leb()
                    table = s.leb() if flags in (2, 6) else 0
                    offset = expression(s, self.types, True) if flags in (0, 2, 4, 6) else None
                    if flags & 4:
                        if flags != 4:
                            value_type(s)
                        elems = s.vector(lambda b: expression(b, self.types, True))
                    else:
                        if flags != 0:
                            if s.byte() != 0:
                                raise ImageError("invalid element kind")
                        elems = [[Instruction(0xd2, x=x), Instruction(0x0b)] for x in s.vector(lambda b: b.leb())]
                    self.elements.append((flags, table, offset, elems))
            elif section == 10:
                for _ in range(s.leb()):
                    body = Reader(s.take(s.leb()))
                    local_count = 0
                    for _ in range(body.leb()):
                        local_count += body.leb()
                        value_type(body)
                    self.bodies.append((local_count, expression(body, self.types)))
            elif section == 11:
                for _ in range(s.leb()):
                    flags = s.leb()
                    memory = s.leb() if flags == 2 else 0
                    offset = expression(s, self.types, True) if flags in (0, 2) else None
                    self.data.append((flags, memory, offset, s.take(s.leb())))
            elif section == 12:
                s.leb()
            elif section == 13:
                for _ in range(s.leb()):
                    s.byte()
                    self.tags.append(s.leb())
            else:
                raise Unsupported(f"section {section}")
            if s.remaining():
                raise ImageError(f"unconsumed bytes in section {section}")


def relocated(code, base, functions, globals_, memories, tables, types, data, elements, type_defs, tags, tag_types):
    """Relocate indices and control targets, retaining every original opcode."""
    result = []
    for original in code:
        i = Instruction(**vars(original))
        if i.op in (2, 3, 4, 0x1f):
            i.z += base
            if i.op == 4:
                i.w += base
            if i.op == 0x1f:
                i.handlers = [(kind, tags[tag] if kind < 2 else 0, label) for kind, tag, label in i.handlers]
        elif i.op == 8:
            i.x = tags[i.x]
            i.y = tag_types[i.x][1]
        elif i.op in (0x10, 0x12, 0xd2):
            i.x = functions[i.x]
        elif i.op in (0x23, 0x24):
            i.x = globals_[i.x]
        elif 0x28 <= i.op <= 0x40 or 0xfd0000 <= i.op <= 0xfd000b or 0xfd0054 <= i.op <= 0xfd005d:
            i.x = memories[i.x]
        elif i.op in (0x11, 0x13):
            i.x, i.y = types[i.x], tables[i.y]
        elif i.op in (0x14, 0x15):
            i.x = types[i.x]
        elif i.op in (0x25, 0x26, 0xfc000f, 0xfc0010, 0xfc0011):
            i.x = tables[i.x]
        elif i.op == 0xfc0008:
            i.x, i.y = data[i.x], memories[i.y]
        elif i.op == 0xfc0009:
            i.x = data[i.x]
        elif i.op == 0xfc000a:
            i.x, i.y = memories[i.x], memories[i.y]
        elif i.op == 0xfc000b:
            i.x = memories[i.x]
        elif i.op == 0xfc000c:
            i.x, i.y = elements[i.x], tables[i.y]
        elif i.op == 0xfc000d:
            i.x = elements[i.x]
        elif i.op == 0xfc000e:
            i.x, i.y = tables[i.x], tables[i.y]
        elif 0xfb0000 <= i.op <= 0xfb0013 and i.op != 0xfb000f:
            t = type_defs[i.x]
            if i.op in (0xfb0000, 0xfb0001):
                i.y = len(t.fields)
            elif 0xfb0002 <= i.op <= 0xfb0005:
                i.z = storage_width(t.fields[i.y][0])
            else:
                i.z = storage_width(t.fields[0][0])
            i.x = types[i.x]
            if i.op in (0xfb0009, 0xfb0012):
                i.y = data[i.y]
            elif i.op in (0xfb000a, 0xfb0013):
                i.y = elements[i.y]
            elif i.op == 0xfb0011:
                i.y = types[i.y]
        elif 0xfb0014 <= i.op <= 0xfb0017:
            i.x = types[i.x] if i.x >= 0 else i.x & 0xffffffff
        elif i.op in (0xfb0018, 0xfb0019):
            i.y = types[i.y] if i.y >= 0 else i.y & 0xffffffff
            i.z = types[i.z] if i.z >= 0 else i.z & 0xffffffff
        result.append(i)
    return result
