'''
TODO

Subtraction seems like a strange operation

0x15 - 0x16 = 0xFF (underflow - ok) in this instance, carry, half-carry, subtract flags were set
0x17 - 0x17 = 0x01 (no underflow - ok) only the subtract flag was set
0x16 - 0x16 = 0x00 - zero flag set, subtract flag set
0xFF - 0x7F = 0x80 - subtract flag set
0xFF - 0x80 = 0x7F - subtract flag set
0xFF - 0xFE = 0x01 - subtract flag set



'''

from number.short_int import ShortInt


def sub_n(cpu_obj, register:ShortInt):
    '''
        Subtract register value from register a
        The flag behaviour has been stolen from bgb instead of the GBCPUMan.pdf dpcumentation

    '''

    cpu_obj.subtract_flag = True

    cpu_obj.half_carry_flag = register.value > cpu_obj.register_A.value
    cpu_obj.carry_flag = cpu_obj.half_carry_flag

    cpu_obj.register_A.value -= register.value

    cpu_obj.zero_flag = cpu_obj.register_A.value == 0
    
    

