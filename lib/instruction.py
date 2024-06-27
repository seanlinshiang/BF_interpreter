from enum import Enum, auto

class Operation(Enum):
    Add = auto()
    Shift = auto()
    Output = auto()
    Input = auto()
    JumpRight = auto()
    JumpLeft = auto()
    Clear = auto()

class Instruction:
    def __init__(self, operation: Operation, value=None) -> None: 
        self.operation = operation
        match operation:
            case Operation.JumpRight | Operation.JumpLeft:
                assert value is not None and value >= 0, f"address = {value}: Instruction {operation.name} must have address >= 0"
                self.value = value
            case Operation.Add | Operation.Shift:
                assert value is not None, f"value = {value}: Instruction {operation.name} must have value >= 0"
                self.value = value


    def __str__(self) -> str:
        if hasattr(self, "value"):
            return f'{self.operation.name}: {self.value}'

        return f'{self.operation.name}'
    
    def __repr__(self) -> str:
        return self.__str__()
