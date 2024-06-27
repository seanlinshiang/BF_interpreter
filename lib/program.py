from lib.instruction import Instruction, Operation
from collections import deque
import time
import io

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
                        new_inst = Instruction(Operation.Add, value=inc)
                    else:
                        instructions[-1].value += inc

                case '>' | '<':
                    inc = 1 if character == '>' else -1
                    if len(instructions) == 0 or instructions[-1].operation != Operation.Shift:
                        new_inst = Instruction(Operation.Shift, value=inc)
                    else:
                        instructions[-1].value += inc

                case '.':
                    new_inst = Instruction(Operation.Output)
                case ',':
                    new_inst = Instruction(Operation.Input)

                case '[':
                    curr_address = len(instructions) 
                    left_bracket_stack.append(curr_address)
                    new_inst = Instruction(Operation.JumpRight, value=0) 
                    
                case ']':
                    if len(left_bracket_stack) < 1:
                        raise RuntimeError("unbalanced bracket")
                    curr_address = len(instructions)
                    prev_address = left_bracket_stack.pop()
                    instructions[prev_address] = Instruction(Operation.JumpRight, value=curr_address)
                    new_inst = Instruction(Operation.JumpLeft, value=prev_address)
                case _:
                    pass
            if new_inst is not None:
                instructions.append(new_inst)
        return instructions


    def run(self):
        program_counter = 0
        memory = [0] * 30_000
        pointer = 0
        start_time = time.time()

        strio = io.StringIO()
        print(f"len of instructions: {len(self.instructions)}")
        while program_counter < len(self.instructions):
            match self.instructions[program_counter]:
                case Instruction(operation=Operation.Add, value=value):
                    memory[pointer] += value

                case Instruction(operation=Operation.Shift, value=value):
                    pointer += value

                case Instruction(operation=Operation.Output):
                    strio.write(chr(memory[pointer]))
                    # print(chr(memory[pointer]), end='')

                case Instruction(operation=Operation.Input):
                    c = input('\nInput char: ').strip()
                    memory[pointer] = ord(c)

                case Instruction(operation=Operation.JumpRight, value=end_addr):
                    if memory[pointer] == 0:
                        program_counter = end_addr

                case Instruction(operation=Operation.JumpLeft, value=start_addr):
                    if memory[pointer] != 0:
                        program_counter = start_addr

                case _:
                    pass
            program_counter += 1

        print(strio.getvalue())
        print(memory[:50])
    
        end_time = time.time()
        print(f"Program took {end_time - start_time}s to run")
