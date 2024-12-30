from number.short_int import ShortInt


def res_b_r(cpu_obj, target_register:ShortInt, bit_number:int):
    '''

        reset chosen bit

    '''
    target_register.write_bit(bit_number, False)