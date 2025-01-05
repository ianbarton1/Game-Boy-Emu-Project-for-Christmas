from number.short_int import ShortInt


def set_b_r(cpu_obj,target_register:ShortInt, bit_number:int):
    '''
        Set bit b in target register
    '''
    target_register.write_bit(bit_number=bit_number, bit= True)