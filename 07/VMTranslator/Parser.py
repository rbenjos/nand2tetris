class Parser:
    c_type_table = \
        {
            "add": "C_ARITHMETIC", "sub": "C_ARITHMETIC", "neg": "C_ARITHMETIC",
            "eq": "C_ARITHMETIC", "gt": "C_ARITHMETIC", "lt": "C_ARITHMETIC",
            "and": "C_ARITHMETIC", "or": "C_ARITHMETIC", "not": "C_ARITHMETIC",
            "push": "C_PUSH", "pop": "C_POP", "label": "C_LABEL",
            "goto": "C_GOTO", "if-goto": "C_IF",
            "function": "C_FUNCTION", "return": "C_RETURN", "call": "C_CALL"
        }

    def __init__(self, input_file_name):
        # first we take in a text file, and transfer it to a list of lines, each
        # representing a command, we can disregard empty lines
        self.input_file_name = input_file_name

        # open and produce a list of lines
        with open(input_file_name) as self.input_file:
            input_string = self.input_file.read()
            self.input_file.close()

        self.inputs_list = input_string.split("\n")
        self.inputs_list = [line for line in self.inputs_list if line is not ""]

        self.counter = 0

        self.arg1 = None
        self.arg2 = None
        self.command_type = None

        # lets load the first command
        self.current_line = self.inputs_list[self.counter]
        self.command = self.current_line.split(" ")
        self.command = [word for word in self.command if word is not " "]

        self.command_type = Parser.c_type_table[self.command[0]]
        if len(self.command) > 1:
            self.arg1 = self.command[1]
        if len(self.command) > 2:
            self.arg2 = self.command[2]

    def hasMoreCommands(self):
        return self.counter < len(self.inputs_list)

    def advance(self):
        self.counter += 1
        self.current_line = self.inputs_list[self.counter]
        self.command = self.current_line.split(" ")
        self.command = [word for word in self.command if word is not " "]

        self.command_type = Parser.c_type_table[self.command[0]]
        if len(self.command) > 1:
            self.arg1 = self.command[1]
        if len(self.command) > 2:
            self.arg2 = self.command[2]

    def commandType(self):
        return self.command_type

    def arg1(self):
        return self.arg1

    def arg2(self):
        return self.arg2
