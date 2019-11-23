# all the lookup tables we will possibly need
import Parser
import Code
import sys
import re

SymbolTable = \
    {
        # first the predefined ones
        "R0": 0, "R1": 1, "R2": 2, "R3": 3,
        "R4": 4, "R5": 5, "R6": 6, "R7": 7,
        "R8": 8, "R9": 9, "R10": 10, "R11": 11,
        "R12": 12, "R13": 13, "R14": 14, "R15": 15,

        "SCREEN": 0x4000, "KBD": 0x6000,

        "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4

        # from now on we can add more
    }

JumpLookupTable = \
    {
        "": "000", "JGT": "001", "JEQ": "010",
        "JGE": "011", "JLT": "100",
        "JNE": "101", "JLE": "110", "JMP": "111"
    }
DestLookupTable = \
    {
        "": "000", "M": "001", "D": "010",
        "MD": "011", "A": "100", "AM": "101",
        "AD": "110", "AMD": "111"
    }
CalcLookupTable = \
    {
        'A>>': '010000000', 'D>>': '010010000', 'A<<': '010100000',
        'D<<': '010110000', 'M>>': '011000000', 'M<<': '011100000',
        "0": "0101010", "1": "0111111", "-1": "0111010",
        "D": "0001100", "A": "0110000", "!D": "0001101",
        "!A": "0110001", "-D": "0001111", "-A": "0110011",
        "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
        "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
        "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",

        "M": "1110000", "!M": "1110001", "-M": "1110011",
        "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
        "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
        "D|M": "1010101"
    }


class Assembler:
    """
    this class cleans up the assembly file, handles the label. uses the parser and the Code classes to
    turn assembly into binary
    """

    def __init__(self, inputFileName):
        self._inputFileName = inputFileName
        self._outputFileName = inputFileName.replace(".asm", ".hack")
        self.parser = Parser.Parser()
        self.code = Code.Code()
        self.input_list = []

    # what we need to do is as follows:

    # first we take in a file as an input

    # we open the file
    def assemble(self):
        """
        the main method, does a first run (to handle labels and variables)
        and then does a full run to assemble everything
        :return:
        """
        self.first_run()
        self.full_run()

    def first_run(self):
        """
        this method does the first run, cleaning up the file and handling label/variables
        :return:
        """

        with open(self._inputFileName) as inputFile:
            input_string = inputFile.read()
            inputFile.close()

        self.input_list = input_string.split("\n")
        comment_regex = r"//.*?$"
        # remove comments
        self.input_list = [line for line in self.input_list if not line.startswith("//") and line is not ""]
        self.input_list = [re.sub(comment_regex,'',line) for line in self.input_list]

        # remove spaces
        self.input_list = [re.sub(' ','',line) for line in self.input_list]

        # parse labels
        for counter, line in enumerate(self.input_list):
            if line.startswith("("):
                self.parser.parse_label(line, counter)
        self.input_list = [line for line in self.input_list if not line.startswith("(")]

    def full_run(self):
        """
        goes over the lines, parses them, and assembles them using the coder
        :return:
        """

        with open(self._outputFileName, 'w') as outputFile:
            i = 0
            while i < len(self.input_list):

                line = self.input_list[i]
                if line[0] == "@":
                    address = "0" + self.parser.parse_a(line)
                    print(address)
                    outputFile.writelines(address + "\n")
                else:
                    dest, clc, jmp = self.parser.parse_c(line)
                    c_ins = "111" + self.code.calc(clc) + self.code.dest(dest) + self.code.jump(jmp)
                    print(c_ins)
                    outputFile.writelines(c_ins + "\n")
                i += 1

            outputFile.close()


assert len(sys.argv) == 2
assembler = Assembler(sys.argv[1])
assembler.assemble()
