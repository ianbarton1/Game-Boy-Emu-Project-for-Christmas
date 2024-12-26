from number.short_int import ShortInt




def dec_n(cpu, register:ShortInt):
    '''
        Decrement given register
    '''
    
    bit_4:bool = register.get_bit(bit_number=4)

    register.value -= 1
    if register.value < 0:
        register.value = 255
    
    #not sure if the zero flag should be cleared if the result isn't 0
    cpu.zero_flag = register.value == 0
    cpu.subtract_flag = True
    cpu.half_carry_flag = bit_4 != register.get_bit(bit_number=4)