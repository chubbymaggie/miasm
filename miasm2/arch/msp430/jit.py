from miasm2.jitter.jitload import jitter
from miasm2.core import asmbloc
from miasm2.core.utils import *
from miasm2.arch.msp430.sem import ir_msp430

import logging

log = logging.getLogger('jit_msp430')
hnd = logging.StreamHandler()
hnd.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))
log.addHandler(hnd)
log.setLevel(logging.CRITICAL)

class jitter_msp430(jitter):

    def __init__(self, *args, **kwargs):
        sp = asmbloc.asm_symbol_pool()
        jitter.__init__(self, ir_msp430(sp), *args, **kwargs)
        self.vm.set_little_endian()

    def push_uint16_t(self, v):
        regs = self.cpu.get_gpreg()
        regs['SP'] -= 2
        self.cpu.set_gpreg(regs)
        self.vm.set_mem(regs['SP'], pck16(v))

    def pop_uint16_t(self):
        regs = self.cpu.get_gpreg()
        x = upck16(self.vm.get_mem(regs['SP'], 2))
        regs['SP'] += 2
        self.cpu.set_gpreg(regs)
        return x

    def get_stack_arg(self, n):
        regs = self.cpu.get_gpreg()
        x = upck16(self.vm.get_mem(regs['SP'] + 2 * n, 2))
        return x

    def init_run(self, *args, **kwargs):
        jitter.init_run(self, *args, **kwargs)
        self.cpu.PC = self.pc

