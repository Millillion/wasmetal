"""Keep the standard DSP model's carry wiring explicit for Verilator scheduling."""


def split_carries(model):
    original='assign int_carry_in[3:1] = int_carry_out[2:0];'
    if model.count(original)!=1:
        raise ValueError('unrecognized standard DSP carry wiring')
    replacement='\n            '.join(
        f'assign int_carry_in[{bit+1}] = int_carry_out[{bit}];' for bit in range(3))
    return model.replace(original,replacement)
