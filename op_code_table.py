
from time import sleep
from bus import get_immediate_address_value, read_byte_at_pc, read_byte_from_address_from_register

from cpu_ops.cb_ops.set_bit import set_b_r
from cpu_ops.daa import daa
from cpu_ops.adds import adc_n, add_n, add_nn
from cpu_ops.cb_ops.reset_bit import bit_b_r, res_b_r
from cpu_ops.cb_ops.swap_ops import swap
from cpu_ops.comparisons import cp_n
from cpu_ops.complement import cpl
from cpu_ops.control import call_cc_nn, call_nn, halt, pop, push, restart, ret, ret_conditional, reti, stop
from cpu_ops.inc_dec import dec_n, dec_nn, inc_n, inc_nn
from cpu_ops.logical_operators import and_n, or_n, xor_n
from cpu_ops.interrupts import di, ei
from cpu_ops.jumps import jp_hl, jp_n, jp_nn, jr_cc_n, jr_n
from cpu_ops.loads import ld_A_into_register, ld_hl_sp, ld_n, ld_n_nn, ld_reg2_into_reg1, ld_val_into_register_a, ldd_a_hl, ldd_hl_a, ldi_a_hl, ldi_hl_a
from cpu_ops.no_op import no_op
from cpu_ops.not_impl_op import halt_op
from cpu_ops.rotates import rla, rlca, rr_n, rrca
from cpu_ops.cb_ops.shifts import sla_n, srl_n
from cpu_ops.subtractions import sub_n
from number.long_int import LongInt
from op_code import OpCode


