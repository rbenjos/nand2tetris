class VMWriter:
    """ todo: !!! important!!! symobl tables for operators so we can convert
    todo: them easily to vm code
    """
    BIN_OPS = \
        {
            '+': 'add',
            '-': 'sub',
            '&': 'and',
            '|': 'or',
            '<': 'lt',
            '>': 'gt',
            '=': 'eq'
        }

    UN_OPS = \
        {
            '~': 'not',
            '-': 'neg'
        }

    def __init__(self, out_file_name):
        self.outFile = open(out_file_name, 'w')

    def out(self, string):
        self.outFile.write(string + '\n')

    def writePush(self, segment, index):
        """
        this method writes a push command in vm language according to the
        segment and index we are pulling from
        :param segment: the segment from which we are pushing
        :param index: the index in that segment
        :return: nothing
        """
        self.out('push ' + segment + ' ' + str(index))

    def writePop(self, segment, index):
        """
        this method writes a pop command in vm language according to the
        segment and index we are pushing to
        :param segment: the segment to which we are pushing
        :param index: the index in the segment
        :return: nothing
        """
        self.out('pop ' + segment + ' ' + str(index))


    def WriteArithmetic(self, command, un):
        """
        this method writes an arithmetic command in vm language
        :param command: the arithmetic operators name
        :param un: whether the symbol is unary or not
        :return: nothing
        """
        if un:
            command = self.UN_OPS[command]
        else:
            command = self.BIN_OPS[command]
        self.out(command)

    def WriteLabel(self, label):
        """
        this method writes a new label in vm language
        :param label: the labels name
        :return: nothing
        """
        self.out('label ' + label)

    def WriteGoto(self, label):
        """
        this method writes a goto command to a certain label in vm language
        :param label: the labels name
        :return: nothing
        """
        self.out('goto ' + label)

    def WriteIf(self, label):
        """
        this method writes an if command in vm language
        :param label: the labels name
        :return: nothing
        """
        self.out('if-goto ' + label)

    def writeCall(self, name, n_args):
        """
        this method calls a function in vm language
        :param name: the name of the function
        :param n_args: the number of arguments it uses
        :return: nothing
        """
        self.out('call ' + name + ' ' + str(n_args))

    def writeFunction(self, name, n_args):
        """
        this method declares a function in vm language
        :param name: the name of the function
        :param n_args: the number of arguments it uses
        :return: nothing
        """
        self.out('function ' + name + ' ' + str(n_args))

    def writeReturn(self):
        """
        just writes return basically
        :return: nothing
        """
        self.out('return')

    def close(self):
        """
        closes the output file we are writing into
        :return: nothing
        """
        self.outFile.close()
