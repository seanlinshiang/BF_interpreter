from lib.instruction import Instruction, Operation
from collections import deque

class Program:
    def __init__(self, source_code):
        self.instructions = self.parse_source_code(source_code)

    def parse_source_code(self, source_code):
        instructions = []
        new_inst = None
        left_bracket_stack = deque()
        for character in source_code:
            match character:
                case '+':
                    new_inst = Instruction(Operation.Increase)
                case '-':
                    new_inst = Instruction(Operation.Decrease)
                case '>':
                    new_inst = Instruction(Operation.ShiftRight)
                case '<':
                    new_inst = Instruction(Operation.ShiftLeft)
                case '.':
                    new_inst = Instruction(Operation.Output)
                case ',':
                    new_inst = Instruction(Operation.Input)

                case '[':
                    curr_address = len(instructions) 
                    left_bracket_stack.append(curr_address)
                    new_inst = None 
                    
                case ']':
                    curr_address = len(instructions)
                    if len(left_bracket_stack) < 1:
                        raise RuntimeError("unbalanced bracket")
                    prev_address = left_bracket_stack.pop()
                    instructions[prev_address] = Instruction(Operation.JumpRight, curr_address)
                    new_inst = Instruction(Operation.JumpLeft, prev_address)
                case _:
                    continue
            instructions.append(new_inst)
        return instructions


    def run(self):
        program_counter = 0
        memory = [0] * 30_000
        pointer = 0

        while program_counter < len(self.instructions):
            match self.instructions[program_counter]:
                case Instruction(operation=Operation.Increase):
                    memory[pointer] += 1

                case Instruction(operation=Operation.Decrease):
                    memory[pointer] -= 1

                case Instruction(operation=Operation.ShiftRight):
                    pointer = (pointer + 1) % len(memory)

                case Instruction(operation=Operation.ShiftLeft):
                    pointer = (pointer + len(memory) - 1) % len(memory)

                case Instruction(operation=Operation.Output):
                    print(chr(memory[pointer]), end='')

                case Instruction(operation=Operation.Input):
                    c = input('\nInput char: ').strip()
                    memory[pointer] = ord(c)

                case Instruction(operation=Operation.JumpRight, address=end_addr):
                    if memory[pointer] == 0:
                        program_counter = end_addr

                case Instruction(operation=Operation.JumpLeft, address=start_addr):
                    if memory[pointer] != 0:
                        program_counter = start_addr

                case _:
                    pass
            program_counter += 1

        print(memory[:50])
                    


            

                
                    
                    
