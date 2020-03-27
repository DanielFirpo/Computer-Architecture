"""CPU functionality."""

import sys

#Instruction codes
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

#Register Addresses
MAR = 0 #Memory Address Register, holds the memory address we're reading or writing
MDR = 1 #Memory Data Register, holds the value to write or the value just read
IR = 2 #Instruction Register, contains a copy of the currently executing instruction
PC = 5 #Program Counter, address of the currently executing instruction
FL = 4 #Flags, see below

IM = 3 #is reserved as the interrupt mask (IM)
IS = 6 #is reserved as the interrupt status (IS)
SP = 7#Stack Pointer, contains RAM index of current stack 

#RAM
#       top of RAM
# +-----------------------+
# | 255  I7 vector         |    Interrupt vector table
# | 254  I6 vector         |
# | 253  I5 vector         |
# | 252  I4 vector         |
# | 251  I3 vector         |
# | 250  I2 vector         |
# | 249  I1 vector         |
# | 248  I0 vector         |
# | 247  Reserved          |
# | 246  Reserved          |
# | 245  Reserved          |
# | 244  Key pressed       |    Holds the most recent key pressed on the keyboard
# | 243  Start of Stack    |
# | 242  [more stack]      |    Stack grows down
# | ...                    |
# | 1  [more program]      |
# | 0  Program entry       |    Program loaded upward in memory starting at 0
# +-----------------------+
#     bottom of RAM


class CPU:
    """Main CPU class."""
    ram = [None] * 256
    registers = [0] * 8 


    def __init__(self):
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.branchtable[ADD] = self.handle_add
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[PUSH] = self.handle_push
        self.branchtable[POP] = self.handle_pop
        self.branchtable[CALL] = self.handle_call
        self.branchtable[RET] = self.handle_ret
        self.branchtable[CMP] = self.handle_cmp
        self.branchtable[JMP] = self.handle_jmp
        self.branchtable[JEQ] = self.handle_jeq
        self.branchtable[JNE] = self.handle_jne
        self.registers[SP] = 244#start at key pressed
        self.registers[PC] = 0#start program counter at 0
        self.registers[FL] = "00000000"#start program counter at 0

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        f = open(str(filename) + ".ls8", "r")

        print("Loading program " + filename + ":\n")

        for line in f:
            line_without_comments = line.split("#")[0].strip(" ")
            if(line_without_comments != ""):
                if(address > len(self.ram) - 1):
                    print("WARNING: The program file was too large to be loaded into ram fully. It may also be further overwritten by stack and other system memory.")
                    return
                int_instruction = int(line_without_comments, 2)
                print(str(int_instruction))
                self.ram[address] = int_instruction
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            result = self.registers[reg_a] + self.registers[reg_b]
            if result > 255:
                result = 255
            self.registers[reg_a] = result
        elif op == "MUL":
            result = self.registers[reg_a] * self.registers[reg_b]
            if result > 255:
                result = 255
            self.registers[reg_a] = result
        elif op == "CMP":
            #elif op == "SUB": etc
            if self.registers[reg_a] == self.registers[reg_b]:
                # print(str(self.registers[reg_a]) + " " + str(self.registers[reg_b]))
                fl_as_list = list(self.registers[FL]) #000 00l ge 
                fl_as_list[7] = "1"
                self.registers[FL] = "".join(fl_as_list)
            else:
                fl_as_list = list(self.registers[FL]) #000 00l ge 
                fl_as_list[7] = "0"
                self.registers[FL] = "".join(fl_as_list)
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, pc):
        return self.ram[pc]

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: \nPC: {self.registers[PC]} \nRAM at PC:{bin(self.ram_read(self.registers[PC]))}\nRAM at PC + 1{self.ram_read(self.registers[PC] + 1)}\nRAM at PC + 2{self.ram_read(self.registers[PC] + 2)}")

        # for i in range(8):
        #     print(f"{self.registers[i]}")

    def handle_ldi(self, instruction_address):
        self.registers[self.ram[instruction_address + 1]] = self.ram[instruction_address + 2]
        return instruction_address + 3

    def handle_prn(self, instruction_address):
        print(str(int(self.registers[self.ram[instruction_address + 1] ])))
        return instruction_address + 2

    def handle_add(self, instruction_address):
        self.alu("ADD", self.ram[instruction_address + 1], self.ram[instruction_address + 2])
        return instruction_address + 3

    def handle_mul(self, instruction_address):
        self.alu("MUL", self.ram[instruction_address + 1], self.ram[instruction_address + 2])
        return instruction_address + 3

    def handle_push(self, instruction_address):
        
        self.registers[SP] -= 1
        # print("Pushing " + str(self.registers[ self.ram[instruction_address + 1] ]) + " to " + str(self.registers[SP]) )

        self.ram[ self.registers[SP] ] = self.registers[ self.ram[instruction_address + 1] ]

        # Let stack grow as much as it wants? What if it overwrites our program in RAM?
        # if self.registers[SP] < 200:
        #     self.registers[SP] = 200

        return instruction_address + 2

    def handle_pop(self, instruction_address):
        # print("Popping " + str(self.ram[self.registers[SP]]) + " from " + str(self.registers[SP]) + " to " + str(self.ram[instruction_address + 1]) )
        self.registers[ self.ram[instruction_address + 1] ] = self.ram[ self.registers[SP] ]

        self.registers[SP] += 1
        if self.registers[SP] > 244:
            self.registers[SP] = 244
        return instruction_address + 2

    def handle_call(self, instruction_address):
        #spec says to use stack to keep track of where the subroutine was called from.
        #What if that subroutine calls push or pop an uneven amount of times though?
        #Wouldn't that cause us to lose track of the address to return to?
        return_address = instruction_address + 2

        self.registers[SP] -= 1

        self.ram[ self.registers[SP] ] = return_address

        return self.registers[ self.ram[instruction_address + 1] ]

    def handle_ret(self, instruction_address):

        return_address = self.ram[ self.registers[SP] ] 

        self.registers[SP] += 1

        return return_address

    def handle_cmp(self, instruction_address):
        self.alu("CMP", self.ram[instruction_address + 1], self.ram[instruction_address + 2])
        return instruction_address + 3

    def handle_jmp(self, instruction_address):
        return self.registers[self.ram[instruction_address + 1]]

    def handle_jeq(self, instruction_address):
        if self.registers[FL][7] == "1":
            return self.registers[self.ram[instruction_address + 1]]
        else:
            return instruction_address + 2

    def handle_jne(self, instruction_address):
        if self.registers[FL][7] != "1":
            return self.registers[self.ram[instruction_address + 1]]
        else:
            return instruction_address + 2

    def handle_hlt(self, instruction_address):
        #end the loop
        return len(self.ram) + 1#Is using 256 cheating?

    def run(self):
        """Run the CPU."""
        # print(self.ram)
        print("\n\n\nCPU RUNNING:\n\n\n")

        while self.registers[PC] <= len(self.ram):
            # self.trace()

            #handle the instruction and
            i = self.registers[PC]
            instruction_as_int = self.ram[i]
            if instruction_as_int in self.branchtable.keys():
                self.registers[PC] = self.branchtable[instruction_as_int](i)
            else:
                print("Unrecognized Instruction: " + bin(self.ram[i]) + "\n")
                print("Available Instructions: ")
                for instruction in list(self.branchtable.keys()):
                    print(bin(instruction))
                return

