import sys
from collections import deque, defaultdict

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 profiling.py <file_name>")
        exit(-1)

    file_name = sys.argv[1]

    with open(file_name, "r") as f:
        source_code = f.read()
    source_code = source_code.strip().replace(' ', '').replace('\n', '')

    left_bracket_stack = deque()
    profile_dict = defaultdict(lambda: 0)

    for i, c in enumerate(source_code):
        match c:
            case '[':
                left_bracket_stack.append(i)
            case ']':
                start_i = left_bracket_stack.pop()
                profile_dict[source_code[start_i:i+1]] += 1
    print(sorted(profile_dict.items(), key=lambda x: x[1], reverse=True)[:10])

if __name__ == "__main__":
    main()
                
                

 
    


