# from cpu import CPU
import sys
from time import sleep
from cpu_ops.control import jump_exec_to
from number.long_int import LongInt
from bus import read_byte_at_pc

def jp_n(cpu):
    '''
        Jump instruction immediate 2 byte address (least signifcant first)
    
    '''

    least_signifant_byte = read_byte_at_pc(cpu)
    most_significant_byte = read_byte_at_pc(cpu)

    full_address = LongInt()
    full_address.low_byte = least_signifant_byte
    full_address.high_byte = most_significant_byte

    cpu.program_counter = full_address.value

    # print(f"JP to {cpu.program_counter}")


def jr_cc_n(cpu, flag:bool, jumping_condition:bool):
    offset = read_byte_at_pc(cpu).signed_value

    if flag != jumping_condition:
        return
    
    cpu.program_counter += offset

def jp_hl(cpu_obj):
    '''
        Jump execution to address contained in register HL
    '''
    jump_exec_to(cpu_obj, cpu_obj.register_HL)

def jp_nn(cpu_obj, flag:bool, condition:bool):
    '''
        two byte immediate jump with condition
    
    '''
    
    jump_address = LongInt()
    jump_address.low_byte = read_byte_at_pc(cpu_obj)
    jump_address.high_byte = read_byte_at_pc(cpu_obj)

    if flag != condition:
        return

    jump_exec_to(cpu_obj, jump_address)



def jr_n(cpu_obj):
    '''
        relative jump immediate value
    '''

    address_offset = read_byte_at_pc(cpu_obj).signed_value

    jump_exec_to(cpu_obj, LongInt(cpu_obj.program_counter + address_offset))