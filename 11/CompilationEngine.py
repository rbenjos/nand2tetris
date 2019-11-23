import re
import symbolTable
import VMWriter


class CompilationEngine:
    CLASS_VARIABLES = ['static', 'field']
    SUBROUTINE_TYPES = ['constructor', 'method', 'function']
    TYPES = ['int', 'char', 'boolean']
    STATEMENTS = {'do', 'let', 'if', 'while', 'return'}
    BIN_OPS = ['+', '-', '&', '<', '>', '=','|']
    CONSTANTS = ['integerConstant', 'stringConstant', 'keywordConstant']

    def __init__(self, tokenizer, output_name):
        self.classTable = symbolTable.SymbolTable()
        self.subRoutineTable = symbolTable.SymbolTable()
        self.vm_writer = VMWriter.VMWriter(output_name)
        self.tokenizer = tokenizer
        self.out_file_name = tokenizer.getFileName()
        self.output_file = open(self.out_file_name + '.xml', 'w')
        self.CLASSES = []

        self.class_name = None

        self.if_label_counter = 0
        self.while_label_counter = 0

    def out(self, phrase):
        """

        :param phrase:
        :return:
        """
        print(phrase)
        self.output_file.write(phrase + '\n')

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

    def startr(self, phrase):
        """

        :param phrase:
        :return:
        """
        return "<" + phrase + ">"

    def endr(self, phrase):
        """

        :param phrase:
        :return:
        """
        return "</" + phrase + ">"

    def bound(self, phrase, ter_type):
        """

        :param phrase:
        :param ter_type:
        :return:
        """
        final_phrase = self.startr(ter_type) + phrase + self.endr(ter_type)
        self.out(final_phrase)

    def token(self):
        return self.tokenizer.get_token()

    def token_type(self):
        return self.tokenizer.get_token_type()

    def advance(self):
        return self.tokenizer.advance()

    def compile(self):
        self.advance()
        self.CompileClass()

    def CompileClass(self):
        """
        **Done!**
        how do we parse a class? we start with the keyword class,
        then the class name, brackets and within them all
        variables and then the functions/methods
        :return:
        """

        # class keyword and name, start of body

        # class
        self.advance()

        # name
        self.class_name = self.token()
        self.advance()

        # {
        self.advance()

        # now to declare all class variables

        while self.token() in self.CLASS_VARIABLES:
            self.compileClassVarDec()

        # now to declare all methods

        while self.token() in self.SUBROUTINE_TYPES:
            self.compileSubroutine()

        # }
        self.advance()

        self.vm_writer.close()

    def compileClassVarDec(self):
        """
        **Done!**
        a variable or variables start with static or field,
        then their type, then their name, and a ',' with more
        potential varnames. ends with a ';'
        :return:
        """

        # class var dec

        # field? static?
        kind = self.token()
        self.advance()

        # compile type
        type_of_var = self.token()
        self.advance()

        # self.compileType()
        # todo: find out if compiling an object dec is different then a primitive

        # names
        name = self.token()
        self.classTable.define(name, type_of_var, kind)
        self.advance()

        while self.token() == ',':
            # ,
            self.advance()
            # name
            name = self.token()

            self.classTable.define(name, type_of_var, kind)
            self.advance()

        # ;
        if self.tokenizer.has_more_tokens():
            self.advance()

    def compileType(self):
        """
        DEPRECATED!!!
        :return:
        """
        token = self.token()
        if token in self.TYPES:
            self.bound(token, 'keyword')

        else:
            self.bound(token, 'identifier')

        self.advance()

    def compileSubroutine(self):
        """
        **DONE!**
        a subroutine decleration start with a keyword of the following:
        ['constructor','function','method'], then the return type ['void',type]
        then the subroutine name, the parameter list within parentheses and
        then the subroutine body
        :return:
        """

        # subroutine

        # function/method/constructor
        kind = self.token()
        self.advance()

        # function return type

        type_of_sub = self.token()
        self.advance()

        # name
        name = self.token()
        self.advance()

        # (

        # parameter list
        self.advance()
        nvars = self.compileParameterList()

        # )
        self.advance()

        # subroutine body
        self.compileSubroutineBody(nvars, name)

    def compileParameterList(self):
        """
        **done!**
        the parameter list is potentially empty, but has couples of types
        and varnames with ',' between them
        :return:
        """
        nvars = 0

        # if there are no parameters, we should go back
        if self.token() == ')':
            return nvars

        else:

            nvars += 1

            # type

            # self.compileType()
            # todo: find out about object types

            type_of_arg = self.token()
            self.advance()

            # name
            name = self.token()

            self.subRoutineTable.define(name, type_of_arg, 'ARG')
            self.advance()

            # other parameters

            while self.token() == ',':
                # ,
                self.advance()

                nvars += 1

                # type
                # self.compileType()
                # todo: find out about object types
                type_of_arg = self.token()
                self.advance()

                # name
                name = self.token()
                self.subRoutineTable.define(name, type_of_arg, 'ARG')
                self.advance()

            return nvars

    def compileSubroutineBody(self, nvars, name):
        """

        :return:
        """

        # {
        self.advance()

        self.vm_writer.writeFunction(self.class_name + '.' + name, nvars)

        while self.token() == 'var':
            self.advance()
            self.compileVarDec()

        self.compileStatements()

        # }
        self.advance()

    def compileVarDec(self):
        """
        declaring a var in a function starts with keyword 'var' then the type
        and then the name. can also be followed by commas and more names, ends
        with ';'
        :return:
        """
        # type
        type_of_var = self.token()
        self.advance()

        # name
        name = self.token()
        self.advance()

        self.subRoutineTable.define(name, type_of_var, 'VAR')

        while self.token() == ',':
            self.advance()

            # type

            # name
            name = self.token()
            self.advance()

            self.subRoutineTable.define(name, type_of_var, 'VAR')


        # ;
        if self.tokenizer.has_more_tokens():
            self.advance()

    def compileStatements(self):
        """
        compiles all following statements in a loop
        :return:
        """
        while self.token() in self.STATEMENTS:
            self.compileStatement()

    def compileStatement(self):
        """
        compiles statement based on its keyword
        :return:
        """

        if self.token() == 'do':
            self.compileDo()
        elif self.token() == 'let':
            self.compileLet()
        elif self.token() == 'if':
            self.compileIf()
        elif self.token() == 'while':
            self.compileWhile()
        elif self.token() == 'return':
            self.compileReturn()

    def compileDo(self):
        """
        calls a subroutine, keyword 'do' then a subroutine call
        :return:
        """

        # do
        self.advance()

        name = self.token()
        self.advance()

        # call subroutine
        self.compileSubroutineCall(name)

        # always void, pop to temp

        self.vm_writer.writePop('temp', 0)

        # ;
        self.advance()

    def compileSubroutineCall(self,first_name):
        """

        :return:
        """
        second_name = None
        seg = None
        index = None
        counter = 0

        if self.subRoutineTable.contains(first_name):
            seg = self.subRoutineTable.kindOf(first_name)
            index = self.subRoutineTable.indexOf(first_name)

        elif self.classTable.contains(first_name):
            seg = self.classTable.kindOf(first_name)
            index = self.classTable.indexOf(first_name)

        else:
            seg = 'pointer'
            index = 0

        # handling after the first identifier , advanced after it

        # ( or .
        # if .
        full_name = first_name

        if self.token() == '.':
            full_name += '.'
            # .
            self.advance()
            # name of subroutine
            second_name = self.token()
            full_name += second_name

            self.advance()

        print(second_name)
        if second_name is not None:




            self.vm_writer.writePush(seg, index)
            counter += 1

        else:
            print(2)
            full_name = self.class_name + '.' + first_name
            self.vm_writer.writePush('pointer', 0)
            counter += 1

        # (
        # expression list
        self.advance()
        counter += self.compileExpressionList()

        # )
        self.advance()
        self.vm_writer.writeCall(full_name, counter)

    def compileLet(self):
        """
        assignment, 'let', then a varname (with an expression in brackets if
        its an array) then '=' and then another expression. ends with ';'
        :return:
        """
        # let
        self.advance()

        # varname

        lastLineSeg = None
        lastLineindex = None

        isArray = False

        print(self.subRoutineTable)
        print(self.token())
        # finding identifier in tables

        if self.subRoutineTable.contains(self.token()):
            lastLineSeg = self.subRoutineTable.kindOf(self.token())
            lastLineindex = self.subRoutineTable.indexOf(self.token())
            print(lastLineindex,lastLineSeg)

        elif self.classTable.contains(self.token()):
            lastLineSeg = self.classTable.kindOf(self.token())
            lastLineindex = self.classTable.indexOf(self.token())
        else:
            print("identifier doesn't exist")
        # might be an array, need to check that

        self.advance()

        if self.token() is '[':
            isArray = True
            # [

            """pushing array base address"""
            self.vm_writer.writePush(lastLineSeg, lastLineindex)
            self.advance()

            """push expression result"""  # todo - make sure expression leaves the result on the top of the stack
            self.compileExpression()
            # ]

            """adding the base address and the expression result"""
            self.advance()

            self.vm_writer.WriteArithmetic("+", False)
            """poping the result to temp 0 so we will get access to the previous addition result"""
            self.vm_writer.writePop("temp", 0)

        # otherwise its a =
        # then an expression
        self.advance()

        """calculating the expression"""  # todo-make sure expression leaves the result on the top of the stack
        self.compileExpression()



        # ;
        """if the value should be put in an array then pop the expression result to that 0"""

        if isArray:
            """poping to pointer 1(that) so that 0 will hold the required array cell"""
            self.vm_writer.writePush("temp", 0)
            self.vm_writer.writePop("pointer", 1)
            self.vm_writer.writePop("that", 0)
        else:
            """if not then pop the expression result to the given address"""
            self.vm_writer.writePop(lastLineSeg, lastLineindex)

    def compileWhile(self):
        """
        :return:
        """
        self.while_label_counter += 1
        while_label = "While_Loop_" + str(self.while_label_counter)
        end_while_label = "End_Of_while_" + str(self.while_label_counter)
        # while
        self.advance()

        # (
        self.advance()

        # the condition expression

        self.vm_writer.WriteLabel(while_label)

        """make sure the result is on the top of the stack"""
        self.compileExpression()
        # )
        self.vm_writer.WriteArithmetic("~",True)
        self.advance()

        """creating if condition"""
        self.vm_writer.WriteIf(end_while_label)

        # the body of while

        # {
        self.advance()

        # statements
        self.compileStatements()
        self.vm_writer.WriteGoto(while_label)
        self.vm_writer.WriteLabel(end_while_label)

        # }
        self.advance()

    def compileReturn(self):
        """
        :return:
        """
        # return
        self.advance()

        # expression (might be empty)

        if self.token() is not ';':
            self.compileExpression()

        else:
            self.vm_writer.writePush("constant", 0)
        self.vm_writer.writeReturn()

        # ;
        self.advance()

    def compileIf(self):
        """
        :return:
        """

        # if
        self.advance()

        self.if_label_counter += 1
        end_if_label = "EndIf_" + str(self.if_label_counter)

        # (
        self.advance()

        # the condition expression
        self.tokenizer.advance()
        """expression result is on the top of the stack"""
        self.compileExpression()

        """negating the top"""
        self.vm_writer.WriteArithmetic("~",True)
        # )
        self.advance()

        """if true - skip condition statements"""
        self.vm_writer.WriteIf(end_if_label)

        # the body of if

        # {
        self.advance()

        # statements
        self.compileStatements()

        # }
        self.advance()

        # might be an else:

        if self.token() is 'else':
            end_else = "Else_" + str(self.if_label_counter)
            self.vm_writer.WriteGoto(end_else)
            self.vm_writer.WriteLabel(end_if_label)

            self.advance()
            # {
            self.advance()

            # statements
            self.compileStatements()

            self.vm_writer.WriteLabel(end_else)

            # }
            self.advance()
        else:
            self.vm_writer.WriteLabel(end_if_label)

    def compileExpression(self):
        """
        ** done!! **
        an expression is a term, followed by couples of operators and more
        terms
        :return:
        """

        # first term
        self.compileTerm()

        # following terms and operators
        operator = self.token()
        if operator in self.BIN_OPS:
            self.advance()
            self.compileTerm()
            self.vm_writer.WriteArithmetic(operator,False)

        # writing the vm code for the operator


    def compileTerm(self):
        """

        :return:
        """
        token_type = self.tokenizer.get_token_type()
        if token_type in self.CONSTANTS:
            self.vm_writer.writePush('constant',self.token())
            self.advance()

        # expression
        elif self.token() is '(':
            # (
            self.advance()

            # thats an expression
            self.compileExpression()

            # )
            self.advance()

        # unary operator and a term
        elif self.token() in ['-', '~']:
            operator = self.token()
            self.advance()
            self.compileTerm()
            self.vm_writer.WriteArithmetic(operator,True)

        # subroutine/array/variable
        elif token_type is 'identifier':
            name = self.token()
            lastLineSeg = None
            lastLineindex = None


            print(self.token()+'1111111')
            # finding identifier in tables
            if self.subRoutineTable.contains(name):
                lastLineSeg = self.subRoutineTable.kindOf(name)
                lastLineindex = self.subRoutineTable.indexOf(name)

            elif self.classTable.contains(name):
                lastLineSeg = self.classTable.kindOf(name)
                lastLineindex = self.classTable.indexOf(name)
            else:
                print("identifier doesn't exist")

            # variable
            self.advance()
            # subroutine

            if self.token() in ['(', '.']:
                self.compileSubroutineCall(name)
            # array
            elif self.token() is '[':
                # [
                self.advance()

                """pushing array base address"""
                self.vm_writer.writePush(lastLineSeg, lastLineindex)

                """push expression result"""  # todo - make sure expression leaves the result on the top of the stack
                self.compileExpression()
                # ]

                """adding the base address and the expression result"""
                self.advance()

                self.vm_writer.WriteArithmetic("+",False)

                self.vm_writer.writePop("pointer", 1)
                self.vm_writer.writePush("that", 0)
            else:
                # just a variable
                self.vm_writer.writePush(lastLineSeg, lastLineindex)


    def compileExpressionList(self):
        """
        todo: might need to add a counter and return as this
        todo: tells the subroutine the number of arguments called
        todo: easily
        :return:
        """
        counter = 0

        if self.token() == ')':
            return counter

        self.compileExpression()
        counter += 1

        while self.token() is ',':
            # ,
            self.advance()
            self.compileExpression()
            counter += 1

        self.advance()
        return counter
