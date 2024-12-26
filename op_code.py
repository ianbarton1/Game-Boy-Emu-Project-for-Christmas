class OpCode:
    pnuemonic = '???'
    cycles = 4
    function:callable = lambda a,b: print('x')

    def __init__(self, pnuemonic, cycles, function) -> None:
        self.pnuemonic = pnuemonic
        self.cycles = cycles
        self.function = function