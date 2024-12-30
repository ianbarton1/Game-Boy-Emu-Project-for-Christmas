from number.long_int import LongInt
from number.short_int import ShortInt




def dec_n(cpu, register:ShortInt):
    '''
        Decrement given register
    '''
    
    bit_4:bool = register.get_bit(bit_number=4)

    register.value -= 1
    
    #not sure if the zero flag should be cleared if the result isn't 0
    cpu.zero_flag = register.value == 0
    cpu.subtract_flag = True
    cpu.half_carry_flag = bit_4 != register.get_bit(bit_number=4)

def inc_n(cpu, register:ShortInt):
    '''
        Increment given register
    '''
    
    bit_3:bool = register.get_bit(bit_number=3)

    register.value += 1
        
    #not sure if the zero flag should be cleared if the result isn't 0
    cpu.zero_flag = register.value == 0
    cpu.subtract_flag = False
    cpu.half_carry_flag = bit_3 != register.get_bit(bit_number=3)

def dec_nn(_, large_register:LongInt):
    large_register.value -= 1

def inc_nn(_, large_register:LongInt):
    large_register.value += 1

