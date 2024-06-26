import sys
from lib.program import Program

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 bf_intepreter.py <file name>")
        exit()

    file_name = sys.argv[1]
    with open(file_name, "r") as f:
        source_code = f.read()
    source_code = source_code.strip().replace(' ', '')


    program = Program(source_code)

    print(program.instructions)
    program.run()


if __name__ == "__main__":
    main()
