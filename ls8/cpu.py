"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    ram = [None] * 1000 
    pc = 0
    registers = [None] * 8


    def __init__(self):
        """Construct a new CPU."""
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, pc):
        return self.ram[pc]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        for i in range(len(self.ram)):
            #LDI
            if self.ram[i] == 0b10000010:
                self.registers[int(self.ram[i + 1])] = self.ram[i + 2]

            #print
            if self.ram[i] == 0b01000111:
                print(str(int(self.registers[self.ram[i + 1] ])))

            #HLT
            if self.ram[i] == 0b00000001:
                return

