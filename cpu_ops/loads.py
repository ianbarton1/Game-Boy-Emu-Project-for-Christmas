from bus import read_byte_at_pc, read_byte_from_address_from_register

def ld_n_nn(cpu, high_register, low_register):
    '''
        16 bit load immediate value into 16 bit register
    '''

    low_register.value = read_byte_at_pc(cpu).value
    high_register.value = read_byte_at_pc(cpu).value


def ld_n(cpu, register):
    '''
        8 bit load immediate value
    '''

    register.value = read_byte_at_pc(cpu).value


def ldd_hl_a(cpu):
    '''
        Put register A into Memory address stored in HL, decrement HL
           
    '''
    cpu.bus.write(cpu.register_HL.value, cpu.register_A.value)

    cpu.register_HL.value -= 1


def ldi_hl_a(cpu):
    try:
        cpu.bus.write(cpu.register_HL.value, cpu.register_A.value)
    except AttributeError:
        print("error value", cpu.register_HL)
        sys.exit()
    # except TypeError:
    #     print(cpu.register_HL.value, cpu.register_A.value)
    #     sys.exit()

    
    cpu.register_HL.value += 1

def ldi_a_hl(cpu):
    cpu.register_A.value = read_byte_from_address_from_register(cpu, cpu.register_HL).value
    
    cpu.register_HL.value += 1

def ldd_a_hl(cpu):
    cpu.register_A.value = read_byte_from_address_from_register(cpu, cpu.register_HL).value
    
    cpu.register_HL.value -= 1

import sys
from number.short_int import ShortInt

def ld_A_into_register(cpu, destination_byte:ShortInt):

    destination_byte.value = cpu.register_A.value

    # cpu.program_counter += 1 + program_count_inc

def ld_val_into_register_a(cpu, source_byte:ShortInt):
    cpu.register_A.value = source_byte.value

def ld_reg2_into_reg1(cpu, register_1:ShortInt, register_2:ShortInt):
    '''
        Store the value of register_2 into register_1
    
    
    '''    
    register_1.value = register_2.value


def ld_hl_sp(cpu_obj):
    '''

    Put SP + n effective address into HL.
    '''

    immediate_byte = read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL).signed_value
    cpu_obj.zero_flag = False
    cpu_obj.subtract_flag = False
    #carry flag logic
    #if the full 16 bit additions will result in a value higher than 2 to the 16 then a carry must've occurred

    full_carry_mask = 65535
    cpu_obj.carry_flag = (cpu_obj.register_HL.value + immediate_byte) > full_carry_mask

    #half carry logic
    #Bitwise AND both registers with bottom 12 bits, sum and check whether the resulting sum requires more than
    #12 bits to represent, if true a half-carry must've occurred.
    half_carry_mask = 4095
    cpu_obj.half_carry_flag = ((cpu_obj.register_HL.value & half_carry_mask) + (immediate_byte & half_carry_mask)) > half_carry_mask

    
    cpu_obj.register_HL.value = (cpu_obj.stack_pointer.value + immediate_byte)

    
