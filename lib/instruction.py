from enum import Enum, auto

class Operation(Enum):
    Add = auto()
    Shift = auto()
    Output = auto()
    Input = auto()
    JumpRight = auto()
    JumpLeft = auto()
    Clear = auto()
    AddTo = auto()

class Instruction:
    def __init__(self, operation: Operation, val1=None, val2=None) -> None: 
        self.operation = operation
        match operation:
            case Operation.JumpRight | Operation.JumpLeft:
                assert val1 is not None and val1 >= 0, f"address = {val1}: Instruction {operation.name} must have address >= 0"
                self.val1 = val1
            case Operation.Add | Operation.Shift:
                assert val1 is not None, f"val1 = {val1}: Instruction {operation.name} must have val1 >= 0"
                self.val1 = val1
            case Operation.AddTo:
                assert val1 is not None, f"val1 = {val1}: Instruction {operation.name} must have val1 >= 0"
                assert val2 is not None, f"val2 = {val2}: Instruction {operation.name} must have val2 >= 0"
                self.val1 = val1
                self.val2 = val2


    def __str__(self) -> str:
        if hasattr(self, "val1"):
            if hasattr(self, "val2"):
                return f'{self.operation.name}: {self.val1}, {self.val2}'
            return f'{self.operation.name}: {self.val1}'

        return f'{self.operation.name}'
    
    def __repr__(self) -> str:
        return self.__str__()
