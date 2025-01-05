from number.short_int import ShortInt


def res_b_r(cpu_obj, target_register:ShortInt, bit_number:int):
    '''

        reset chosen bit

    '''
    target_register.write_bit(bit_number, False)


def bit_b_r(cpu_obj, target_register:ShortInt, bit_number:int):
    '''

        test bit n in register r

    '''

    cpu_obj.zero_flag = not target_register.get_bit(bit_number)
    cpu_obj.half_carry_flag = True
    cpu_obj.subtract_flag = False