from bus import Bus
from number.long_int import LongInt


class Timer:
    def __init__(self, bus:Bus):
        self.bus = bus
        self.divider_register = LongInt()

        self.divider_register.high_byte = self.bus.read(0xFF04)

        self.divider_register.high_byte.add_write_viewer(self.reset_register)

        self.timer_counter = self.bus.read(0xFF05)
        self.timer_modulo = self.bus.read(0xFF06)
        self.time_control = self.bus.read(0xFF07)
        self.time_control.add_write_viewer(self.change_state)

        self.interrupt_register = self.bus.read(0xFF0F)

        self.divider_register_wait:int = 256

        self.clock_is_enabled = False

        self.clock_rates = {
            0: 1024,
            1: 16,
            2: 64,
            3: 256
        }

        # self.clock_rates = {
        #     0: 4096,
        #     1: 64,
        #     2: 256,
        #     3: 1024
        # }


        self.selected_clock_rate = 4096
        self.clock_tick:int = 0

        self.change_state()

    def reset_register(self):
        '''
            if the register located at 0xFF04 is written to then it should be reset back to 0
        
        '''
        self.divider_register.special_value = 0

    def change_state(self):
        self.clock_is_enabled = self.time_control.get_bit(bit_number=2)

        new_clock_rate = self.clock_rates[(int(self.time_control.get_bit(bit_number=1)) << 1) + int(self.time_control.get_bit(bit_number=0))]
        if new_clock_rate != self.selected_clock_rate:
            self.selected_clock_rate = new_clock_rate
            self.clock_tick = 0


    def tick(self, tick_rate:int = 1):
        '''
            Increments the timers and fires the interrupt when required
        
        '''
        self.divider_register_wait -= tick_rate

        if self.divider_register_wait <= 0:
            self.divider_register_wait = 256
            self.divider_register.special_value += 1

        if self.clock_is_enabled:
            self.clock_tick += 1
            if self.clock_tick > self.selected_clock_rate:
                self.clock_tick = 0
                
                self.timer_counter.value += 1

                if self.time_control.value == 0x00:
                    timer_overflow = True
                    self.timer_counter.value = self.timer_modulo.value

                    #request interrupt
                    self.interrupt_register.write_bit(bit_number=2, bit=True)
            
        
        


