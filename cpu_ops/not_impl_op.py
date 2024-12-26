


import sys


def halt_op(cpu):
    '''
        This "op" is the default entry in the op table and represents that the CPU has
        attempted to run a operation that has not been implemented.
    
    '''

    print(f"An unimplemented instruction has been encountered at {hex(cpu.program_counter - 1)}, the opcode encountered was {hex(cpu.op_code)}")
    sys.exit()