from number.short_int import ShortInt


def swap(cpu_obj, value:ShortInt):
    '''
        Swap the upper and lower nibbles of supplied byte
    
    '''
    
    value.swap_nibbles()

    cpu_obj.zero_flag = value.value == 0
    cpu_obj.carry_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.subtract_flag = False