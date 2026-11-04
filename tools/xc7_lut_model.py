"""Private, checked lookup optimization for the pinned Yosys 7-series LUTs."""
import re


def fast_lut(model, name):
    if re.fullmatch(r'LUT[1-6]', name) is None:
        raise ValueError('unsupported 7-series LUT: '+name)
    width = int(name[-1])
    pins = '{'+','.join('I'+str(i) for i in reversed(range(width)))+'}'
    original = 'I0 ? INIT[1] : INIT[0]' if width == 1 else 'I0 ? s1[1] : s1[0]'
    anchor = 'assign O = '+original+';'
    if model.count(anchor) != 1:
        raise ValueError('unrecognized pinned 7-series LUT output: '+name)
    return model.replace(anchor, f'assign O = $isunknown({pins}) ? ({original}) : INIT[{pins}];')
