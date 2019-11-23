import re
import SymbolTable


class Parser:
    """
    handles parsing the text and returning the different parts
    of each line
    """

    def __init__(self):
        """
        sets up a symbol table object
        """
        self.symbol_table = SymbolTable.SymbolTable()

    # if we recon its an A instruction, we will parse it accordingly

    def parse_a(self, instruction):
        """
        parses an A type command
        :param instruction: the instruction/line of text
        :return: the code for that adress
        """
        instruction = instruction[1:]
        pattern = "^\d+$"
        mathces = re.findall(pattern, instruction)
        if len(mathces) == 1:
            return format(int(instruction), '015b')
        else:
            if not self.symbol_table.contains(instruction):
                address = self.symbol_table.create_var(instruction)
            else:
                address = self.symbol_table.get(instruction)

        return format(address, '015b')

    def parse_c(self, instruction):
        """
        parses a C type command
        :param instruction: the instruction/line of text
        :return: the dest/calc/jump parts of the C command as different variables
        """
        dest, calc, jump = None, None, None

        destreg = "^.*?="
        jumpreg = ";.*$"
        if "=" in instruction:
            dest_match = re.findall(destreg, instruction)
            dest = dest_match[0]
            instruction = instruction.replace(dest, '')
            dest = dest[:-1]
        if ";" in instruction:
            jump_match = re.findall(jumpreg, instruction)
            jump = jump_match[0]
            instruction = instruction.replace(jump, "")
            jump = jump[1:]

        # need to remove jump and dest!
        calc = instruction
        return dest, calc, jump

    def parse_label(self, instruction, counter):
        """
        helps with parsing a label, removing the parentheses
        :param instruction: the instruction/line of text
        :param counter: the counter that helps making a unique name for that label
        :return:
        """

        # basically just insert the exp without ()
        if instruction[0] == "(" and instruction[-1] == ")":
            self.symbol_table.create_label(instruction[1:-1], counter)

    def giveTable(self):
        """
        a helper method for debugging, prints the updated symbol table
        :return:
        """
        print(self.symbol_table)
