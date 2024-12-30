from number.long_int import LongInt
from number.short_int import ShortInt


def add_n(cpu_obj, register:ShortInt):
    '''
        8-bit add to register A
    
    '''

    cpu_obj.half_carry_flag = (cpu_obj.register_A.lower_nibble + register.lower_nibble) > 15
    cpu_obj.carry_flag = (cpu_obj.register_A.value + register.value) > 255
    
    cpu_obj.register_A.value += register.value

    cpu_obj.zero_flag = cpu_obj.register_A.value == 0x00
    cpu_obj.subtract_flag = False

def add_nn(cpu_obj, long_register:LongInt):
    '''
        16-bit add to register HL
    
    '''

    cpu_obj.subtract_flag = False

    #carry flag logic
    #if the full 16 bit additions will result in a value higher than 2 to the 16 then a carry must've occurred

    full_carry_mask = 65535
    cpu_obj.carry_flag = (cpu_obj.register_HL.value + long_register.value) > full_carry_mask

    #half carry logic
    #Bitwise AND both registers with bottom 12 bits, sum and check whether the resulting sum requires more than
    #12 bits to represent, if true a half-carry must've occurred.
    half_carry_mask = 4095
    cpu_obj.half_carry_flag = ((cpu_obj.register_HL.value & half_carry_mask) + (long_register.value & half_carry_mask)) > half_carry_mask

    cpu_obj.register_HL.value += long_register.value