import symbolTable
import VMWriter

class CompilationEngine:
    CLASS_VARIABLES = ['static', 'field']
    SUBROUTINE_TYPES = ['constructor', 'method', 'function']
    TYPES = ['int', 'char', 'boolean']
    STATEMENTS = {'do', 'let', 'if', 'while', 'return'}
    OPS = ['+', '-', '*', '/', '&', ',', '<', '>', '=']

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.output_file = open('temp', 'w')
        self.CLASSES = []
        self.classTable = symbolTable.SymbolTable()
        self.subRoutineTable = symbolTable.SymbolTable()
        self.vm_writer = VMWriter.VMWriter()
        self.if_label_counter = 0
        self.while_label_counter = 0


    def out(self, phrase):
        """
        :param phrase:
        :return:
        """
        self.output_file.write(phrase)

    def start(self, phrase):
        """
        :param phrase:
        :return:
        """
        self.out("<" + phrase + ">")

    def end(self, phrase):
        """
        :param phrase:
        :return:
        """
        self.out("</" + phrase + ">")

    def bound(self, phrase, ter_type):
        """

        :param phrase:
        :param ter_type:
        :return:
        """
        self.start(ter_type)
        self.out(phrase)
        self.end(ter_type)

    def token(self):
        return self.token()

    def CompileClass(self):
        """
        how do we parse a class? we start with the keyword class,
        then the class name, brackets and within them all
        variables and then the functions/methods
        :return:
        """

        # class keyword and name, start of body
        self.tokenizer.advance()
        self.start('class')

        # class
        self.bound(self.tokenizer.advance(), 'keyword')

        # name
        self.bound(self.tokenizer.advance(), 'identifier')

        # {
        self.bound(self.tokenizer.advance(), 'symbol')

        # now to declare all class variables

        token = self.tokenizer.advance()
        while token in self.CLASS_VARIABLES:
            self.compileClassVarDec()

        # now to declare all methods

        token = self.tokenizer.advance()
        while token in self.SUBROUTINE_TYPES:
            self.compileSubroutine()

        # }
        self.bound(self.tokenizer.advance(), 'symbol')

        self.end('class')

    def compileClassVarDec(self):
        """
        a variable or variables start with static or field,
        then their type, then their name, and a ',' with more
        potential varnames. ends with a ';'
        :return:
        """

        # class var dec
        self.start('classVarDec')

        # field? static?
        self.bound(self.tokenizer.advance(), 'keyword')

        self.tokenizer.advance()
        # var dec

        # ;
        self.bound(self.token(), 'identifier')
        self.end('classVarDec')

    def compileType(self):
        token = self.token()
        if token in self.TYPES:
            self.bound(token, 'keyword')

        elif token in self.CLASSES:
            self.bound(token, 'identifier')


        else:
            # todo: raise an exception i guess
            pass

    def compileSubroutine(self):
        """
        a subroutine decleration start with a keyword of the following:
        ['constructor','function','method'], then the return type ['void',type]
        then the subroutine name, the parameter list within parentheses and
        then the subroutine body
        todo: add compile subroutine body helper
        :return:
        """

        # subroutine
        self.start('subroutineDec')

        # function/method/constructor
        self.bound(self.tokenizer.advance(), 'keyword')

        # function return type
        self.tokenizer.advance()
        if self.token() is 'void':
            self.bound(self.token(), 'keyword')
        else:
            self.compileType()

        # function variables

        # (
        self.bound(self.tokenizer.advance(), 'symbol')

        # parameter list
        self.tokenizer.advance()
        self.compileParameterList()

        # )
        self.bound(self.token(), 'symbol')

        # subroutine body
        self.compileSubroutineBody()

        self.end('subroutineDec')

    def compileParameterList(self):
        """
        the parameter list is potentially empty, but has couples of types
        and varnames with ',' between them
        :return:
        """

        # if there are no parameters, we should go back
        if self.token() is ')':
            return

        else:
            self.start('parameterList')

            # type
            self.tokenizer.advance()
            self.compileType()
            # name
            self.bound(self.tokenizer.advance(), 'identifier')

            # other parameters

            while self.tokenizer.advance() is ',':
                self.bound(self.token(), 'symbol')
                self.bound(self.tokenizer.advance(), 'identifier')

            self.end('parameterList')

    def compileSubroutineBody(self):
        self.start('subroutineBody')

        # {
        self.bound(self.tokenizer.advance(), 'symbol')

        while self.tokenizer.advance() is 'var':
            self.bound(self.token(), 'keyword')
            self.compileVarDec()

        self.compileStatements()

        # }
        self.bound(self.tokenizer.advance(), 'symbol')
        self.end('subroutineBody')

    def compileVarDec(self):
        """
        declaring a var in a function starts with keyword 'var' then the type
        and then the name. can also be followed by commas and more names, ends
        with ';'
        :return:
        """
        # type
        self.bound(self.compileType(), 'keyword')

        # name
        self.bound(self.tokenizer.advance(), 'identifier')
        while self.token() is ',':
            self.bound(self.token(), 'symbol')
            self.bound(self.tokenizer.advance(), 'identifier')
            self.tokenizer.advance()

    def compileStatements(self):
        """
        compiles all following statements in a loop
        :return:
        """

        self.start('statements')

        while self.tokenizer.advance() in self.STATEMENTS:
            self.compileStatement()

        self.end('statements')

    def compileStatement(self):
        """
        compiles statement based on its keyword
        :return:
        """
        if self.token is 'do':
            self.compileDo()
        elif self.token is 'let':
            self.compileLet()
        elif self.token is 'if':
            self.compileIf()
        elif self.token is 'while':
            self.compileWhile()
        elif self.token is 'return':
            self.compileReturn()

    def compileDo(self):
        """
        calls a subroutine, keyword 'do' then a subroutine call
        :return:
        """

        self.start('doStatement')

        # do
        self.bound(self.token(), 'keyword')

        # call subroutine
        self.tokenizer.advance()
        self.bound(self.token(), 'identifier')
        self.tokenizer.advance()

        self.tokenizer.advance()
        self.compileSubroutineCall()

        # ;
        self.bound(self.tokenizer.advance(), 'symbol')
        self.end('doStatement')

    def compileSubroutineCall(self):
        """
        :return:
        """

        # handling after the first identifier , advanced after it

        # ( or .
        # if .
        if self.token() is '.':
            # .
            self.bound(self.token(), 'symbol')
            # name of subroutine
            self.bound(self.tokenizer.advance(), 'identifier')
            # (
            self.bound(self.token(), 'symbol')
            # expression list
            self.tokenizer.advance()
            self.compileExpressionList()
            # )
            self.bound(self.tokenizer.advance(), 'symbol')
        # if (
        else:
            # (
            self.bound(self.token(), 'symbol')
            # expression list
            self.tokenizer.advance()
            self.compileExpressionList()
            # )
            self.bound(self.tokenizer.advance(), 'symbol')

        self.end('subroutineCall')

    def compileLet(self):
        """
        assignment, 'let', then a varname (with an expression in brackets if
        its an array) then '=' and then another expression. ends with ';'
        :return:
        """
        # let

        # varname
        self.bound(self.tokenizer.advance(), 'identifier')
        isArray = False
        # finding identifier in tables
        if self.subRoutineTable.contains(self.token()):
            lastLineSeg = self.subRoutineTable.kindOf(self.token())
            lastLineindex = self.subRoutineTable.indexOf(self.token())
        elif self.classTable.contains(self.token()):
            lastLineSeg = self.classTable.kindOf(self.token())
            lastLineindex = self.classTable.indexOf(self.token())
        else:
            print("identifier doesn't exist")

        # might be an array, need to check that
        if self.tokenizer.advance() is '[':
            isArray = True
            # [

            """pushing array base address"""
            self.vm_writer.writePush(lastLineSeg, lastLineindex)
            self.tokenizer.advance()

            """push expression result""" #todo - make sure expression leaves the result on the top of the stack
            self.compileExpression()
            # ]

            """adding the base address and the expression result"""
            self.vm_writer.WriteArithmetic("add")



            self.bound(self.tokenizer.advance(), 'symbol')
            self.tokenizer.advance()




        # otherwise its a =
        self.bound(self.token(), 'symbol')

        # then an expression
        self.tokenizer.advance()

        """calculating the expression""" # todo-make sure expression leaves the result on the top of the stack
        self.compileExpression()

        """poping the result to temp 0 so we will get access to the previous addition result"""
        self.vm_writer.writePop("temp", 0)

        # ;
        self.bound(self.tokenizer.advance(), 'symbol')
        """if the value should be put in an array then pop the expression result to that 0"""
        if isArray:
            """poping to pointer 1(that) so that 0 will hold the required array cell"""
            self.vm_writer.writePop("pointer", 1)
            self.vm_writer.writePush("temp", 0)
            self.vm_writer.writePop("that", 0)
        else:
            """if not then pop the expression result to the given address"""
            self.vm_writer.writePop(lastLineSeg, lastLineindex)

        self.end('letStatement')

    def compileWhile(self):
        """
        :return:
        """
        self.while_label_counter += 1
        while_label = "While Loop _" + str(self.label_counter)
        end_while_label = "End Of while" + str(self.label_counter)
        self.start('whileStatement')
        # while
        self.bound(self.tokenizer.advance(), 'keyword')

        # (
        self.bound(self.tokenizer.advance(), 'symbol')

        # the condition expression
        self.tokenizer.advance()

        self.vm_writer.WriteLabel(while_label)

        """make sure the result is on the top of the stack"""
        self.compileExpression()
        # )
        self.vm_writer.WriteArithmetic("neg")
        self.bound(self.tokenizer.advance(), 'symbol')

        """creating if condition"""
        self.vm_writer.WriteIf(end_while_label)

        # the body of while

        # {
        self.bound(self.tokenizer.advance(), 'symbol')

        # statements
        self.compileStatements()
        self.vm_writer.WriteGoto(while_label)
        self.vm_writer.WriteLabel(end_while_label)



        # }
        self.bound(self.tokenizer.advance(), 'symbol')

        self.end('whileStatement')

    def compileReturn(self):
        """
        :return:
        """
        self.start('returnStatement')
        # return
        self.bound(self.token(), 'keyword')

        # expression (might be empty)
        self.tokenizer.advance()
        if self.token() is not ';':
            self.compileExpression()
            self.tokenizer.advance()
        else:
            self.vm_writer.writePush("constant", 0)
        self.vm_writer.writeReturn()

        # ;
        self.bound(self.token(), 'symbol')
        self.end('returnStatement')

    def compileIf(self):
        """
        :return:
        """
        self.if_label_counter += 1
        end_if_label = "EndIfl" + str(self.if_label_counter)
        # (
        self.bound(self.tokenizer.advance(), 'symbol')

        # the condition expression
        self.tokenizer.advance()
        """expression result is on the top of the stack"""
        self.compileExpression()

        """negating the top"""
        self.vm_writer.WriteArithmetic("neg")
        # )
        self.bound(self.tokenizer.advance(), 'symbol')


        """if true - skip condition statements"""
        self.vm_writer.WriteIf(end_if_label)

        # the body of if

        # {
        self.bound(self.tokenizer.advance(), 'symbol')

        # statements
        self.compileStatements()

        # }
        self.bound(self.tokenizer.advance(), 'symbol')

        # might be an else:



        if self.tokenizer.advance() is 'else':
            end_else = "Else" + str(self.if_label_counter)
            self.vm_writer.WriteGoto(end_else)
            self.vm_writer.WriteLabel(end_if_label)

            self.bound(self.token(), 'keyword')
            # {
            self.bound(self.tokenizer.advance(), 'symbol')

            # statements
            self.compileStatements()

            self.vm_writer.WriteLabel(end_else)

            # }
            self.bound(self.tokenizer.advance(), 'symbol')
            self.tokenizer.advance()
        else:
            self.vm_writer.WriteLabel(end_if_label)



        self.end('ifStatement')

    def compileExpression(self):
        """
        an expression is a term, followed by couples of operators and more
        terms
        :return:
        """
        self.start('expression')

        # first term
        self.compileTerm()

        # following terms and operators
        while self.tokenizer.advance() in self.OPS:
            self.bound(self.token(), 'symbol')
            self.tokenizer.advance()
            self.compileTerm()
            self.tokenizer.advance()

        self.end('expression')

    def compileTerm(self):
        """
        :return:
        """
        self.start('term')
        self.tokenizer.advance()
        token_type = self.tokenizer.getType()
        if token_type is 'integerConstant' or \
                'stringConstant' or \
                'keywordConstant':
            self.bound(self.token(), self.tokenizer.getType())
        # expression
        elif self.token() is '(':
            # (
            self.bound(self.token(), 'symbol')
            # thats an expression
            self.tokenizer.advance()
            self.compileExpression()
            # )
            self.bound(self.tokenizer.advance(), 'symbol')
        # unary operator
        elif self.token() in ['-', '~']:
            self.bound(self.token(), 'symbol')
            self.tokenizer.advance()
            self.compileTerm()


        # subroutine/array/variable
        elif token_type is 'identifier':
            # variable
            self.bound(self.token(), 'identifier')
            self.tokenizer.advance()
            # subroutine
            if self.token() in ['(', '.']:
                self.compileSubroutineCall()
            # array
            elif self.token() is '[':
                # [
                self.bound(self.token(), 'symbol')
                self.tokenizer.advance()
                self.compileExpression()
                # ]
                self.bound(self.tokenizer.advance(), 'symbol')
                self.tokenizer.advance()

        self.end('term')

    def compileExpressionList(self):
        """
        :return:
        """
        self.start('expressionList')
        self.compileExpression()
        while self.tokenizer.advance() is ',':
            self.bound(self.token(), 'symbol')
            self.tokenizer.advance()
            self.compileExpression()
            self.tokenizer.advance()

        self.end('expressionList')