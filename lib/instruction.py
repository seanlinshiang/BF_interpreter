from enum import Enum, auto

class Operation(Enum):
    Increase = auto()
    Decrease = auto()
    ShiftLeft = auto()
    ShiftRight = auto()
    Output = auto()
    Input = auto()
    JumpRight = auto()
    JumpLeft = auto()

class Instruction:
    def __init__(self, operation: Operation, address: int = -1) -> None: 
        self.operation = operation
        if operation in (Operation.JumpRight, Operation.JumpLeft):
            assert address >= 0, f"address = {address}: Instruction {operation.name} must have address >= 0"
            self.address = address

    def __str__(self) -> str:
        if hasattr(self, "address"):
            return f'{self.operation.name}: {self.address}'

        return f'{self.operation.name}'
    
    def __repr__(self) -> str:
        return self.__str__()
