from lib.instruction import Instruction, Operation
from collections import deque
import time

class Program:
    def __init__(self, source_code):
        self.instructions = self.parse_source_code(source_code)

    def parse_source_code(self, source_code):
        print(source_code)
        instructions = []
        left_bracket_stack = deque()
        for character in source_code:
            new_inst = None
            # print(character)
            match character:
                case '+' | '-':
                    inc = 1 if character == '+' else -1
                    if len(instructions) == 0 or instructions[-1].operation != Operation.Add:
                        new_inst = Instruction(Operation.Add, val1=inc)
                    else:
                        instructions[-1].val1 += inc

                case '>' | '<':
                    inc = 1 if character == '>' else -1
                    if len(instructions) == 0 or instructions[-1].operation != Operation.Shift:
                        new_inst = Instruction(Operation.Shift, val1=inc)
                    else:
                        instructions[-1].val1 += inc

                case '.':
                    new_inst = Instruction(Operation.Output)
                case ',':
                    new_inst = Instruction(Operation.Input)

                case '[':
                    curr_address = len(instructions) 
                    left_bracket_stack.append(curr_address)
                    new_inst = Instruction(Operation.JumpRight, val1=0) 
                    
                case ']':
                    if len(left_bracket_stack) < 1:
                        raise RuntimeError("unbalanced bracket")
                    curr_address = len(instructions)
                    prev_address = left_bracket_stack.pop()
                    new_inst = self.optimize_loop(instructions, prev_address, curr_address)
                case _:
                    pass
            if new_inst is not None:
                instructions.append(new_inst)
        return instructions

    def optimize_loop(self, instructions, prev_address, curr_address):
        new_inst = None
        match instructions[prev_address:curr_address]:
            # case for [-], clearing cell
            case [Instruction(operation=Operation.JumpRight), 
                  Instruction(operation=Operation.Add, val1=-1)]:
                for _ in range(2):
                    instructions.pop()
                new_inst = Instruction(Operation.Clear)

            # case for add to another cell, [-1>4+1<4]
            case [Instruction(operation=Operation.JumpRight),
                  Instruction(operation=Operation.Add, val1=-1),
                  Instruction(operation=Operation.Shift, val1=x),
                  Instruction(operation=Operation.Add, val1=v),
                  Instruction(operation=Operation.Shift, val1=y)] if x == -y:
                for _ in range(5):
                    instructions.pop()
                new_inst = Instruction(Operation.AddTo, val1=x, val2=v) 

            case _:
                instructions[prev_address] = Instruction(Operation.JumpRight, val1=curr_address)
                new_inst = Instruction(Operation.JumpLeft, val1=prev_address)

        return new_inst

    def run(self):
        program_counter = 0
        memory = [0] * 30_000
        pointer = 0
        start_time = time.time()

        print(f"len of instructions: {len(self.instructions)}")
        while program_counter < len(self.instructions):
            match self.instructions[program_counter]:
                case Instruction(operation=Operation.Add, val1=val1):
                    memory[pointer] += val1

                case Instruction(operation=Operation.Shift, val1=val1):
                    pointer += val1

                case Instruction(operation=Operation.Output):
                    print(chr(memory[pointer]), end='')

                case Instruction(operation=Operation.Input):
                    c = input('\nInput char: ').strip()
                    memory[pointer] = int(c)

                case Instruction(operation=Operation.JumpRight, val1=end_addr):
                    if memory[pointer] == 0:
                        program_counter = end_addr

                case Instruction(operation=Operation.JumpLeft, val1=start_addr):
                    if memory[pointer] != 0:
                        program_counter = start_addr

                case Instruction(operation=Operation.Clear):
                    memory[pointer] = 0

                case Instruction(operation=Operation.AddTo, val1=to, val2=multiplier):
                    memory[pointer + to] += memory[pointer] * multiplier
                    memory[pointer] = 0

                case _:
                    pass
            program_counter += 1

        print(memory[:50])
    
        end_time = time.time()
        print(f"Program took {end_time - start_time}s to run")
