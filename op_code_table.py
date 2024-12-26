
from time import sleep
from bus import get_immediate_address_value, read_byte_at_pc
from cpu_ops.dec import dec_n
from cpu_ops.exclusive_or import xor_n
from cpu_ops.jumps import jp_n, jr_cc_n
from cpu_ops.loads import ld_A_into_register, ld_n, ld_n_nn, ld_val_into_register_a, ldd_hl_a
from cpu_ops.no_op import no_op
from cpu_ops.not_impl_op import halt_op
from op_code import OpCode


class OPCodeTable:
    unknown_op_code = OpCode(pnuemonic='???', cycles=4, function=lambda cpu_obj: halt_op(cpu_obj))
    _op_code_lookup = [unknown_op_code] * 256

    
    #0x
    _op_code_lookup[0x00] = OpCode(pnuemonic='NOP', cycles=4, function=lambda cpu_obj: no_op())
    _op_code_lookup[0x01] = OpCode(pnuemonic='LD BC, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_B, cpu_obj.register_C))

    _op_code_lookup[0x02] = OpCode(pnuemonic='LD (BC),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_BC.value),1))
    
    _op_code_lookup[0x05] = OpCode(pnuemonic='DEC B', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x06] = OpCode(pnuemonic='LD B, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x0A] = OpCode(pnuemonic='LD A,(BC)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_BC.value)))
    _op_code_lookup[0x0D] = OpCode(pnuemonic='DEC C', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x0E] = OpCode(pnuemonic='LD C, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_C))

    #1x
    _op_code_lookup[0x11] = OpCode(pnuemonic='LD DE, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_D, cpu_obj.register_E))
    _op_code_lookup[0x12] = OpCode(pnuemonic='LD (DE),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_DE.value),1))
    _op_code_lookup[0x15] = OpCode(pnuemonic='DEC D', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x16] = OpCode(pnuemonic='LD D, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x1A] = OpCode(pnuemonic='LD A,(DE)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_DE.value)))
    _op_code_lookup[0x1D] = OpCode(pnuemonic='DEC E ', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x1E] = OpCode(pnuemonic='LD E, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_E))
    

    #2x
    _op_code_lookup[0x20] = OpCode(pnuemonic='JR NZ, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.zero_flag, False))
    _op_code_lookup[0x21] = OpCode(pnuemonic='LD HL, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_H, cpu_obj.register_L))
    _op_code_lookup[0x25] = OpCode(pnuemonic='DEC H', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x26] = OpCode(pnuemonic='LD H, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x28] = OpCode(pnuemonic='JR Z, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.zero_flag, True))
    _op_code_lookup[0x2D] = OpCode(pnuemonic='DEC L', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x2E] = OpCode(pnuemonic='LD L, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_L))

    #3x
    _op_code_lookup[0x30] = OpCode(pnuemonic='JR NC, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.carry_flag, False))
    _op_code_lookup[0x31] = OpCode(pnuemonic='LD SP, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_S, cpu_obj.register_P))
    _op_code_lookup[0x32] = OpCode(pnuemonic='LD (HLD), A', cycles=8, function=lambda cpu_obj: ldd_hl_a(cpu_obj))

    #load variable from memory address - not sure on this
    _op_code_lookup[0x35] = OpCode(pnuemonic='DEC (HL)', cycles=12, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value)))
    _op_code_lookup[0x38] = OpCode(pnuemonic='JR C, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.carry_flag, True))
    _op_code_lookup[0x3D] = OpCode(pnuemonic='DEC A', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_A))
    _op_code_lookup[0x3E] = OpCode(pnuemonic='LD A,#', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, read_byte_at_pc(cpu_obj)))
    
    #4x
    _op_code_lookup[0x47] = OpCode(pnuemonic='LD B,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x4F] = OpCode(pnuemonic='LD C,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_C))


    
    #5x
    _op_code_lookup[0x57] = OpCode(pnuemonic='LD D,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x5F] = OpCode(pnuemonic='LD E,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_E))

    #6x
    _op_code_lookup[0x67] = OpCode(pnuemonic='LD H,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x6F] = OpCode(pnuemonic='LD L,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_L))

    #7x
    _op_code_lookup[0x77] = OpCode(pnuemonic='LD (HL),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value),1))
    _op_code_lookup[0x78] = OpCode(pnuemonic='LD A,B', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x79] = OpCode(pnuemonic='LD A,C', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x7A] = OpCode(pnuemonic='LD A,D', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x7B] = OpCode(pnuemonic='LD A,E', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x7C] = OpCode(pnuemonic='LD A,H', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x7D] = OpCode(pnuemonic='LD A,L', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x7E] = OpCode(pnuemonic='LD A,(HL)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value)))
    _op_code_lookup[0x7F] = OpCode(pnuemonic='LD A,A', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_A))
    

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
    ##TODO: not test - check on this
    _op_code_lookup[0xEA] = OpCode(pnuemonic='LD (nn),A', cycles=16, function=lambda cpu_obj: ld_A_into_register(cpu_obj, get_immediate_address_value(cpu_obj)))

    

    #Fx
    _op_code_lookup[0xFA] = OpCode(pnuemonic='LD A,(nn)', cycles=16, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, get_immediate_address_value(cpu_obj)))

    print("Op Code Table Implementation %", 100 - (_op_code_lookup.count(unknown_op_code)/ len(_op_code_lookup) * 100))
    sleep(1)

    def decode_instruction(self,op_code:int)->OpCode:
        return self._op_code_lookup[op_code]