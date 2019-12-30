import re


class Tokenizer:
    def __init__(self, input_file):
        """
        A constructor of a tokenizer. Mainly prepares the input as
        a list to work with.
        :param input_file: a jack file to read the jack code from
        """
        self.input_file_name = input_file

        # opening the input jack file
        print("file is  " + input_file)
        file = open(input_file, "r")
        if file.mode == "r":
            # extracting the entire text
            self.file_content = file.read()

        self.key_words = {"class", "constructor", "function", "method",
                          "field", "static", "var", "int", "char", "true",
                          "boolean", "void", "false", "null", "this",
                          "let", "do", "if", "else", "while", "return"}

        self.symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+",
                        "-", "*", "/", "&", "|", "<", ">", "=", "~"}

        self.spacers = {' ', '\n', '\t'}

        # flags
        self.inside_string = False
        self.inside_comment = False
        self.inside_multiLine = False
        self.pointer = 0
        self.word = ""
        self.token = None
        self.token_type = None
        self.tokens = []
        if self.file_content is not None:
            self.create_list()
        self.advance()


    def create_list(self):
        symbols = []
        for letter in self.file_content:
            if self.inside_string:
                if letter != "\"":
                    self.word += letter
                else:
                    self.tokens.append(self.word)
                    self.inside_string = False
                    self.tokens.append(letter)
                    self.word = ''

            elif self.inside_multiLine:
                self.word += letter
                if self.word.endswith('*/'):
                    self.word = ''
                    self.inside_multiLine = False

            elif self.inside_comment:
                if letter == "\n":
                    self.inside_comment = False

            elif letter in self.spacers:
                self.tokens.append(self.word)
                self.word = ''

            elif letter in self.symbols|{"\""}:
                if letter == '\"':
                    self.tokens.append(letter)
                    self.inside_string = True
                elif letter == "/":
                    if self.word!= '':
                        self.tokens.append(self.word)
                        self.word = ''
                    self.tokens.append(letter)
                    if self.tokens[-2:] == ['/', '/']:
                        self.inside_comment = True
                        self.word = ''
                        self.tokens = self.tokens[:-2]
                elif letter == "*":
                    self.tokens.append(letter)
                    if self.tokens[-2:] == ['/', '*']:
                        self.inside_multiLine = True
                        self.word = ''
                        self.tokens = self.tokens[:-2]
                else:
                    self.tokens.append(self.word)
                    self.tokens.append(letter)
                    self.word = ''

            else:
                self.word += letter
        self.tokens = [token for token in self.tokens if token != '']
        print(self.tokens)



    def getFileName(self):
        return self.input_file_name

    def get_token(self):
        return self.token

    def get_token_type(self):
        return self.token_type

    def has_more_tokens(self):
        """
        :return: true if there are more tokens in the file,
        false otherwise
        """
        return self.pointer != len(self.tokens)

    # def set_word(self, cut):
    #     self.token = self.word[:cut]
    #     self.word = self.word[cut:]

    # def extract_token(self):
    #     if self.symbols.__contains__(self.word[0]):
    #         if self.double_symbols.__contains__(self.word[:2]):
    #             cut_index = 2
    #         else:
    #             cut_index = 1
    #         self.token_type = "symbol"
    #
    #     else:
    #         text = re.search("^[a-zA-Z_][a-zA-Z_\\d]*", self.word, re.MULTILINE)
    #         if text is not None:
    #             if self.key_words.__contains__(text.group()):
    #                 self.token_type = "keyword"
    #             else:
    #                 self.token_type = "identifier"
    #             cut_index = text.span()[1]+1
    #         else:
    #             text = re.search("^\\d+", self.word, re.MULTILINE)
    #             if text is not None:
    #                 self.token_type = "integerConstant"
    #                 cut_index = text.span()[1]+1
    #     self.set_word(cut_index)

    def advance(self):
        if self.has_more_tokens():
            self.token = self.tokens[self.pointer]
            while self.token == "\"":
                self.pointer += 1
                self.token = self.tokens[self.pointer]
            if self.tokens[self.pointer - 1] == "\"" and self.tokens[self.pointer + 1] == "\"":
                self.token_type = "stringConstant"
            elif self.token in self.symbols:
                self.token_type = "symbol"
            elif self.token in self.key_words:
                self.token_type = "keyword"
            else:
                text = re.search("^[a-zA-Z_][a-zA-Z_\\d]*", self.token)
                if text is not None:
                    self.token_type = "identifier"
                else:
                    text = re.search("^\\d+", self.token)
                    if text is not None:
                        self.token_type = "integerConstant"
            self.pointer += 1
            return self.token

        # if self.word != "" or self.word != " " or self.word != "\n":
        #     self.extract_token()
        # else:
        #     if self.inside_string and self.token == "\"":
        #         string_content = re.search("[^\"]*", self.file_content)
        #         self.token = string_content.group()
        #         self.token_type = "stringConstant"
        #         self.file_content = self.file_content[string_content.span()[1]:]
        #
        #     elif self.has_more_tokens():
        #         separator = re.search(" |\n|\"", self.file_content)
        #         if separator.group() == "\"":
        #             self.inside_string = not self.inside_string
        #             cut_at = separator.span()[0]+1
        #             self.word = self.file_content[:cut_at]
        #             self.file_content = self.file_content[cut_at:]
        #         else:
        #             cut_at = separator.span()[0]
        #             self.word = self.file_content[:cut_at]
        #             self.file_content = self.file_content[cut_at+1:]
        #         self.extract_token()
