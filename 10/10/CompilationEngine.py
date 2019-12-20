class CompilationEngine:
    CLASS_VARIABLES = ['static', 'field']
    SUBROUTINE_TYPES = ['constructor', 'method', 'function']
    TYPES = ['int', 'char', 'boolean']
    STATEMENTS = {'do', 'let', 'if', 'while', 'return'}
    OPS = ['+', '-', '*', '/', '&', ',', '<', '>', '=']
    EX_OPS = ['+', '-', '*', '/', '&', '<', '>','|','=']
    CONSTANTS = ['integerConstant','stringConstant','keywordConstant']

    def __init__(self, tokenizer):
        self.indent_counter= 0
        self.tokenizer = tokenizer
        self.out_file_name = tokenizer.getFileName()
        self.output_file = open(self.out_file_name + '.xml', 'w')
        self.CLASSES = []

    def out(self, phrase):
        """

        :param phrase:
        :return:
        """
        print(phrase)
        self.output_file.write('  '*self.indent_counter+phrase+'\n')

    def start(self, phrase):
        """

        :param phrase:
        :return:
        """
        self.out("<" + phrase + ">")
        self.indent_counter += 1

    def end(self, phrase):
        """

        :param phrase:
        :return:
        """
        self.indent_counter -= 1
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
        final_phrase = self.startr(ter_type)+" "+ phrase+" " + self.endr(ter_type)
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
        how do we parse a class? we start with the keyword class,
        then the class name, brackets and within them all
        variables and then the functions/methods
        :return:
        """

        # class keyword and name, start of body
        self.start('class')

        # class
        self.bound(self.token(), 'keyword')
        self.advance()

        # name
        self.bound(self.token(), 'identifier')
        self.advance()

        # {
        self.bound(self.token(), 'symbol')
        self.advance()

        # now to declare all class variables

        while self.token() in self.CLASS_VARIABLES:
            self.compileClassVarDec()

        # now to declare all methods

        while self.token() in self.SUBROUTINE_TYPES:
            self.compileSubroutine()



        # }
        self.bound(self.token(), 'symbol')
        if (self.tokenizer.has_more_tokens()):
            self.advance()

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
        self.bound(self.token(), 'keyword')

        self.tokenizer.advance()
        # compile type
        self.compileType()

        # names
        self.bound(self.token(), 'identifier')
        self.tokenizer.advance()
        while self.token() == ',':
            self.bound(self.token(), 'symbol')
            self.bound(self.tokenizer.advance(), 'identifier')
            self.tokenizer.advance()

        # ;
        self.bound(self.token(), 'symbol')
        self.end('classVarDec')
        if self.tokenizer.has_more_tokens():
            self.advance()

    def compileType(self):
        """

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
        self.bound(self.token(), 'keyword')
        self.advance()

        # function return type
        if self.token() == 'void':
            self.bound(self.token(), 'keyword')
            self.advance()
        else:
            self.compileType()

        # function variables

        # name
        self.bound(self.token(), 'identifier')
        self.advance()

        # (
        self.bound(self.token(), 'symbol')

        # parameter list
        self.advance()
        self.compileParameterList()

        # )
        self.bound(self.token(), 'symbol')
        self.advance()

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
        if self.token() == ')':
            self.start('parameterList')
            self.end('parameterList')
            return

        else:
            self.start('parameterList')

            # type
            self.compileType()
            # name
            self.bound(self.token(), 'identifier')
            self.advance()

            # other parameters

            while self.token() == ',':
                self.bound(self.token(), 'symbol')
                self.advance()
                self.compileType()
                self.bound(self.token(), 'identifier')
                self.advance()

            self.end('parameterList')

    def compileSubroutineBody(self):
        self.start('subroutineBody')

        # {
        self.bound(self.token(), 'symbol')
        self.advance()

        while self.token() == 'var':
            self.start('varDec')
            self.bound(self.token(), 'keyword')
            self.advance()
            self.compileVarDec()

        self.compileStatements()

        # }
        print ("****************************")
        self.bound(self.token(), 'symbol')
        self.advance()
        self.end('subroutineBody')

    def compileVarDec(self):
        """
        declaring a var in a function starts with keyword 'var' then the type
        and then the name. can also be followed by commas and more names, ends
        with ';'
        :return:
        """

        # type
        self.compileType()

        # name
        self.bound(self.token(), 'identifier')
        self.advance()

        while self.token() == ',':
            self.bound(self.token(), 'symbol')
            self.advance()
            self.bound(self.token(), 'identifier')
            self.advance()

        # ;
        self.bound(self.token(), 'symbol')
        if self.tokenizer.has_more_tokens():
            self.advance()

        self.end('varDec')

    def compileStatements(self):
        """
        compiles all following statements in a loop
        :return:
        """

        self.start('statements')

        while self.token() in self.STATEMENTS:
            self.compileStatement()

        self.end('statements')
        print('********',self.token())


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

        self.start('doStatement')

        # do
        self.bound(self.token(), 'keyword')
        self.tokenizer.advance()

        # call subroutine
        self.bound(self.token(), 'identifier')
        self.tokenizer.advance()

        self.compileSubroutineCall()

        # ;
        self.bound(self.token(), 'symbol')
        self.advance()
        self.end('doStatement')

    def compileSubroutineCall(self):
        """

        :return:
        """

        # handling after the first identifier , advanced after it

        # ( or .
        # if .
        if self.token() == '.':
            # .
            self.bound(self.token(), 'symbol')
            self.advance()
            # name of subroutine
            self.bound(self.token(), 'identifier')
            self.advance()


        # (
        self.bound(self.token(), 'symbol')
        # expression list
        self.tokenizer.advance()
        self.compileExpressionList()
        # )
        self.bound(self.token(), 'symbol')
        self.advance()

    def compileLet(self):
        """
        assignment, 'let', then a varname (with an expression in brackets if
        its an array) then '=' and then another expression. ends with ';'
        :return:
        """

        self.start('letStatement')

        # let
        self.bound(self.token(), 'keyword')
        self.advance()

        # varname
        self.bound(self.token(), 'identifier')
        self.advance()

        # might be an array, need to check that
        if self.token() == '[':
            # [
            self.bound(self.token(), 'symbol')
            self.tokenizer.advance()
            self.compileExpression()
            # ]
            self.bound(self.token(), 'symbol')
            self.tokenizer.advance()

        # otherwise its a =
        self.bound(self.token(), 'symbol')
        self.tokenizer.advance()

        # then an expression
        self.compileExpression()

        # ;
        self.bound(self.token(), 'symbol')
        self.advance()
        self.end('letStatement')

    def compileWhile(self):
        """

        :return:
        """
        self.start('whileStatement')
        # while
        self.bound(self.token(), 'keyword')
        self.advance()

        # (
        self.bound(self.token(), 'symbol')
        self.advance()

        # the condition expression
        self.compileExpression()
        # )
        self.bound(self.token(), 'symbol')
        self.advance()

        # the body of while

        # {
        self.bound(self.token(), 'symbol')
        self.advance()

        # statements
        self.compileStatements()

        # }
        self.bound(self.token(), 'symbol')
        self.advance()

        self.end('whileStatement')

    def compileReturn(self):
        """

        :return:
        """
        self.start('returnStatement')
        # return
        self.bound(self.token(), 'keyword')
        self.advance()

        # expression (might be empty)
        if self.token() != ';':
            self.compileExpression()

        # ;
        self.bound(self.token(), 'symbol')
        self.advance()
        self.end('returnStatement')

    def compileIf(self):
        """

        :return:
        """
        self.start('ifStatement')
        self.bound(self.token(), 'keyword')
        self.advance()

        # (
        self.bound(self.token(), 'symbol')
        self.advance()

        # the condition expression
        self.compileExpression()
        # )
        self.bound(self.token(), 'symbol')
        self.advance()
        # the body of if

        # {
        self.bound(self.token(), 'symbol')
        self.advance()

        # statements
        self.compileStatements()

        # }
        self.bound(self.token(), 'symbol')
        self.advance()

        # might be an else:

        if self.token() == 'else':
            self.bound(self.token(), 'keyword')
            self.advance()

            # {
            self.bound(self.token(), 'symbol')
            self.advance()

            # statements
            self.compileStatements()

            # }
            self.bound(self.token(), 'symbol')
            self.advance()

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
        while self.token() in self.EX_OPS:
            self.bound(self.token(), 'symbol')
            self.advance()
            self.compileTerm()

        self.end('expression')

    def compileTerm(self):
        """

        :return:
        """
        self.start('term')
        token_type = self.tokenizer.get_token_type()
        if token_type in self.CONSTANTS:
            self.bound(self.token(), self.tokenizer.get_token_type())
            self.advance()
        # expression
        elif self.token() is '(':
            # (
            self.bound(self.token(), 'symbol')
            self.advance()
            # thats an expression
            self.compileExpression()
            # )
            self.bound(self.token(), 'symbol')
            self.advance()

        # unary operator and a term
        elif self.token() in ['-', '~']:
            self.bound(self.token(), 'symbol')
            self.advance()
            self.compileTerm()

        elif token_type is 'keyword':
            print("here is a keyword!!",self.token())
            self.bound(self.token(), 'keyword')
            self.advance()



    # subroutine/array/variable
        elif token_type is 'identifier':
            # variable
            self.bound(self.token(), 'identifier')
            self.advance()
            # subroutine
            if self.token() in ['(', '.']:

                self.compileSubroutineCall()
            # array
            elif self.token() is '[':
                # [
                self.bound(self.token(), 'symbol')
                self.advance()
                self.compileExpression()
                # ]
                self.bound(self.token(), 'symbol')
                self.advance()

        self.end('term')

    def compileExpressionList(self):
        """

        :return:
        """
        self.start('expressionList')
        if self.token() != ')':
            self.compileExpression()
            while self.token() is ',':
                self.bound(self.token(), 'symbol')
                self.tokenizer.advance()
                self.compileExpression()

        self.end('expressionList')
