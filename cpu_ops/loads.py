def ld_n_nn(cpu, high_register, low_register):
    '''
        16 bit load immediate value into 16 bit register
    '''
    low_register.value = cpu.bus.read(cpu.program_counter).value
    high_register.value = cpu.bus.read(cpu.program_counter+1).value
    
    cpu.program_counter += 2

def ld_n(cpu, register):
    '''
        8 bit load immediate value
    '''

    register.value = cpu.bus.read(cpu.program_counter).value

    cpu.program_counter += 1


def ldd_hl_a(cpu):
    '''
        Put register A into Memory address stored in HL, decrement HL
           
    '''
    print(cpu.register_HL)
    cpu.bus.write(cpu.register_HL.value, cpu.register_A)

    cpu.register_HL.value = cpu.register_HL.value - 1