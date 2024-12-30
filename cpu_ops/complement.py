def cpl(cpu):
    '''
        Complement A register
    
    '''

    cpu.register_A.value ^= 255

    cpu.half_carry_flag = True
    cpu.subtract_flag = True