"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    ram = [None] * 1000 
    pc = 0
    registers = {}


    def __init__(self):
        """Construct a new CPU."""
        pass

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        f = open(str(filename) + ".ls8", "r")

        for line in f:
            intOfString = int(str(line), 2)
            self.ram[address] = intOfString
            address += 1

        # print(self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
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
        # print(self.ram)
        i = 0
        while i <= len(self.ram):
            if self.ram[i] is None:
                print("Skipping None")
                continue
            # print(self.ram[i])
            # #LDI
            # print(f"if {int(self.ram[i])} == {int(0b10000010)}" )
            if int(self.ram[i]) == int(0b10000010):
                # print("LDI")
                self.registers[self.ram[i + 1]] = self.ram[i + 2]
                i += 2

            #print
            # print(f"if {int(self.ram[i])} == {int(0b01000111)}" )
            if int(self.ram[i]) == int(0b01000111):
                # print("Print")
                print(str(int(self.registers[self.ram[i + 1]])))
                i += 1

            if int(self.ram[i]) == int(0b10100010):
                # print("Mul")
                self.alu("MUL", self.ram[i + 1], self.ram[i + 2])
                i += 3
                # print("address after mul")
                # print(self.ram[i])
                continue

            #HLT
            if int(self.ram[i]) == int(0b00000001):
                # print("HLT")
                return

            i += 1

