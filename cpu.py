import sys


class CPU:
    def __init__(self):
        print('Booting up')
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.fl = 0b00000000

    def load(self):
        program = []

        if len(sys.argv) == 1:

            sys.argv.append(
                'c:\\Users\\MPere\\Desktop\\Lambda\\Python\\SPRINT-CHALLENGE--COMPUTER-ARCHITECTURE/sctest.ls8')
            print(sys.argv)

        load_file = sys.argv[1]
        with open(load_file, 'r') as f:
            for line in f:
                # print(line)
                if line[0] == '\n' or line[0] == '#' or len(line) == 0:
                    continue
                else:
                    print(line[:8])
                    program.append(int(line[:8], 2))

            # print(program)
            f.close()

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
                print('equal')
                return self.fl
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
                print('greater than')
                return self.fl
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
                return self.fl
                print('less than')
        if op is "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            return self.reg[reg_a]
        if op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        if op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        if op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def hlt(self):
        self.pc += 1
        sys.exit(0)

    def ldi(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)

        self.pc += 3

    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def mul(self):
        self.alu('MUL', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def add(self):
        self.alu('ADD', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def cmp(self):
        self.alu('CMP', self.ram[self.pc + 1], self.ram[self.pc + 2])
        self.pc += 3

    def pop(self):
        self.ram_pop(self.ram[self.pc + 1])
        self.pc += 2

    def push(self):
        self.ram_push(self.pc + 1)
        self.pc += 2

    def call(self):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        self.pc += 2

    def ret(self):
        self.pc = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1
        self.pc += 1

    def run(self):
        """Run the CPU."""
        # self.trace()

        # ir = self.ram_read(self.pc)

        running = True
        while running:
            ir = self.ram_read(self.pc)
            print(f'Current IR: {ir}')

            if ir == 0b00000001:  # HLT -1- Computer Halt (STOP)
                print(f'{"-"*10} HLT {"-"*10} \n COMPUTER STOPPED')
                self.hlt()

            if ir == 0b10000010:  # LDI -130- Add following item to reg???
                print(f'{"-"*10} LDI {"-"*10} ')
                self.ldi()
            if ir == 0b01000111:    # PRN -71- Display next item from ram
                self.prn()
            if ir == 0b10100010:   # MUL -162- multipy the next two
                print(f'{"-"*10} MUL {"-"*10} ')
                self.mul()
            if ir == 0b10100000:   # MUL -162- multipy the next two
                print(f'{"-"*10} ADD {"-"*10} ')
                self.add()
            if ir == 0b01000101:    # Push -69- add item to stack in end of ram
                print(f'{"-"*10} PUSH {"-"*10} ')
                self.push()
            if ir == 0b01000110:    # Pop -- remove the last item from the stack
                print(f'{"-"*10} POP {"-"*10} ')
                self.pop()
            if ir == 0b01010000:  # Call -80-
                print(f'{"-"*10} CALL {"-"*10} ')
                # print(self.pc, self.reg, self.ram[:10])
                self.call()
            if ir == 0b00010001:  # RETURN -17-
                print(f'{"-"*10} RETURN {"-"*10} ')
                self.ret()
            if ir == 0b10100111:    # COMPARE -167-
                # alu function
                # cpm reg1, reg2
                # compare the values in the registers
                # if they are equal set the equal E flag to 1, otherwise set to 0
                # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
                # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
                self.cmp()
            if ir == 0b01010101:  # JEQ -85- jeq reg
                # if equal is true, jump to the next item in ram
                print(self.ram[self.pc],
                      self.ram[self.pc+1], self.ram[self.pc+2])
                if self.fl == 1:
                    print('equal')
                else:
                    self.pc += 2
                # break
            if ir == 0b01010110:    # JNE -86- if E is false, jump to the given address
                # print(self.ram[self.pc])
                # print(self.fl)
                if self.fl != 1:
                    self.pc = self.reg[self.ram[self.pc+1]]
                    # self.pc = self.ram[self.pc+1]
                else:
                    self.pc += 2
                # break
            if ir == 10:
                print('err')

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, item):
        print('in ram_write')
        print(address, item)
        self.ram[address] = item

    def ram_pop(self, address):
        self.reg[address] = self.ram[self.reg[7]]
        self.reg[7] += 1

    def ram_push(self, address):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram[address]]

    def reg_write(self, address, item):
        self.reg[address] = item

    def reg_read(self, address):
        print(self.reg[address])
        return self.reg[address]


"""Main."""


cpu = CPU()

cpu.load()
cpu.run()
