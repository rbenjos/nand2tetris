class Code:

    def __init__(self):
        """
        sets up the lookup tables
        """
        self.JumpLookupTable = \
            {
                None: "000",
                "": "000", "JGT": "001", "JEQ": "010",
                "JGE": "011", "JLT": "100",
                "JNE": "101", "JLE": "110", "JMP": "111"
            }
        self.DestLookupTable = \
            {
                None: "000",
                "": "000", "M": "001", "D": "010",
                "MD": "011", "A": "100", "AM": "101",
                "AD": "110", "AMD": "111"
            }
        self.CalcLookupTable = \
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

    def dest(self, dest):
        """
        handles the dest part of command
        :param dest: destination of the calculation
        :return: the code for the destination
        """
        return self.DestLookupTable[dest]

    def jump(self, jmp):
        """
        handles the jump part of the command
        :param jmp: the condition of the jump
        :return: the code for that condition
        """
        return self.JumpLookupTable[jmp]

    def calc(self, clc):
        """
        handles the calculation part of the command
        :param clc: the type of calculation
        :return: the code for that calculation
        """
        return self.CalcLookupTable[clc]
