import time
import threading
import sys
import signal


class CPU:
    def __init__(self):
        print('Booting up')
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.sp = 7
        self.reg[self.sp] = 0xf4
        self.fl = 0b00000000
        self.MAR = 3
        self.MDR = 4

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

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""
        if op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
                # print('equal')
                return self.fl
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
                # print('greater than')
                return self.fl
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
                return self.fl
                # print('less than')
        elif op is "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            return self.reg[reg_a]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] ^= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            self.reg[reg_a] << self.reg[reg_b]
        elif op == "SHR":
            self.reg[reg_a] >> self.reg[reg_b]
        elif op == "MOD":
            if self.reg[reg_b] == '0':
                print('error message')
                self.hlt()
            else:
                self.reg[reg_a] %= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

    def timer_thing_maybe(self):
        print('\n', time.ctime(), '\n')
        threading.Timer(5, self.timer_thing_maybe).start()

    def keyboard_interrupt_handler(self, signal, frame):
        print()
        print('-'*50, '\n Keyboard interrupt, (ID: {}) has been caught, Cleaning up now....'.format(
            signal), '\n', '-'*50, '\n', '\n', '\n')
        exit(0)

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

    def jump(self):
        self.pc = self.reg[self.ram[self.pc + 1]]

    def jeq(self):
        if self.fl == 1:
            self.jump()
        else:
            self.pc += 2

    def jne(self):
        if self.fl != 1:
            self.jump()
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        # self.trace()
        print('-' * 25)

        # ir = self.ram_read(self.pc)

        running = True
        self.timer_thing_maybe()
        signal.signal(signal.SIGINT, self.keyboard_interrupt_handler)
        while running:
            ir = self.ram_read(self.pc)
            # print(f'Current IR: {ir}')

            if ir == 0b00000001:  # HLT -1- Computer Halt (STOP)
                print(f'{"-"*10} HLT {"-"*10} \n COMPUTER STOPPED')
                self.hlt()

            elif ir == 0b10000010:  # LDI -130- Add following item to reg???
                # print(f'{"-"*10} LDI {"-"*10} ')
                self.ldi()
            elif ir == 0b01000111:    # PRN -71- Display next item from ram
                self.prn()
            elif ir == 0b10100010:   # MUL -162- multipy the next two
                # print(f'{"-"*10} MUL {"-"*10} ')
                self.mul()
            elif ir == 0b10100000:   # MUL -162- multipy the next two
                # print(f'{"-"*10} ADD {"-"*10} ')
                self.add()
            elif ir == 0b01000101:    # Push -69- add item to stack in end of ram
                # print(f'{"-"*10} PUSH {"-"*10} ')
                self.push()
            elif ir == 0b01000110:    # Pop -- remove the last item from the stack
                # print(f'{"-"*10} POP {"-"*10} ')
                self.pop()
            elif ir == 0b01010000:  # Call -80-
                # print(f'{"-"*10} CALL {"-"*10} ')
                # print(self.pc, self.reg, self.ram[:10])
                self.call()
            elif ir == 0b00010001:  # RETURN -17-
                # print(f'{"-"*10} RETURN {"-"*10} ')
                self.ret()
            elif ir == 0b10100111:    # COMPARE -167-
                self.cmp()
            elif ir == 0b01010101:  # JEQ -85- jeq reg
                self.jeq()
            elif ir == 0b01010110:  # JNE -86- if E is false, jump to the given address
                self.jne()
            elif ir == 0b01010100:  # JMP -84-
                self.jump()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, item):
        # print('in ram_write')
        # print(address, item)
        self.ram[address] = item

    def ram_pop(self, address):
        self.reg[address] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def ram_push(self, address):
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[self.ram[address]]

    def reg_write(self, address, item):
        self.reg[address] = item

    def reg_read(self, address):
        # print(self.reg[address])
        return self.reg[address]


"""Main."""


cpu = CPU()

cpu.load()

cpu.run()
