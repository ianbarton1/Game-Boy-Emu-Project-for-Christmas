
#FIXME: I think this may be incorrect behaviour
from number.short_int import ShortInt


def rlca(cpu_obj):
    '''
        Rotate A left, old bit 7 in carry flag
    '''
    cpu_obj.carry_flag = cpu_obj.register_A.get_bit(bit_number=7)
    
    cpu_obj.register_A.value <<= 1
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.zero_flag = cpu_obj.register_A.value == 0
    
    cpu_obj.register_A.write_bit(bit_number = 0, bit= cpu_obj.carry_flag)

def rla(cpu_obj):
    '''
        Rotate A left through carry bit, old bit 7 in carry flag
    '''
    prev_carry_flag = cpu_obj.carry_flag
    cpu_obj.carry_flag = cpu_obj.register_A.get_bit(bit_number=7)
    
    cpu_obj.register_A.value <<= 1
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.zero_flag = cpu_obj.register_A.value == 0
    
    cpu_obj.register_A.write_bit(bit_number = 0, bit= prev_carry_flag)


def rrca(cpu_obj):
    '''
        Rotate A right, old bit 0 in carry flag
    '''
    cpu_obj.carry_flag = cpu_obj.register_A.get_bit(bit_number=0)
    
    cpu_obj.register_A.value >>= 1
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.zero_flag = cpu_obj.register_A.value == 0
    
    cpu_obj.register_A.write_bit(bit_number = 7, bit= cpu_obj.carry_flag)

def rra(cpu_obj):
    '''
        Rotate A right through carry bit, old bit 0 in carry flag
    '''
    prev_carry_flag = cpu_obj.carry_flag
    cpu_obj.carry_flag = cpu_obj.register_A.get_bit(bit_number=0)
    
    cpu_obj.register_A.value >>= 1
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.zero_flag = cpu_obj.register_A.value == 0
    
    cpu_obj.register_A.write_bit(bit_number = 7, bit= prev_carry_flag)

def rr_n(cpu_obj, target_register:ShortInt):
    prev_carry_flag = cpu_obj.carry_flag
    cpu_obj.carry_flag = target_register.get_bit(bit_number=0)
    
    target_register.value >>= 1
    cpu_obj.subtract_flag = False
    cpu_obj.half_carry_flag = False
    cpu_obj.zero_flag = target_register.value == 0
    
    target_register.write_bit(bit_number = 7, bit= prev_carry_flag)