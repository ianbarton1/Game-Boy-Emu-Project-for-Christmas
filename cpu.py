
import sys
from time import sleep
from bus import Bus, read_byte_at_pc
from cpu_ops.control import push_current_pc_to_stack
from enums.ime_transition import IMETransition
from number.long_int import LongInt
from number.short_int import ShortInt
from op_code import OpCode
from op_code_table import OPCodeTable
from stack import push_to_stack





class CPU:
    

    def __init__(self, bus:Bus) -> None:
        self.program_counter:int = 0x100
        self.last_fetch_pc:int = 0x100
        self.instruction_count:int = 0
        self.stack_pointer:LongInt = LongInt(value=0x0000)
        self.bus:Bus = bus
        self.op_code:int = 0x00
        self.cb_code:int = 0x00
        self.inst_lookup = OPCodeTable(parent_cpu= self)
        self.last_instruction = OpCode(pnuemonic='???', cycles=4, function=lambda: print('run op'))
        self.cpu_is_halted:bool = False
        self.cpu_is_stopped:bool = False

        self.last_tick_was_active:bool = False
        
        self.ime_flag:bool = False
        self.ime_transition:IMETransition = IMETransition.IDLE

        self.clock_wait = 0

        self.register_AF = LongInt()
        self.register_BC = LongInt()
        self.register_DE = LongInt()


        self.register_A = ShortInt()
        self.register_B = ShortInt()
        self.register_C = ShortInt()
        self.register_D = ShortInt()
        self.register_E = ShortInt()
        
        self.register_F = ShortInt()
        
        self.register_HL = LongInt()
        self.register_H = ShortInt()
        self.register_L = ShortInt()

        #ppu registers
        self.register_LCDC = self.bus.read(0xFF40)

        

        self.init_cpu()


    def init_cpu(self):
        '''
            Set the initial register values based on https://bgb.bircd.org/pandocs.htm#powerupsequence

            AF=$01B0
            BC=$0013
            DE=$00D8
            HL=$014D
            Stack Pointer=$FFFE
            [$FF05] = $00   ; TIMA
            [$FF06] = $00   ; TMA
            [$FF07] = $00   ; TAC
            [$FF10] = $80   ; NR10
            [$FF11] = $BF   ; NR11
            [$FF12] = $F3   ; NR12
            [$FF14] = $BF   ; NR14
            [$FF16] = $3F   ; NR21
            [$FF17] = $00   ; NR22
            [$FF19] = $BF   ; NR24
            [$FF1A] = $7F   ; NR30
            [$FF1B] = $FF   ; NR31
            [$FF1C] = $9F   ; NR32
            [$FF1E] = $BF   ; NR33
            [$FF20] = $FF   ; NR41
            [$FF21] = $00   ; NR42
            [$FF22] = $00   ; NR43
            [$FF23] = $BF   ; NR30
            [$FF24] = $77   ; NR50
            [$FF25] = $F3   ; NR51
            [$FF26] = $F1-GB, $F0-SGB ; NR52
            [$FF40] = $91   ; LCDC
            [$FF42] = $00   ; SCY
            [$FF43] = $00   ; SCX
            [$FF45] = $00   ; LYC
            [$FF47] = $FC   ; BGP
            [$FF48] = $FF   ; OBP0
            [$FF49] = $FF   ; OBP1
            [$FF4A] = $00   ; WY
            [$FF4B] = $00   ; WX
            [$FFFF] = $00   ; IE
        
        '''
        self.register_AF.value = 0x01B0
        self.register_BC.value = 0x0013
        self.register_DE.value = 0x00D8
        self.register_HL.value = 0x01FD
        self.stack_pointer.value = 0xFFFE

        self.register_LCDC.value = 0x91

        self.interrupt_enable = self.bus.read(0xFFFF)
        self.interrupt_flag = self.bus.read(0xFF0F)

        self.dma_register = self.bus.read(0xFF46)
        self.dma_register.add_write_viewer(self.start_dma_transfer)
       
    
    @property
    def register_A(self)->ShortInt:
        return self.register_AF.high_byte
    
    @property
    def register_F(self)->ShortInt:
        return self.register_AF.low_byte
    
    @property
    def register_B(self)->ShortInt:
        return self.register_BC.high_byte
    
    @property
    def register_C(self)->ShortInt:
        return self.register_BC.low_byte
    
    @property
    def register_D(self)->ShortInt:
        return self.register_DE.high_byte
    
    @property
    def register_E(self)->ShortInt:
        return self.register_DE.low_byte
    
    
    @property
    def register_H(self)->ShortInt:
        return self.register_HL.high_byte

    @property
    def register_L(self)->ShortInt:
        return self.register_HL.low_byte
    
    @property
    def register_SP(self)->LongInt:
        return self.stack_pointer
    
    @register_SP.setter
    def register_SP(self):
        raise NotImplementedError("Not allowed to set register_SP directly.")
    





    @register_A.setter
    def register_A(self, new_value:int):
        self.register_AF.high_byte = new_value
    
    @register_F.setter
    def register_F(self, new_value:int):
        self.register_AF.low_byte = new_value
    
    @register_B.setter
    def register_B(self, new_value:int):
        self.register_BC.high_byte = new_value
    
    @register_C.setter
    def register_C(self, new_value:int):
        self.register_BC.low_byte = new_value
    
    @register_D.setter
    def register_D(self, new_value:int):
        self.register_DE.high_byte = new_value
    
    @register_E.setter
    def register_E(self, new_value:int):
        self.register_DE.low_byte = new_value
    
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
        return f"IC: {self.instruction_count},PC (current): {hex(self.program_counter)}, PC (at last fetch):{hex(self.last_fetch_pc)} OP_CODE:{hex(self.op_code)} {hex(self.cb_code) if self.op_code == 0xCB else ''}, INSTR:{self.last_instruction.pnuemonic}, CLOCKWAIT: {self.clock_wait},IE:{self.interrupt_enable},IF:{self.interrupt_flag}, A:{self.register_A},B:{self.register_B},C:{self.register_C},D:{self.register_D},E:{self.register_E},F:{self.register_F},H:{self.register_H},L:{self.register_L},AF:{self.register_AF},BC:{self.register_BC},DE:{self.register_DE},HL:{self.register_HL},SP:{self.stack_pointer}, Flags:Z:{int(self.zero_flag)},N:{int(self.subtract_flag)},H:{int(self.half_carry_flag)},C:{int(self.carry_flag)},IME:{self.ime_flag},FF24 {self.bus.read(0xFF24)},"
    
    def tick(self, tick_amount:int = 1):
        if self.clock_wait == 0:
            self.fire_interrupts()
        

        if self.clock_wait > 0:
            self.clock_wait -= 1
            self.last_tick_was_active = False
            return


        if self.cpu_is_halted or self.cpu_is_stopped:
            # print(self)
            return
                    
        # print(self.interrupt_enable,self.interrupt_flag,self.cpu_is_halted,self.ime_flag)
        self.last_tick_was_active = True
        
        self.last_fetch_pc = self.program_counter
        self.op_code = read_byte_at_pc(self).value

        if self.op_code == 0xCB:
            self.cb_code = self.bus.read(self.program_counter).value

        self.last_instruction = self.inst_lookup.decode_instruction(self.op_code)
        self.clock_wait = self.last_instruction.cycles

        
        self.instruction_count += tick_amount

        self.last_instruction.function(self)
        # print(f"LRA ({hex(self.bus.last_read_address)}):{self.bus.read(self.bus.last_read_address)}")

        #handle interrupt enable disable
        match self.ime_transition:
            case IMETransition.IDLE:
                pass
            case IMETransition.REQUEST_TO_OFF:
                self.ime_transition = IMETransition.TRANSITIONING_OFF
            case IMETransition.REQUEST_TO_ON:
                self.ime_transition = IMETransition.TRANSITIONING_ON
            case IMETransition.TRANSITIONING_ON:
                self.ime_transition = IMETransition.IDLE
                self.ime_flag = True
            case IMETransition.TRANSITIONING_OFF:
                self.ime_flag = False
                self.ime_transition = IMETransition.IDLE

    def fire_interrupts(self):
        '''
            Handle any interrupts that may need handling
        
        '''
        
        #if ime_flag is disabled we shall not handle any more interrupts
        if not self.ime_flag:
            return
        
        temp_interrupt = ShortInt(self.interrupt_enable.value & self.interrupt_flag.value)
        # print("CPU view ", id(self.bus.read(0xFF0F)),id(self.bus.read(0xFFFF)))
        # print(id(self.interrupt_flag), id(self.interrupt_enable))
        # print(self.interrupt_enable, self.interrupt_flag, temp_interrupt, temp_interrupt.value)
        # sleep(1)
        handler_address = 0x00

        if temp_interrupt.get_bit(bit_number=0) and not self.cpu_is_stopped:
            # print("V-Blank Interrupt")
            handler_address = 0x40
            self.interrupt_flag.write_bit(bit_number=0,bit=False)
        elif temp_interrupt.get_bit(bit_number=1) and not self.cpu_is_stopped:
            print("LCD STAT")
            handler_address = 0x48
            self.interrupt_flag.write_bit(bit_number=1,bit=False)
        elif temp_interrupt.get_bit(bit_number=2) and not self.cpu_is_stopped:
            print("Timer")
            handler_address = 0x50
            self.interrupt_flag.write_bit(bit_number=2,bit=False)
        elif temp_interrupt.get_bit(bit_number=3) and not self.cpu_is_stopped:
            print("Serial")
            handler_address = 0x58
            self.interrupt_flag.write_bit(bit_number=3,bit=False)
        elif temp_interrupt.get_bit(bit_number=4):
            print("Joypad")
            self.interrupt_flag.write_bit(bit_number=4,bit=False)
            handler_address = 0x60
        else:
            return

        self.ime_flag = False
        
        push_current_pc_to_stack(self)
        self.program_counter = handler_address
        self.clock_wait = 20
        self.cpu_is_halted = False
        self.cpu_is_stopped = False
    
    def start_dma_transfer(self):
        # print(self.dma_register)
        source_address = LongInt()
        source_address.high_byte = self.dma_register

        
        destination_address = LongInt(0xFE00)

        # print(source_address, destination_address)

        for offset in range(160):
            
            self.bus.write(destination_address.value + offset, self.bus.read(source_address.value + offset).value)
            # print(hex(source_address.value + offset), hex(destination_address.value + offset), hex(self.bus.read(source_address.value + offset).value),hex(self.bus.read(destination_address.value + offset).value))
