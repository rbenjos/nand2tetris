
class SymbolTable(object):
    """
    wrapper class for the symbol table
    """

    def __init__(self):
        """
        sets up a symbol table
        """
        self.symbolTable = \
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

        self.counter = 16

    def contains(self,key):
        """

        :param key: the key of the symbol
        :return: true if the symbol table contains that key, false if not
        """
        return key in self.symbolTable

    def get(self,key):
        """

        :param key: the key of that symbol
        :return: the value of that symbol
        """
        return self.symbolTable[key]

    def create_var(self,key):
        """
         creates a new variable in the symbol table
        :param key: the key of the new variable
        :return: its address in the code
        """
        self.symbolTable[key] = self.counter
        self.counter += 1
        return self.symbolTable[key]

    def create_label(self,key,val):
        """
        creates a new label in the symbol table
        :param key: the name of the label
        :param val: its place / address in the code
        :return:
        """
        self.symbolTable[key] = val


