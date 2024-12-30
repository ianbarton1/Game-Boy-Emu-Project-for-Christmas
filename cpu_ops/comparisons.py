
from number.short_int import ShortInt
def cp_n(cpu_obj, value:ShortInt):
    '''
        compare register A with value provided.

        Apparently it's basically a subtraction but the results are ignored.
    
    '''
    cpu_obj.zero_flag = cpu_obj.register_A.value == value.value
    cpu_obj.subtract_flag = True
    cpu_obj.carry_flag = cpu_obj.register_A.value < value.value
    cpu_obj.half_carry_flag = cpu_obj.register_A.get_bit(bit_number=4) == value.get_bit(bit_number=4)