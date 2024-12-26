from number.short_int import ShortInt


def xor_n(cpu, input_register:ShortInt):
    '''implements the XOR operation, logical exclusive OR with register A (hardcoded), 
    register should be the input register, result is stored back in register_A'''

    cpu.register_A.value = cpu.register_A.value ^ input_register.value

    cpu.zero_flag = (cpu.register_A.value == 0x00)
    cpu.half_carry_flag = False
    cpu.carry_flag = False
    cpu.subtract_flag = False
