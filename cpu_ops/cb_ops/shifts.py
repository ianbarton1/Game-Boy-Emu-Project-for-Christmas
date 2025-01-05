from number.short_int import ShortInt


def srl_n(cpu_obj, register:ShortInt):
    '''
        Shift right into carry, most signifcant bit set to 0
    '''

    cpu_obj.carry_flag = register.get_bit(bit_number=0)
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False

    register.value >>= 1

    cpu_obj.zero_flag = register.value == 0

def sla_n(cpu_obj, register:ShortInt):
    '''
        Shift left into carry, LSB of n set to 0
    '''
    cpu_obj.carry_flag = register.get_bit(bit_number=0)
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False

    register.value <<= 1

    cpu_obj.zero_flag = register.value == 0