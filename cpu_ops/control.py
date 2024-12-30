import sys
from time import sleep
from bus import read_byte_at_pc

from number.long_int import LongInt
from stack import pop_from_stack, push_to_stack


def call_nn(cpu_obj):
    '''
        Call a sub-routine given an immediate 16 bit address
    
    
    '''
    #read where to jump from the next two immediate bytes in memory
    next_jump_address:LongInt = LongInt()

    
    next_jump_address.low_byte = read_byte_at_pc(cpu_obj)
    next_jump_address.high_byte = read_byte_at_pc(cpu_obj)
    

    #push the current program counter to the stack
    #TODO: should the program counter be a LongInt by default
    push_current_pc_to_stack(cpu_obj)

    #set program counter to previous address read from memory
    cpu_obj.program_counter = next_jump_address.value

def push_current_pc_to_stack(cpu_obj):
    pc_copy = LongInt(cpu_obj.program_counter)

    push_to_stack(cpu_obj, pc_copy.high_byte.value)
    push_to_stack(cpu_obj, pc_copy.low_byte.value)

def ret(cpu_obj):
    '''
        Returns back to previous routine call
    
    '''

    next_pc:LongInt = LongInt()

    next_pc.low_byte.value = pop_from_stack(cpu_obj).value
    next_pc.high_byte.value = pop_from_stack(cpu_obj).value

    jump_exec_to(cpu_obj, next_pc)

def jump_exec_to(cpu_obj, next_pc:LongInt):
    cpu_obj.program_counter = next_pc.value

def ret_conditional(cpu_obj, flag:bool, condition:bool, branch_clock_wait:int = 20):
    '''
        Return if a condition is met

        branch_clock_wait is the number of cycles to wait if the branch is taken
    
    '''
    if flag == condition:
        ret(cpu_obj)
        cpu_obj.clock_wait = branch_clock_wait

def restart(cpu_obj, target_address:LongInt):
    '''
        Push present address onto stack and jump to address
    
    '''

    push_current_pc_to_stack(cpu_obj)

    jump_exec_to(cpu_obj, target_address)

