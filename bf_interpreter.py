import sys

class Stack:
    def __init__(self):
        self.container = []

    def push(self, e):
        self.container.append(e)

    def pop(self):
        self.container.pop()

    def top(self):
        if len(self.container) < 1:
            raise RuntimeError("Trying to access stack with 0 element") 
        return self.container[-1]

def parse_source_code(source_code):
    source_code = source_code.strip()
    tmp = source_code

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 bf_intepreter.py <file name>")
        exit()

    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        source_code = f.read()
    source_code = source_code.strip().replace(' ', '')

    program_counter = 0
    memory = [0] * 30_000
    pointer = 0

    left_bracket_stack = Stack()

    while program_counter < len(source_code):
        # print(source_code[program_counter])
        match source_code[program_counter]:
            case '+':
                memory[pointer] += 1
            case '-':
                memory[pointer] -= 1
            case '>':
                pointer = (pointer + 1) % len(memory) 
            case '<':
                pointer = (pointer + len(memory) - 1) % len(memory)

            case '[':
                left_bracket_stack.push((program_counter, pointer))
            case ']':
                next_counter, next_pointer = left_bracket_stack.top()
                if memory[next_pointer] > 0:
                    program_counter = next_counter 
                else:
                    left_bracket_stack.pop()
            
            case '.':
                print(chr(memory[pointer]), end='')
            case ',':
                c = input("\nInput char: ").strip()
                memory[pointer] = ord(c)

            # Ignore comment
            case '#':
                while program_counter < len(source_code) and source_code[program_counter] != '\n':
                    program_counter += 1

            case _:
                pass
        program_counter += 1 
    print(memory[:50])


if __name__ == "__main__":
    main()
