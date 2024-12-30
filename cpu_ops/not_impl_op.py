


import sys
from time import perf_counter


def halt_op(cpu):
    '''
        This "op" is the default entry in the op table and represents that the CPU has
        attempted to run a operation that has not been implemented.
    
    '''

    print(f"An unimplemented instruction has been encountered at {hex(cpu.last_fetch_pc)} , the opcode encountered was {hex(cpu.op_code)} {hex(cpu.cb_code) if cpu.op_code == 0xCB else ''}")
    print(cpu)
    print(perf_counter())
    sys.exit()