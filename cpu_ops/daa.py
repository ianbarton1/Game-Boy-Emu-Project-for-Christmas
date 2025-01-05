from number.short_int import ShortInt


def daa(cpu_obj):
    '''
        Performs the Decimal Adjustment to Accumlator instruction:

        This instruction's job is to 'correct' maths which has been done back
        into Binary Coded Decimal i.e. each nibble of a byte represents a number

        the top/bottom nibble can range from 0x0 to 0x9 only,
    '''
    register:ShortInt = cpu_obj.register_A
    new_carry_state:bool = cpu_obj.carry_flag
    if not cpu_obj.subtract_flag:
        if register.lower_nibble > 0x9 or cpu_obj.half_carry_flag:
            register.value += 0x6
        if register.upper_nibble > 0x9 or cpu_obj.carry_flag:
            register.value += 0x60
            new_carry_state = True
    else:
        if cpu_obj.half_carry_flag:
            register.value -= 0x6
        if cpu_obj.carry_flag:
            register.value -= 0x60
            new_carry_state = True

    if register.value > 0x99:
        new_carry_state = True

    cpu_obj.half_carry_flag = False
    cpu_obj.carry_flag = new_carry_state
    cpu_obj.zero_flag = register.value == 0


