from bus import Bus
from number.long_int import LongInt
from number.short_int import ShortInt
from op_code import OpCode
from op_code_table import OPCodeTable


class CPU:

    def __init__(self, bus:Bus) -> None:
        self.program_counter:int = 0x100
        self.stack_pointer:LongInt = LongInt(value=0x0000)
        self.bus:Bus = bus
        self.op_code:int = 0x00
        self.inst_lookup = OPCodeTable()
        self.last_instruction = OpCode(pnuemonic='???', cycles=4, function=lambda: print('run op'))
        
        self.clock_wait = 0

        self.register_A = ShortInt()
        self.register_B = ShortInt()
        self.register_C = ShortInt()
        self.register_D = ShortInt()
        self.register_E = ShortInt()
        
        self.register_F = ShortInt()
        
        self.register_HL = LongInt()
        self.register_H = ShortInt()
        self.register_L = ShortInt()

        


        self.register_S = ShortInt()
        self.register_P = ShortInt()

    @property
    def register_H(self)->ShortInt:
        return self.register_HL.high_byte

    @property
    def register_L(self)->ShortInt:
        return self.register_HL.low_byte
    
    @register_H.setter
    def register_H(self, new_value:int):
        self.register_HL.high_byte = new_value

    @register_L.setter
    def register_L(self, new_value:int):
        self.register_HL.low_byte = new_value

    @property
    def zero_flag(self)->bool:
        return self.register_F.get_bit(bit_number=7)
    
    @property
    def subtract_flag(self)->bool:
        return self.register_F.get_bit(bit_number=6)
    
    @property
    def half_carry_flag(self)->bool:
        return self.register_F.get_bit(bit_number=5)
    
    @property
    def carry_flag(self)->bool:
        return self.register_F.get_bit(bit_number=4)
    
    @property
    def register_S(self)->ShortInt:
        return self.stack_pointer.high_byte
    
    @property
    def register_P(self)->ShortInt:
        return self.stack_pointer.low_byte
    
    @register_S.setter
    def register_S(self, new_value:int):
        self.stack_pointer.high_byte.value = new_value
    
    @register_P.setter
    def register_P(self, new_value:int):
        self.stack_pointer.low_byte.value = new_value

    @zero_flag.setter
    def zero_flag(self, flag:bool)->None:
        return self.register_F.write_bit(bit_number=7,bit=flag)
    
    @subtract_flag.setter
    def subtract_flag(self,flag:bool)->None:
        return self.register_F.write_bit(bit_number=6,bit=flag)
    
    @half_carry_flag.setter
    def half_carry_flag(self,flag:bool)->None:
        return self.register_F.write_bit(bit_number=5,bit=flag)
    
    @carry_flag.setter
    def carry_flag(self,flag:bool)->None:
        return self.register_F.write_bit(bit_number=4,bit=flag)

    def __repr__(self) -> str:
        return f"PC: {hex(self.program_counter)}, OP_CODE:{hex(self.op_code)}, INSTR:{self.last_instruction.pnuemonic}, CLOCKWAIT: {self.clock_wait}, A:{self.register_A},B:{self.register_B},C:{self.register_C},D:{self.register_D},E:{self.register_E},F:{self.register_F},H:{self.register_H},L:{self.register_L},HL:{self.register_HL} Flags:Z:{int(self.zero_flag)},N:{int(self.subtract_flag)},H:{int(self.half_carry_flag)},C:{int(self.carry_flag)}"
    
    def tick(self):
        if self.clock_wait > 0:
            self.clock_wait -= 1

        if self.clock_wait > 0:
            return
        
        self.op_code = self.bus.read(self.program_counter).value
        self.last_instruction = self.inst_lookup.decode_instruction(self.op_code)
        self.clock_wait = self.last_instruction.cycles

        print(self)
        self.program_counter += 1

        
        self.last_instruction.function(self)
        
