class Coder:

    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output_file = open(self.output_file_name, 'w')

        self.stackPointer = 256
        self

    def writeArithmetic(self, command):
        if command[0] == "add":
            self.write_add()
        elif command[0] == "sub":
            self.write_sub()
        elif command[0] == "neg":
            self.write_neg()
        elif command[0] == "eq":
            self.write_eq()
        elif command[0] == "gt":
            self.write_gt()
        elif command[0] == "lt":
            self.write_lt()
        elif command[0] == "and":
            self.write_and()
        elif command[0] == "or":
            self.write_or()
        elif command[0] == "not":
            self.write_not()

    def writePushPop(self, command):

    def close(self):
        self.output_file.close()

    def write_add(self):
        pass

    def write_sub(self):
        pass

    def write_neg(self):
        pass

    def write_eq(self):
        pass

    def write_gt(self):
        pass

    def write_lt(self):
        pass

    def write_and(self):
        pass

    def write_or(self):
        pass

    def write_not(self):
        pass
