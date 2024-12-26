# from cpu import CPU
from number.long_int import LongInt

def jp_n(cpu):
    '''
        Jump instruction immediate 2 byte address (least signifcant first)
    
    '''

    least_signifant_byte = cpu.bus.read(cpu.program_counter)
    most_significant_byte = cpu.bus.read(cpu.program_counter + 1)

    full_address = LongInt()
    full_address.low_byte = least_signifant_byte
    full_address.high_byte = most_significant_byte

    cpu.program_counter = full_address.value

    # print(f"JP to {cpu.program_counter}")


def jr_cc_n(cpu, flag:bool, jumping_condition:bool):
    cpu.program_counter += 1

    if flag != jumping_condition:
        return
    
    

    offset = cpu.bus.read(cpu.program_counter - 1).signed_value
    
    cpu.program_counter += offset    