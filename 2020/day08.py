import os

script_dir = os.path.dirname(__file__)
script_name = os.path.splitext(os.path.basename(__file__))[0]
input_file = os.path.join(script_dir, f"inputs/{script_name}_input.txt")
lines = [line.rstrip("\n") for line in open(input_file)]

program = {}
for i, line in enumerate(lines):
    instruction, param = line.split(" ")
    program[i] = (instruction, int(param))


class Computer:
    INITIALISED = "Initialised"
    RUNNING = "Running"
    LOOP_ERROR = "Loop Error"
    TERMINATED = "Terminated"

    def __init__(self, program, patches={}):
        self.program = program
        self.patches = patches
        self.stack_trace = {}
        self.pointer = 0
        self.accumulator = 0
        self.status = self.INITIALISED

    def run_program(self):
        self.status = self.RUNNING
        while True:
            if self.pointer in self.stack_trace:
                return self.LOOP_ERROR
            if self.pointer not in self.program:
                return self.TERMINATED
            instruction, param = self.program[self.pointer]
            instruction = self.patches.get(self.pointer, instruction)
            self.stack_trace[self.pointer] = (instruction, param, self.accumulator)
            getattr(self, instruction)(param)

    def acc(self, param):
        self.accumulator += param
        self.pointer += 1

    def jmp(self, param):
        self.pointer += param

    def nop(self, param):
        self.pointer += 1


computer = Computer(program)
computer.run_program()
print(f"Part 1: {computer.accumulator}")

stack_trace = computer.stack_trace
part2 = None
for pointer, (instruction, _, _) in stack_trace.items():
    if instruction == "acc":
        continue
    patch = {pointer: {"nop": "jmp", "jmp": "nop"}[instruction]}
    test_computer = Computer(program, patches=patch)
    if test_computer.run_program() == Computer.TERMINATED:
        part2 = test_computer.accumulator
        break

print(f"Part 2: {part2}")