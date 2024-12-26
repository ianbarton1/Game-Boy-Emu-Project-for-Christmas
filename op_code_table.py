from cpu_ops.exclusive_or import xor_n
from cpu_ops.jumps import jp_n
from cpu_ops.loads import ld_n, ld_n_nn, ldd_hl_a
from cpu_ops.no_op import no_op
from cpu_ops.not_impl_op import halt_op
from op_code import OpCode


class OPCodeTable:
    unknown_op_code = OpCode(pnuemonic='???', cycles=4, function=lambda cpu_obj: halt_op(cpu_obj))
    _op_code_lookup = [unknown_op_code] * 256

    #0x
    _op_code_lookup[0x00] = OpCode(pnuemonic='NOP', cycles=4, function=lambda cpu_obj: no_op())
    _op_code_lookup[0x01] = OpCode(pnuemonic='LD BC, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_B, cpu_obj.register_C))
    _op_code_lookup[0x06] = OpCode(pnuemonic='LD B, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x0E] = OpCode(pnuemonic='LD C, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_C))

    #1x
    _op_code_lookup[0x11] = OpCode(pnuemonic='LD DE, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_D, cpu_obj.register_E))
    _op_code_lookup[0x16] = OpCode(pnuemonic='LD D, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x1E] = OpCode(pnuemonic='LD E, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x26] = OpCode(pnuemonic='LD H, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x2E] = OpCode(pnuemonic='LD L, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_L))

    #2x
    _op_code_lookup[0x21] = OpCode(pnuemonic='LD HL, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_H, cpu_obj.register_L))
    
    #3x
    _op_code_lookup[0x31] = OpCode(pnuemonic='LD SP, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_S, cpu_obj.register_P))

    _op_code_lookup[0x32] = OpCode(pnuemonic='LD (HLD), A', cycles=8, function=lambda cpu_obj: ldd_hl_a(cpu_obj))
    #4x

    #5x

    #6x

    #7x

    #8x

    #9x

    #Ax
    _op_code_lookup[0xA8] = OpCode(pnuemonic='XOR b', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0xA9] = OpCode(pnuemonic='XOR c', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0xAA] = OpCode(pnuemonic='XOR d', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0xAB] = OpCode(pnuemonic='XOR e', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0xAC] = OpCode(pnuemonic='XOR h', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0xAD] = OpCode(pnuemonic='XOR a', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_L))

    _op_code_lookup[0xAF] = OpCode(pnuemonic='XOR a', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_A))

    #Bx

    #Cx
    _op_code_lookup[0xC3] = OpCode(pnuemonic='JP n', cycles=16, function=lambda cpu_obj: jp_n(cpu_obj))

    #Dx

    #Ex

    #Fx

    print("Op Code Table Implementation %", 100 - (_op_code_lookup.count(unknown_op_code)/ len(_op_code_lookup) * 100))


    def decode_instruction(self,op_code:int)->OpCode:
        return self._op_code_lookup[op_code]