class OPCodeTable:
    unknown_op_code = OpCode(pnuemonic='???', cycles=4, function=lambda cpu_obj: halt_op(cpu_obj))
    unknown_cb_code = OpCode(pnuemonic='CB ???', cycles=8, function=lambda cpu_obj: halt_op(cpu_obj))
    _op_code_lookup = [unknown_op_code] * 256
    _cb_code_lookup = [unknown_cb_code] * 256

    def __init__(self, parent_cpu):
        self.parent_cpu = parent_cpu

    
    #0x
    _op_code_lookup[0x00] = OpCode(pnuemonic='NOP', cycles=4, function=lambda cpu_obj: no_op())
    _op_code_lookup[0x01] = OpCode(pnuemonic='LD BC, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_B, cpu_obj.register_C))

    _op_code_lookup[0x02] = OpCode(pnuemonic='LD (BC),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_BC.value)))
    _op_code_lookup[0x03] = OpCode(pnuemonic="INC BC", cycles=8, function=lambda cpu_obj: inc_nn(cpu_obj, cpu_obj.register_BC))
    _op_code_lookup[0x04] = OpCode(pnuemonic='INC B', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x05] = OpCode(pnuemonic='DEC B', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x06] = OpCode(pnuemonic='LD B, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x07] = OpCode(pnuemonic='RLCA', cycles=4, function=lambda cpu_obj: rlca(cpu_obj))
    _op_code_lookup[0x09] = OpCode(pnuemonic='ADD HL, BC', cycles=8, function=lambda cpu_obj: add_nn(cpu_obj, cpu_obj.register_BC))
    _op_code_lookup[0x0A] = OpCode(pnuemonic='LD A,(BC)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_BC.value)))
    _op_code_lookup[0x0B] = OpCode(pnuemonic="DEC BC", cycles=8, function=lambda cpu_obj: dec_nn(cpu_obj, cpu_obj.register_BC))
    _op_code_lookup[0x0C] = OpCode(pnuemonic='INC C', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x0D] = OpCode(pnuemonic='DEC C', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x0E] = OpCode(pnuemonic='LD C, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x0F] = OpCode(pnuemonic='RRCA', cycles=4, function=lambda cpu_obj: rrca(cpu_obj))

    #1x
    _op_code_lookup[0x10] = OpCode(pnuemonic='STOP 0', cycles=4, function=lambda cpu_obj: stop(cpu_obj))
    _op_code_lookup[0x11] = OpCode(pnuemonic='LD DE, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_D, cpu_obj.register_E))
    _op_code_lookup[0x12] = OpCode(pnuemonic='LD (DE),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_DE.value)))
    _op_code_lookup[0x13] = OpCode(pnuemonic="INC DE", cycles=8, function=lambda cpu_obj: inc_nn(cpu_obj, cpu_obj.register_DE))
    _op_code_lookup[0x14] = OpCode(pnuemonic='INC D', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x15] = OpCode(pnuemonic='DEC D', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x16] = OpCode(pnuemonic='LD D, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x17] = OpCode(pnuemonic='RLA', cycles=4, function=lambda cpu_obj: rla(cpu_obj))
    _op_code_lookup[0x18] = OpCode(pnuemonic="JR n", cycles=8, function= lambda cpu_obj: jr_n(cpu_obj))
    _op_code_lookup[0x19] = OpCode(pnuemonic='ADD HL, DE', cycles=8, function=lambda cpu_obj: add_nn(cpu_obj, cpu_obj.register_DE))
    _op_code_lookup[0x1A] = OpCode(pnuemonic='LD A,(DE)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_DE.value)))
    _op_code_lookup[0x1B] = OpCode(pnuemonic="DEC DE", cycles=8, function=lambda cpu_obj: dec_nn(cpu_obj, cpu_obj.register_DE))
    _op_code_lookup[0x1C] = OpCode(pnuemonic='INC E', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x1D] = OpCode(pnuemonic='DEC E ', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x1E] = OpCode(pnuemonic='LD E, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x1F] = OpCode(pnuemonic='RRC', cycles=4, function=lambda cpu_obj: rrca(cpu_obj))
    

    #2x
    _op_code_lookup[0x20] = OpCode(pnuemonic='JR NZ, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.zero_flag, False))
    _op_code_lookup[0x21] = OpCode(pnuemonic='LD HL, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_H, cpu_obj.register_L))
    _op_code_lookup[0x22] = OpCode(pnuemonic='LDI (HL), A', cycles=8, function=lambda cpu_obj: ldi_hl_a(cpu_obj))
    _op_code_lookup[0x23] = OpCode(pnuemonic="INC HL", cycles=8, function=lambda cpu_obj: inc_nn(cpu_obj, cpu_obj.register_HL))
    _op_code_lookup[0x24] = OpCode(pnuemonic='INC H', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x25] = OpCode(pnuemonic='DEC H', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x26] = OpCode(pnuemonic='LD H, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x27] = OpCode(pnuemonic='DAA', cycles=4, function=lambda cpu_obj: daa(cpu_obj))
    _op_code_lookup[0x28] = OpCode(pnuemonic='JR Z, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.zero_flag, True))
    _op_code_lookup[0x29] = OpCode(pnuemonic='ADD HL, HL', cycles=8, function=lambda cpu_obj: add_nn(cpu_obj, cpu_obj.register_HL))
    _op_code_lookup[0x2A] = OpCode(pnuemonic='LDI A, (HL)', cycles=8, function=lambda cpu_obj: ldi_a_hl(cpu_obj))
    _op_code_lookup[0x2B] = OpCode(pnuemonic="DEC HL", cycles=8, function=lambda cpu_obj: dec_nn(cpu_obj, cpu_obj.register_HL))
    _op_code_lookup[0x2C] = OpCode(pnuemonic='INC L', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x2D] = OpCode(pnuemonic='DEC L', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x2E] = OpCode(pnuemonic='LD L, d8', cycles=8, function=lambda cpu_obj: ld_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x2F] = OpCode(pnuemonic='CPL', cycles=4, function=lambda cpu_obj: cpl(cpu_obj))

    #3x
    _op_code_lookup[0x30] = OpCode(pnuemonic='JR NC, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.carry_flag, False))
    _op_code_lookup[0x31] = OpCode(pnuemonic='LD SP, d16', cycles=12, function=lambda cpu_obj: ld_n_nn(cpu_obj, cpu_obj.register_S, cpu_obj.register_P))
    _op_code_lookup[0x32] = OpCode(pnuemonic='LD (HLD), A', cycles=8, function=lambda cpu_obj: ldd_hl_a(cpu_obj))
    _op_code_lookup[0x33] = OpCode(pnuemonic="INC SP", cycles=8, function=lambda cpu_obj: inc_nn(cpu_obj, cpu_obj.register_SP))
    _op_code_lookup[0x34] = OpCode(pnuemonic='INC (HL)', cycles=12, function=lambda cpu_obj: inc_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))

    #load variable from memory address - not sure on this
    _op_code_lookup[0x35] = OpCode(pnuemonic='DEC (HL)', cycles=12, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value)))
    _op_code_lookup[0x36] = OpCode(pnuemonic='LD (HL),n', cycles=12, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), read_byte_at_pc(cpu_obj)))
    _op_code_lookup[0x38] = OpCode(pnuemonic='JR C, n', cycles=8, function=lambda cpu_obj: jr_cc_n(cpu_obj, cpu_obj.carry_flag, True))
    _op_code_lookup[0x39] = OpCode(pnuemonic='ADD HL, SP', cycles=8, function=lambda cpu_obj: add_nn(cpu_obj, cpu_obj.register_SP))
    _op_code_lookup[0x3A] = OpCode(pnuemonic='LD A,(HLD)', cycles=8, function=lambda cpu_obj: ldd_a_hl(cpu_obj))
    _op_code_lookup[0x3B] = OpCode(pnuemonic="DEC SP", cycles=8, function=lambda cpu_obj: dec_nn(cpu_obj, cpu_obj.register_SP))
    _op_code_lookup[0x3C] = OpCode(pnuemonic='INC A', cycles=4, function=lambda cpu_obj: inc_n(cpu_obj, cpu_obj.register_A))
    _op_code_lookup[0x3D] = OpCode(pnuemonic='DEC A', cycles=4, function=lambda cpu_obj: dec_n(cpu_obj, cpu_obj.register_A))
    _op_code_lookup[0x3E] = OpCode(pnuemonic='LD A,#', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, read_byte_at_pc(cpu_obj)))
    
    #4x
    _op_code_lookup[0x40] = OpCode(pnuemonic='LD B,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_B))
    _op_code_lookup[0x41] = OpCode(pnuemonic='LD B,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_C))
    _op_code_lookup[0x42] = OpCode(pnuemonic='LD B,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_D))
    _op_code_lookup[0x43] = OpCode(pnuemonic='LD B,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_E))
    _op_code_lookup[0x44] = OpCode(pnuemonic='LD B,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_H))
    _op_code_lookup[0x45] = OpCode(pnuemonic='LD B,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, cpu_obj.register_L))
    _op_code_lookup[0x46] = OpCode(pnuemonic='LD B,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_B, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))


    _op_code_lookup[0x48] = OpCode(pnuemonic='LD C,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_B))
    _op_code_lookup[0x49] = OpCode(pnuemonic='LD C,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_C))
    _op_code_lookup[0x4A] = OpCode(pnuemonic='LD C,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_D))
    _op_code_lookup[0x4B] = OpCode(pnuemonic='LD C,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_E))
    _op_code_lookup[0x4C] = OpCode(pnuemonic='LD C,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_H))
    _op_code_lookup[0x4D] = OpCode(pnuemonic='LD C,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, cpu_obj.register_L))
    _op_code_lookup[0x4E] = OpCode(pnuemonic='LD C,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_C, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))

    _op_code_lookup[0x47] = OpCode(pnuemonic='LD B,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x4F] = OpCode(pnuemonic='LD C,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_C))


    
    #5x
    _op_code_lookup[0x50] = OpCode(pnuemonic='LD D,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_B))
    _op_code_lookup[0x51] = OpCode(pnuemonic='LD D,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_C))
    _op_code_lookup[0x52] = OpCode(pnuemonic='LD D,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_D))
    _op_code_lookup[0x53] = OpCode(pnuemonic='LD D,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_E))
    _op_code_lookup[0x54] = OpCode(pnuemonic='LD D,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_H))
    _op_code_lookup[0x55] = OpCode(pnuemonic='LD D,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, cpu_obj.register_L))
    _op_code_lookup[0x56] = OpCode(pnuemonic='LD D,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_D, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))

    _op_code_lookup[0x58] = OpCode(pnuemonic='LD E,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_B))
    _op_code_lookup[0x59] = OpCode(pnuemonic='LD E,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_C))
    _op_code_lookup[0x5A] = OpCode(pnuemonic='LD E,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_D))
    _op_code_lookup[0x5B] = OpCode(pnuemonic='LD E,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_E))
    _op_code_lookup[0x5C] = OpCode(pnuemonic='LD E,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_H))
    _op_code_lookup[0x5D] = OpCode(pnuemonic='LD E,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, cpu_obj.register_L))
    _op_code_lookup[0x5E] = OpCode(pnuemonic='LD E,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_E, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))



    _op_code_lookup[0x57] = OpCode(pnuemonic='LD D,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x5F] = OpCode(pnuemonic='LD E,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_E))

    #6x

    _op_code_lookup[0x60] = OpCode(pnuemonic='LD H,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_B))
    _op_code_lookup[0x61] = OpCode(pnuemonic='LD H,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_C))
    _op_code_lookup[0x62] = OpCode(pnuemonic='LD H,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_D))
    _op_code_lookup[0x63] = OpCode(pnuemonic='LD H,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_E))
    _op_code_lookup[0x64] = OpCode(pnuemonic='LD H,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_H))
    _op_code_lookup[0x65] = OpCode(pnuemonic='LD H,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, cpu_obj.register_L))
    _op_code_lookup[0x66] = OpCode(pnuemonic='LD H,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_H, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))

    _op_code_lookup[0x67] = OpCode(pnuemonic='LD H,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_H))
    
    _op_code_lookup[0x68] = OpCode(pnuemonic='LD L,B', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_B))
    _op_code_lookup[0x69] = OpCode(pnuemonic='LD L,C', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_C))
    _op_code_lookup[0x6A] = OpCode(pnuemonic='LD L,D', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_D))
    _op_code_lookup[0x6B] = OpCode(pnuemonic='LD L,E', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_E))
    _op_code_lookup[0x6C] = OpCode(pnuemonic='LD L,H', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_H))
    _op_code_lookup[0x6D] = OpCode(pnuemonic='LD L,L', cycles=4, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, cpu_obj.register_L))
    _op_code_lookup[0x6E] = OpCode(pnuemonic='LD L,(HL)', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, cpu_obj.register_L, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    
    
    
    
    _op_code_lookup[0x6F] = OpCode(pnuemonic='LD L,A', cycles=4, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.register_L))

    #7x
    _op_code_lookup[0x70] = OpCode(pnuemonic='LD (HL),B', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_B))
    _op_code_lookup[0x71] = OpCode(pnuemonic='LD (HL),C', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_C))
    _op_code_lookup[0x72] = OpCode(pnuemonic='LD (HL),D', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_D))
    _op_code_lookup[0x73] = OpCode(pnuemonic='LD (HL),E', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_E))
    _op_code_lookup[0x74] = OpCode(pnuemonic='LD (HL),H', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_H))
    _op_code_lookup[0x75] = OpCode(pnuemonic='LD (HL),L', cycles=8, function=lambda cpu_obj: ld_reg2_into_reg1(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), cpu_obj.register_L))
    _op_code_lookup[0x76] = OpCode(pnuemonic="HALT", cycles=4, function= lambda cpu_obj: halt(cpu_obj))
    _op_code_lookup[0x77] = OpCode(pnuemonic='LD (HL),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value)))
    _op_code_lookup[0x78] = OpCode(pnuemonic='LD A,B', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x79] = OpCode(pnuemonic='LD A,C', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x7A] = OpCode(pnuemonic='LD A,D', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x7B] = OpCode(pnuemonic='LD A,E', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x7C] = OpCode(pnuemonic='LD A,H', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x7D] = OpCode(pnuemonic='LD A,L', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x7E] = OpCode(pnuemonic='LD A,(HL)', cycles=8, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(cpu_obj.register_HL.value)))
    _op_code_lookup[0x7F] = OpCode(pnuemonic='LD A,A', cycles=4, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.register_A))
    

    #8x
    _op_code_lookup[0x80] = OpCode(pnuemonic="ADD A,B", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x81] = OpCode(pnuemonic="ADD A,C", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x82] = OpCode(pnuemonic="ADD A,D", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x83] = OpCode(pnuemonic="ADD A,E", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x84] = OpCode(pnuemonic="ADD A,H", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x85] = OpCode(pnuemonic="ADD A,L", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x86] = OpCode(pnuemonic="ADD A,(HL)", cycles=8, function= lambda cpu_obj: add_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0x87] = OpCode(pnuemonic="ADD A,A", cycles=4, function= lambda cpu_obj: add_n(cpu_obj, cpu_obj.register_A))
    _op_code_lookup[0x88] = OpCode(pnuemonic="ADC A,B", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x89] = OpCode(pnuemonic="ADC A,C", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x8A] = OpCode(pnuemonic="ADC A,D", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x8B] = OpCode(pnuemonic="ADC A,E", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x8C] = OpCode(pnuemonic="ADC A,H", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x8D] = OpCode(pnuemonic="ADC A,L", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x8E] = OpCode(pnuemonic="ADC A,(HL)", cycles=8, function= lambda cpu_obj: adc_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0x8F] = OpCode(pnuemonic="ADC A,A", cycles=4, function= lambda cpu_obj: adc_n(cpu_obj, cpu_obj.register_A))

    #9x
    _op_code_lookup[0x90] = OpCode(pnuemonic="SUB B", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0x91] = OpCode(pnuemonic="SUB C", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0x92] = OpCode(pnuemonic="SUB D", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0x93] = OpCode(pnuemonic="SUB E", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0x94] = OpCode(pnuemonic="SUB H", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0x95] = OpCode(pnuemonic="SUB L", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0x96] = OpCode(pnuemonic="SUB (HL)", cycles=8, function= lambda cpu_obj: sub_n(cpu_obj, read_byte_from_address_from_register(cpu_obj,cpu_obj.register_HL)))
    _op_code_lookup[0x97] = OpCode(pnuemonic="SUB A", cycles=4, function= lambda cpu_obj: sub_n(cpu_obj, cpu_obj.register_A))

    #Ax
    _op_code_lookup[0xA0] = OpCode(pnuemonic='AND B', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0xA1] = OpCode(pnuemonic='AND C', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0xA2] = OpCode(pnuemonic='AND D', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0xA3] = OpCode(pnuemonic='AND E', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0xA4] = OpCode(pnuemonic='AND H', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0xA5] = OpCode(pnuemonic='AND L', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0xA6] = OpCode(pnuemonic='AND (HL)', cycles=8, function=lambda cpu_obj: and_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0xA7] = OpCode(pnuemonic='AND a', cycles=4, function=lambda cpu_obj: and_n(cpu_obj, cpu_obj.register_A))
    _op_code_lookup[0xA8] = OpCode(pnuemonic='XOR b', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0xA9] = OpCode(pnuemonic='XOR c', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0xAA] = OpCode(pnuemonic='XOR d', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0xAB] = OpCode(pnuemonic='XOR e', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0xAC] = OpCode(pnuemonic='XOR h', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0xAD] = OpCode(pnuemonic='XOR L', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0xAE] = OpCode(pnuemonic='XOR (HL)', cycles=8, function=lambda cpu_obj: xor_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0xAF] = OpCode(pnuemonic='XOR a', cycles=4, function=lambda cpu_obj: xor_n(cpu_obj, cpu_obj.register_A))

    #Bx
    _op_code_lookup[0xB0] = OpCode(pnuemonic='OR B', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0xB1] = OpCode(pnuemonic='OR C', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0xB2] = OpCode(pnuemonic='OR D', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0xB3] = OpCode(pnuemonic='OR E', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0xB4] = OpCode(pnuemonic='OR H', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0xB5] = OpCode(pnuemonic='OR L', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0xB6] = OpCode(pnuemonic='OR (HL)', cycles=8, function=lambda cpu_obj: or_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0xB7] = OpCode(pnuemonic='OR A', cycles=4, function=lambda cpu_obj: or_n(cpu_obj, cpu_obj.register_A))

    _op_code_lookup[0xB8] = OpCode(pnuemonic='CP B', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_B))
    _op_code_lookup[0xB9] = OpCode(pnuemonic='CP C', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_C))
    _op_code_lookup[0xBA] = OpCode(pnuemonic='CP D', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_D))
    _op_code_lookup[0xBB] = OpCode(pnuemonic='CP E', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_E))
    _op_code_lookup[0xBC] = OpCode(pnuemonic='CP H', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_H))
    _op_code_lookup[0xBD] = OpCode(pnuemonic='CP L', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_L))
    _op_code_lookup[0xBE] = OpCode(pnuemonic='CP (HL)', cycles=8, function=lambda cpu_obj: cp_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _op_code_lookup[0xBF] = OpCode(pnuemonic='CP A', cycles=4, function=lambda cpu_obj: cp_n(cpu_obj, cpu_obj.register_A))


    #Cx
    _op_code_lookup[0xC0] = OpCode(pnuemonic='RET NZ', cycles=8, function=lambda cpu_obj: ret_conditional(cpu_obj, cpu_obj.zero_flag, False, 20))
    _op_code_lookup[0xC1] = OpCode(pnuemonic='POP BC', cycles=12, function=lambda cpu_obj: pop(cpu_obj, cpu_obj.register_BC))
    _op_code_lookup[0xC2] = OpCode(pnuemonic='JP NZ,nn', cycles=16, function=lambda cpu_obj: jp_nn(cpu_obj, cpu_obj.zero_flag, False))
    _op_code_lookup[0xC3] = OpCode(pnuemonic='JP nn', cycles=16, function=lambda cpu_obj: jp_n(cpu_obj))
    _op_code_lookup[0xC4] = OpCode(pnuemonic='CALL NZ,nn', cycles=12,function= lambda cpu_obj: call_cc_nn(cpu_obj, cpu_obj.zero_flag, False))
    _op_code_lookup[0xC5] = OpCode(pnuemonic='PUSH BC', cycles=16, function=lambda cpu_obj: push(cpu_obj, cpu_obj.register_BC))
    _op_code_lookup[0xC6] = OpCode(pnuemonic="ADD A,#", cycles=8, function= lambda cpu_obj: add_n(cpu_obj, read_byte_at_pc(cpu_obj)))
    _op_code_lookup[0xC7] = OpCode(pnuemonic='RST 00H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0000)))
    _op_code_lookup[0xC8] = OpCode(pnuemonic='RET Z', cycles=8, function=lambda cpu_obj: ret_conditional(cpu_obj, cpu_obj.zero_flag, True, 20))
    _op_code_lookup[0xC9] = OpCode(pnuemonic='RET', cycles=8, function=lambda cpu_obj: ret(cpu_obj))
    _op_code_lookup[0xCA] = OpCode(pnuemonic='JP Z,nn', cycles=16, function=lambda cpu_obj: jp_nn(cpu_obj, cpu_obj.zero_flag, True))
    _op_code_lookup[0xCE] = OpCode(pnuemonic="ADC A,#", cycles=8, function= lambda cpu_obj: adc_n(cpu_obj, read_byte_at_pc(cpu_obj)))

    
    #any incoming CB instructions are re-routed before being looked up thus this entry will never be executed
    _op_code_lookup[0xCB] = OpCode(pnuemonic='CB PREFIX INSTRUCTION (DUMMY ENTRY)', cycles=0, function= None)
    _op_code_lookup[0xCC] = OpCode(pnuemonic='CALL Z,nn', cycles=12,function= lambda cpu_obj: call_cc_nn(cpu_obj, cpu_obj.zero_flag, True))
    _op_code_lookup[0xCD] = OpCode(pnuemonic='CALL nn', cycles=12, function=lambda cpu_obj: call_nn(cpu_obj))
    _op_code_lookup[0xCF] = OpCode(pnuemonic='RST 08H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0008)))


    #Dx
    _op_code_lookup[0xD0] = OpCode(pnuemonic='RET NC', cycles=8, function=lambda cpu_obj: ret_conditional(cpu_obj, cpu_obj.carry_flag, False, 20))
    _op_code_lookup[0xD1] = OpCode(pnuemonic='POP DE', cycles=12, function=lambda cpu_obj: pop(cpu_obj, cpu_obj.register_DE))
    _op_code_lookup[0xD2] = OpCode(pnuemonic='JP NC,nn', cycles=12, function=lambda cpu_obj: jp_nn(cpu_obj, cpu_obj.carry_flag, False))
    _op_code_lookup[0xD4] = OpCode(pnuemonic='CALL NC,nn', cycles=12,function= lambda cpu_obj: call_cc_nn(cpu_obj, cpu_obj.carry_flag, False))
    _op_code_lookup[0xD5] = OpCode(pnuemonic='PUSH DE', cycles=16, function=lambda cpu_obj: push(cpu_obj, cpu_obj.register_DE))
    _op_code_lookup[0xD6] = OpCode(pnuemonic="SUB #", cycles=8, function= lambda cpu_obj: sub_n(cpu_obj, read_byte_at_pc(cpu_obj)))
    _op_code_lookup[0xD7] = OpCode(pnuemonic='RST 10H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0010)))
    _op_code_lookup[0xD8] = OpCode(pnuemonic='RET C', cycles=8, function=lambda cpu_obj: ret_conditional(cpu_obj, cpu_obj.carry_flag, True, 20))
    _op_code_lookup[0xD9] = OpCode(pnuemonic='RETI', cycles=8, function=lambda cpu_obj: reti(cpu_obj))
    _op_code_lookup[0xDA] = OpCode(pnuemonic='JP C,nn', cycles=12, function=lambda cpu_obj: jp_nn(cpu_obj, cpu_obj.carry_flag, True))
    _op_code_lookup[0xDC] = OpCode(pnuemonic='CALL Z,nn', cycles=12,function= lambda cpu_obj: call_cc_nn(cpu_obj, cpu_obj.carry_flag, True))
    _op_code_lookup[0xDF] = OpCode(pnuemonic='RST 18H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0018)))

    #Ex
    #TODO: ld_A_into_register shouldn't have this fudge with program counter.
    _op_code_lookup[0xE0] = OpCode(pnuemonic='LDH (a8),A', cycles=12, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(0xFF00 + read_byte_at_pc(cpu_obj).value)))
    _op_code_lookup[0xE1] = OpCode(pnuemonic='POP HL', cycles=12, function=lambda cpu_obj: pop(cpu_obj, cpu_obj.register_HL))
    _op_code_lookup[0xE2] = OpCode(pnuemonic='LD ($FF00+C),A', cycles=8, function=lambda cpu_obj: ld_A_into_register(cpu_obj, cpu_obj.bus.read(0xFF00 + cpu_obj.register_C.value)))
    _op_code_lookup[0xE5] = OpCode(pnuemonic='PUSH HL', cycles=16, function=lambda cpu_obj: push(cpu_obj, cpu_obj.register_HL))
    _op_code_lookup[0xE6] = OpCode(pnuemonic='AND #', cycles=8, function=lambda cpu_obj: and_n(cpu_obj, read_byte_at_pc(cpu_obj)))
    _op_code_lookup[0xE7] = OpCode(pnuemonic='RST 20H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0020)))
    
    _op_code_lookup[0xE9] = OpCode(pnuemonic='JP (HL)', cycles=4, function=lambda cpu_obj: jp_hl(cpu_obj))
    ##TODO: not test - check on this
    _op_code_lookup[0xEA] = OpCode(pnuemonic='LD (nn),A', cycles=16, function=lambda cpu_obj: ld_A_into_register(cpu_obj, get_immediate_address_value(cpu_obj)))
    _op_code_lookup[0xEF] = OpCode(pnuemonic='RST 28H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0028)))
    _op_code_lookup[0xEE] = OpCode(pnuemonic='XOR #', cycles=8, function=lambda cpu_obj: xor_n(cpu_obj, read_byte_at_pc(cpu_obj)))

    

    #Fx

    _op_code_lookup[0xF0] = OpCode(pnuemonic='LDH A,(a8)', cycles=12, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, cpu_obj.bus.read(0xFF00 + read_byte_at_pc(cpu_obj).value)))
    _op_code_lookup[0xF1] = OpCode(pnuemonic='POP AF', cycles=12, function=lambda cpu_obj: pop(cpu_obj, cpu_obj.register_AF))
    _op_code_lookup[0xF5] = OpCode(pnuemonic='PUSH AF', cycles=16, function=lambda cpu_obj: push(cpu_obj, cpu_obj.register_AF))
    _op_code_lookup[0xF6] = OpCode(pnuemonic='OR #', cycles=8, function=lambda cpu_obj: or_n(cpu_obj, read_byte_at_pc(cpu_obj)))

    _op_code_lookup[0xF7] = OpCode(pnuemonic='RST 30H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0030)))
    _op_code_lookup[0xF8] = OpCode(pnuemonic='LD HL,SP+r8', cycles=12, function=lambda cpu_obj: ld_hl_sp(cpu_obj))
    _op_code_lookup[0xFA] = OpCode(pnuemonic='LD A,(nn)', cycles=16, function=lambda cpu_obj: ld_val_into_register_a(cpu_obj, get_immediate_address_value(cpu_obj)))
    _op_code_lookup[0xF3] = OpCode(pnuemonic='DI', cycles=4, function=lambda cpu_obj: di(cpu_obj))
    _op_code_lookup[0xFB] = OpCode(pnuemonic='EI', cycles=4, function=lambda cpu_obj: ei(cpu_obj))

    _op_code_lookup[0xFE] = OpCode(pnuemonic='CP #', cycles=8, function=lambda cpu_obj: cp_n(cpu_obj, read_byte_at_pc(cpu_obj)))
    _op_code_lookup[0xFF] = OpCode(pnuemonic='RST 38H', cycles=32, function=lambda cpu_obj: restart(cpu_obj, LongInt(0x0038)))
    
    #CB code table

    #1x
    _cb_code_lookup[0x18] = OpCode(pnuemonic="RR B", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_B))
    _cb_code_lookup[0x19] = OpCode(pnuemonic="RR C", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_C))
    _cb_code_lookup[0x1A] = OpCode(pnuemonic="RR D", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_D))
    _cb_code_lookup[0x1B] = OpCode(pnuemonic="RR E", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_E))
    _cb_code_lookup[0x1C] = OpCode(pnuemonic="RR H", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_H))
    _cb_code_lookup[0x1D] = OpCode(pnuemonic="RR L", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_L))
    _cb_code_lookup[0x1E] = OpCode(pnuemonic="RR (HL)", cycles=16, function=lambda cpu_obj:rr_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _cb_code_lookup[0x1F] = OpCode(pnuemonic="RR A", cycles=8, function=lambda cpu_obj:rr_n(cpu_obj, cpu_obj.register_A))

    #2x
    _cb_code_lookup[0x20] = OpCode(pnuemonic='SLA B', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_B))
    _cb_code_lookup[0x21] = OpCode(pnuemonic='SLA C', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_C))
    _cb_code_lookup[0x22] = OpCode(pnuemonic='SLA D', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_D))
    _cb_code_lookup[0x23] = OpCode(pnuemonic='SLA E', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_E))
    _cb_code_lookup[0x24] = OpCode(pnuemonic='SLA H', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_H))
    _cb_code_lookup[0x25] = OpCode(pnuemonic='SLA L', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_L))

    _cb_code_lookup[0x26] = OpCode(pnuemonic='SLA (HL)', cycles= 16, function= lambda cpu_obj: sla_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _cb_code_lookup[0x27] = OpCode(pnuemonic='SLA A', cycles= 8, function= lambda cpu_obj: sla_n(cpu_obj, cpu_obj.register_A))

    #3x
    _cb_code_lookup[0x30] = OpCode(pnuemonic='CB SWAP B', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_B))
    _cb_code_lookup[0x31] = OpCode(pnuemonic='CB SWAP C', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_C))
    _cb_code_lookup[0x32] = OpCode(pnuemonic='CB SWAP D', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_D))
    _cb_code_lookup[0x33] = OpCode(pnuemonic='CB SWAP E', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_E))
    _cb_code_lookup[0x34] = OpCode(pnuemonic='CB SWAP H', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_H))
    _cb_code_lookup[0x35] = OpCode(pnuemonic='CB SWAP L', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_L))
    #FIXME: the timing for this operation is disputed
    _cb_code_lookup[0x36] = OpCode(pnuemonic='CB SWAP (HL)', cycles= 16, function= lambda cpu_obj: swap(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _cb_code_lookup[0x37] = OpCode(pnuemonic='CB SWAP A', cycles= 8, function= lambda cpu_obj: swap(cpu_obj, cpu_obj.register_A))
    _cb_code_lookup[0x38] = OpCode(pnuemonic='SRL B', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_B))
    _cb_code_lookup[0x39] = OpCode(pnuemonic='SRL C', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_C))
    _cb_code_lookup[0x3A] = OpCode(pnuemonic='SRL D', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_D))
    _cb_code_lookup[0x3B] = OpCode(pnuemonic='SRL E', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_E))
    _cb_code_lookup[0x3C] = OpCode(pnuemonic='SRL H', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_H))
    _cb_code_lookup[0x3D] = OpCode(pnuemonic='SRL L', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_L))
    _cb_code_lookup[0x3E] = OpCode(pnuemonic='SRL (HL)', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL)))
    _cb_code_lookup[0x3F] = OpCode(pnuemonic='SRL A', cycles= 8, function= lambda cpu_obj: srl_n(cpu_obj, cpu_obj.register_A))
    #4x
    _cb_code_lookup[0x40] = OpCode(pnuemonic="BIT 0,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,0))
    _cb_code_lookup[0x41] = OpCode(pnuemonic="BIT 0,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,0))
    _cb_code_lookup[0x42] = OpCode(pnuemonic="BIT 0,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,0))
    _cb_code_lookup[0x43] = OpCode(pnuemonic="BIT 0,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,0))
    _cb_code_lookup[0x44] = OpCode(pnuemonic="BIT 0,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,0))
    _cb_code_lookup[0x45] = OpCode(pnuemonic="BIT 0,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,0))
    _cb_code_lookup[0x46] = OpCode(pnuemonic='BIT 0,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 0))
    _cb_code_lookup[0x47] = OpCode(pnuemonic="BIT 0,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,0))

    _cb_code_lookup[0x48] = OpCode(pnuemonic="BIT 1,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,1))
    _cb_code_lookup[0x49] = OpCode(pnuemonic="BIT 1,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,1))
    _cb_code_lookup[0x4A] = OpCode(pnuemonic="BIT 1,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,1))
    _cb_code_lookup[0x4B] = OpCode(pnuemonic="BIT 1,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,1))
    _cb_code_lookup[0x4C] = OpCode(pnuemonic="BIT 1,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,1))
    _cb_code_lookup[0x4D] = OpCode(pnuemonic="BIT 1,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,1))
    _cb_code_lookup[0x4E] = OpCode(pnuemonic='BIT 1,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 1))
    _cb_code_lookup[0x4F] = OpCode(pnuemonic="BIT 1,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,1))

    _cb_code_lookup[0x50] = OpCode(pnuemonic="BIT 2,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,2))
    _cb_code_lookup[0x51] = OpCode(pnuemonic="BIT 2,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,2))
    _cb_code_lookup[0x52] = OpCode(pnuemonic="BIT 2,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,2))
    _cb_code_lookup[0x53] = OpCode(pnuemonic="BIT 2,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,2))
    _cb_code_lookup[0x54] = OpCode(pnuemonic="BIT 2,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,2))
    _cb_code_lookup[0x55] = OpCode(pnuemonic="BIT 2,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,2))
    _cb_code_lookup[0x56] = OpCode(pnuemonic='BIT 2,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 2))
    _cb_code_lookup[0x57] = OpCode(pnuemonic="BIT 2,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,2))

    _cb_code_lookup[0x58] = OpCode(pnuemonic="BIT 3,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,3))
    _cb_code_lookup[0x59] = OpCode(pnuemonic="BIT 3,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,3))
    _cb_code_lookup[0x5A] = OpCode(pnuemonic="BIT 3,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,3))
    _cb_code_lookup[0x5B] = OpCode(pnuemonic="BIT 3,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,3))
    _cb_code_lookup[0x5C] = OpCode(pnuemonic="BIT 3,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,3))
    _cb_code_lookup[0x5D] = OpCode(pnuemonic="BIT 3,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,3))
    _cb_code_lookup[0x5E] = OpCode(pnuemonic='BIT 3,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 3))
    _cb_code_lookup[0x5F] = OpCode(pnuemonic="BIT 3,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,3))



    _cb_code_lookup[0x60] = OpCode(pnuemonic="BIT 4,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,4))
    _cb_code_lookup[0x61] = OpCode(pnuemonic="BIT 4,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,4))
    _cb_code_lookup[0x62] = OpCode(pnuemonic="BIT 4,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,4))
    _cb_code_lookup[0x63] = OpCode(pnuemonic="BIT 4,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,4))
    _cb_code_lookup[0x64] = OpCode(pnuemonic="BIT 4,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,4))
    _cb_code_lookup[0x65] = OpCode(pnuemonic="BIT 4,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,4))
    _cb_code_lookup[0x66] = OpCode(pnuemonic='BIT 4,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 4))
    _cb_code_lookup[0x67] = OpCode(pnuemonic="BIT 4,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,4))

    _cb_code_lookup[0x68] = OpCode(pnuemonic="BIT 5,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,5))
    _cb_code_lookup[0x69] = OpCode(pnuemonic="BIT 5,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,5))
    _cb_code_lookup[0x6A] = OpCode(pnuemonic="BIT 5,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,5))
    _cb_code_lookup[0x6B] = OpCode(pnuemonic="BIT 5,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,5))
    _cb_code_lookup[0x6C] = OpCode(pnuemonic="BIT 5,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,5))
    _cb_code_lookup[0x6D] = OpCode(pnuemonic="BIT 5,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,5))
    _cb_code_lookup[0x6E] = OpCode(pnuemonic='BIT 5,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 5))
    _cb_code_lookup[0x6F] = OpCode(pnuemonic="BIT 5,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,5))



    _cb_code_lookup[0x70] = OpCode(pnuemonic="BIT 6,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,6))
    _cb_code_lookup[0x71] = OpCode(pnuemonic="BIT 6,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,6))
    _cb_code_lookup[0x72] = OpCode(pnuemonic="BIT 6,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,6))
    _cb_code_lookup[0x73] = OpCode(pnuemonic="BIT 6,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,6))
    _cb_code_lookup[0x74] = OpCode(pnuemonic="BIT 6,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,6))
    _cb_code_lookup[0x75] = OpCode(pnuemonic="BIT 6,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,6))
    _cb_code_lookup[0x76] = OpCode(pnuemonic='BIT 6,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 6))
    _cb_code_lookup[0x77] = OpCode(pnuemonic="BIT 6,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,6))

    _cb_code_lookup[0x78] = OpCode(pnuemonic="BIT 7,B",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_B,7))
    _cb_code_lookup[0x79] = OpCode(pnuemonic="BIT 7,C",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_C,7))
    _cb_code_lookup[0x7A] = OpCode(pnuemonic="BIT 7,D",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_D,7))
    _cb_code_lookup[0x7B] = OpCode(pnuemonic="BIT 7,E",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_E,7))
    _cb_code_lookup[0x7C] = OpCode(pnuemonic="BIT 7,H",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_H,7))
    _cb_code_lookup[0x7D] = OpCode(pnuemonic="BIT 7,L",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_L,7))
    _cb_code_lookup[0x7E] = OpCode(pnuemonic='BIT 7,(HL)', cycles= 12, function= lambda cpu_obj: bit_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 7))
    _cb_code_lookup[0x7F] = OpCode(pnuemonic="BIT 7,A",cycles=8, function=lambda cpu_obj: bit_b_r(cpu_obj, cpu_obj.register_A,7))
    #8x
    _cb_code_lookup[0x80] = OpCode(pnuemonic='RES 0,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 0))
    _cb_code_lookup[0x81] = OpCode(pnuemonic='RES 0,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 0))
    _cb_code_lookup[0x82] = OpCode(pnuemonic='RES 0,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 0))
    _cb_code_lookup[0x83] = OpCode(pnuemonic='RES 0,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 0))
    _cb_code_lookup[0x84] = OpCode(pnuemonic='RES 0,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 0))
    _cb_code_lookup[0x85] = OpCode(pnuemonic='RES 0,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 0))
    _cb_code_lookup[0x86] = OpCode(pnuemonic='RES 0,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj,cpu_obj.register_HL), 0))
    _cb_code_lookup[0x87] = OpCode(pnuemonic='RES 0,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 0))

    _cb_code_lookup[0x88] = OpCode(pnuemonic='RES 1,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 1))
    _cb_code_lookup[0x89] = OpCode(pnuemonic='RES 1,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 1))
    _cb_code_lookup[0x8A] = OpCode(pnuemonic='RES 1,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 1))
    _cb_code_lookup[0x8B] = OpCode(pnuemonic='RES 1,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 1))
    _cb_code_lookup[0x8C] = OpCode(pnuemonic='RES 1,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 1))
    _cb_code_lookup[0x8D] = OpCode(pnuemonic='RES 1,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 1))
    _cb_code_lookup[0x8E] = OpCode(pnuemonic='RES 1,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj,cpu_obj.register_HL), 1))
    _cb_code_lookup[0x8F] = OpCode(pnuemonic='RES 1,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 1))

    #9x
    _cb_code_lookup[0x90] = OpCode(pnuemonic='RES 2,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 2))
    _cb_code_lookup[0x91] = OpCode(pnuemonic='RES 2,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 2))
    _cb_code_lookup[0x92] = OpCode(pnuemonic='RES 2,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 2))
    _cb_code_lookup[0x93] = OpCode(pnuemonic='RES 2,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 2))
    _cb_code_lookup[0x94] = OpCode(pnuemonic='RES 2,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 2))
    _cb_code_lookup[0x95] = OpCode(pnuemonic='RES 2,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 2))
    _cb_code_lookup[0x96] = OpCode(pnuemonic='RES 2,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj.register_HL), 2))
    _cb_code_lookup[0x97] = OpCode(pnuemonic='RES 2,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 2))

    _cb_code_lookup[0x98] = OpCode(pnuemonic='RES 3,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 3))
    _cb_code_lookup[0x99] = OpCode(pnuemonic='RES 3,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 3))
    _cb_code_lookup[0x9A] = OpCode(pnuemonic='RES 3,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 3))
    _cb_code_lookup[0x9B] = OpCode(pnuemonic='RES 3,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 3))
    _cb_code_lookup[0x9C] = OpCode(pnuemonic='RES 3,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 3))
    _cb_code_lookup[0x9D] = OpCode(pnuemonic='RES 3,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 3))
    _cb_code_lookup[0x9E] = OpCode(pnuemonic='RES 3,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 3))
    _cb_code_lookup[0x9F] = OpCode(pnuemonic='RES 3,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 3))
    
    #Ax
    _cb_code_lookup[0xA0] = OpCode(pnuemonic='RES 4,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 4))
    _cb_code_lookup[0xA1] = OpCode(pnuemonic='RES 4,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 4))
    _cb_code_lookup[0xA2] = OpCode(pnuemonic='RES 4,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 4))
    _cb_code_lookup[0xA3] = OpCode(pnuemonic='RES 4,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 4))
    _cb_code_lookup[0xA4] = OpCode(pnuemonic='RES 4,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 4))
    _cb_code_lookup[0xA5] = OpCode(pnuemonic='RES 4,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 4))
    _cb_code_lookup[0xA6] = OpCode(pnuemonic='RES 4,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj.register_HL), 4))
    _cb_code_lookup[0xA7] = OpCode(pnuemonic='RES 4,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 4))

    _cb_code_lookup[0xA8] = OpCode(pnuemonic='RES 5,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 5))
    _cb_code_lookup[0xA9] = OpCode(pnuemonic='RES 5,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 5))
    _cb_code_lookup[0xAA] = OpCode(pnuemonic='RES 5,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 5))
    _cb_code_lookup[0xAB] = OpCode(pnuemonic='RES 5,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 5))
    _cb_code_lookup[0xAC] = OpCode(pnuemonic='RES 5,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 5))
    _cb_code_lookup[0xAD] = OpCode(pnuemonic='RES 5,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 5))
    _cb_code_lookup[0xAE] = OpCode(pnuemonic='RES 5,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj.register_HL), 5))
    _cb_code_lookup[0xAF] = OpCode(pnuemonic='RES 5,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 5))


    #bx
    _cb_code_lookup[0xB0] = OpCode(pnuemonic='RES 6,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 6))
    _cb_code_lookup[0xB1] = OpCode(pnuemonic='RES 6,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 6))
    _cb_code_lookup[0xB2] = OpCode(pnuemonic='RES 6,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 6))
    _cb_code_lookup[0xB3] = OpCode(pnuemonic='RES 6,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 6))
    _cb_code_lookup[0xB4] = OpCode(pnuemonic='RES 6,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 6))
    _cb_code_lookup[0xB5] = OpCode(pnuemonic='RES 6,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 6))
    _cb_code_lookup[0xB6] = OpCode(pnuemonic='RES 6,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj,cpu_obj.register_HL), 6))
    _cb_code_lookup[0xB7] = OpCode(pnuemonic='RES 6,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 6))

    _cb_code_lookup[0xB8] = OpCode(pnuemonic='RES 7,B', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_B, 7))
    _cb_code_lookup[0xB9] = OpCode(pnuemonic='RES 7,C', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_C, 7))
    _cb_code_lookup[0xBA] = OpCode(pnuemonic='RES 7,D', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_D, 7))
    _cb_code_lookup[0xBB] = OpCode(pnuemonic='RES 7,E', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_E, 7))
    _cb_code_lookup[0xBC] = OpCode(pnuemonic='RES 7,H', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_H, 7))
    _cb_code_lookup[0xBD] = OpCode(pnuemonic='RES 7,L', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_L, 7))
    _cb_code_lookup[0xBE] = OpCode(pnuemonic='RES 7,(HL)', cycles= 16, function= lambda cpu_obj: res_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj,cpu_obj.register_HL), 7))
    _cb_code_lookup[0xBF] = OpCode(pnuemonic='RES 7,A', cycles= 8, function= lambda cpu_obj: res_b_r(cpu_obj, cpu_obj.register_A, 7))

    #Cx
    _cb_code_lookup[0xC0] = OpCode(pnuemonic='SET 0,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 0))
    _cb_code_lookup[0xC1] = OpCode(pnuemonic='SET 0,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 0))
    _cb_code_lookup[0xC2] = OpCode(pnuemonic='SET 0,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 0))
    _cb_code_lookup[0xC3] = OpCode(pnuemonic='SET 0,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 0))
    _cb_code_lookup[0xC4] = OpCode(pnuemonic='SET 0,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 0))
    _cb_code_lookup[0xC5] = OpCode(pnuemonic='SET 0,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 0))
    _cb_code_lookup[0xC6] = OpCode(pnuemonic='SET 0,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 0))
    _cb_code_lookup[0xC7] = OpCode(pnuemonic='SET 0,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 0))

    _cb_code_lookup[0xC8] = OpCode(pnuemonic='SET 1,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 1))
    _cb_code_lookup[0xC9] = OpCode(pnuemonic='SET 1,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 1))
    _cb_code_lookup[0xCA] = OpCode(pnuemonic='SET 1,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 1))
    _cb_code_lookup[0xCB] = OpCode(pnuemonic='SET 1,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 1))
    _cb_code_lookup[0xCC] = OpCode(pnuemonic='SET 1,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 1))
    _cb_code_lookup[0xCD] = OpCode(pnuemonic='SET 1,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 1))
    _cb_code_lookup[0xCE] = OpCode(pnuemonic='SET 1,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 1))
    _cb_code_lookup[0xCF] = OpCode(pnuemonic='SET 1,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 1))

    _cb_code_lookup[0xD0] = OpCode(pnuemonic='SET 2,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 2))
    _cb_code_lookup[0xD1] = OpCode(pnuemonic='SET 2,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 2))
    _cb_code_lookup[0xD2] = OpCode(pnuemonic='SET 2,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 2))
    _cb_code_lookup[0xD3] = OpCode(pnuemonic='SET 2,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 2))
    _cb_code_lookup[0xD4] = OpCode(pnuemonic='SET 2,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 2))
    _cb_code_lookup[0xD5] = OpCode(pnuemonic='SET 2,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 2))
    _cb_code_lookup[0xD6] = OpCode(pnuemonic='SET 2,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 2))
    _cb_code_lookup[0xD7] = OpCode(pnuemonic='SET 2,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 2))

    _cb_code_lookup[0xD8] = OpCode(pnuemonic='SET 3,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 3))
    _cb_code_lookup[0xD9] = OpCode(pnuemonic='SET 3,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 3))
    _cb_code_lookup[0xDA] = OpCode(pnuemonic='SET 3,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 3))
    _cb_code_lookup[0xDB] = OpCode(pnuemonic='SET 3,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 3))
    _cb_code_lookup[0xDC] = OpCode(pnuemonic='SET 3,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 3))
    _cb_code_lookup[0xDD] = OpCode(pnuemonic='SET 3,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 3))
    _cb_code_lookup[0xDE] = OpCode(pnuemonic='SET 3,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 3))
    _cb_code_lookup[0xDF] = OpCode(pnuemonic='SET 3,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 3))

    _cb_code_lookup[0xE0] = OpCode(pnuemonic='SET 4,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 4))
    _cb_code_lookup[0xE1] = OpCode(pnuemonic='SET 4,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 4))
    _cb_code_lookup[0xE2] = OpCode(pnuemonic='SET 4,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 4))
    _cb_code_lookup[0xE3] = OpCode(pnuemonic='SET 4,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 4))
    _cb_code_lookup[0xE4] = OpCode(pnuemonic='SET 4,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 4))
    _cb_code_lookup[0xE5] = OpCode(pnuemonic='SET 4,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 4))
    _cb_code_lookup[0xE6] = OpCode(pnuemonic='SET 4,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 4))
    _cb_code_lookup[0xE7] = OpCode(pnuemonic='SET 4,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 4))

    _cb_code_lookup[0xE8] = OpCode(pnuemonic='SET 5,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 5))
    _cb_code_lookup[0xE9] = OpCode(pnuemonic='SET 5,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 5))
    _cb_code_lookup[0xEA] = OpCode(pnuemonic='SET 5,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 5))
    _cb_code_lookup[0xEB] = OpCode(pnuemonic='SET 5,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 5))
    _cb_code_lookup[0xEC] = OpCode(pnuemonic='SET 5,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 5))
    _cb_code_lookup[0xED] = OpCode(pnuemonic='SET 5,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 5))
    _cb_code_lookup[0xEE] = OpCode(pnuemonic='SET 5,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 5))
    _cb_code_lookup[0xEF] = OpCode(pnuemonic='SET 5,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 5))

    _cb_code_lookup[0xF0] = OpCode(pnuemonic='SET 6,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 6))
    _cb_code_lookup[0xF1] = OpCode(pnuemonic='SET 6,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 6))
    _cb_code_lookup[0xF2] = OpCode(pnuemonic='SET 6,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 6))
    _cb_code_lookup[0xF3] = OpCode(pnuemonic='SET 6,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 6))
    _cb_code_lookup[0xF4] = OpCode(pnuemonic='SET 6,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 6))
    _cb_code_lookup[0xF5] = OpCode(pnuemonic='SET 6,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 6))
    _cb_code_lookup[0xF6] = OpCode(pnuemonic='SET 6,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 6))
    _cb_code_lookup[0xF7] = OpCode(pnuemonic='SET 6,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 6))

    _cb_code_lookup[0xF8] = OpCode(pnuemonic='SET 7,B', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_B, 7))
    _cb_code_lookup[0xF9] = OpCode(pnuemonic='SET 7,C', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_C, 7))
    _cb_code_lookup[0xFA] = OpCode(pnuemonic='SET 7,D', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_D, 7))
    _cb_code_lookup[0xFB] = OpCode(pnuemonic='SET 7,E', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_E, 7))
    _cb_code_lookup[0xFC] = OpCode(pnuemonic='SET 7,F', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_F, 7))
    _cb_code_lookup[0xFD] = OpCode(pnuemonic='SET 7,H', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_H, 7))
    _cb_code_lookup[0xFE] = OpCode(pnuemonic='SET 7,L', cycles= 8, function= lambda cpu_obj: set_b_r(cpu_obj, cpu_obj.register_L, 7))
    _cb_code_lookup[0xFF] = OpCode(pnuemonic='SET 7,(HL)', cycles= 16, function= lambda cpu_obj: set_b_r(cpu_obj, read_byte_from_address_from_register(cpu_obj, cpu_obj.register_HL), 7))


    print("Op Code Table Implementation %", 100 - (_op_code_lookup.count(unknown_op_code)/ len(_op_code_lookup) * 100))
    print("CB Table Implementation %", 100 - (_cb_code_lookup.count(unknown_cb_code)/ len(_cb_code_lookup) * 100))
    sleep(1)
    print("Emulation begin")

    def decode_instruction(self,op_code:int)->OpCode:

        if op_code == 0xCB:
            return self.decode_cb_instruction()
        

        return self._op_code_lookup[op_code]

    def decode_cb_instruction(self)->OpCode:
        '''
            Performs a secondary lookup for any CB prefixed instructions
        
        '''

        op_code:int = read_byte_at_pc(self.parent_cpu).value
        
        return self._cb_code_lookup[op_code]
        