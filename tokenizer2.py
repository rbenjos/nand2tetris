import re


class Tokenizer:
    def __init__(self, input_file):
        """
        A constructor of a tokenizer. Mainly prepares the input as
        a list to work with.
        :param input_file: a jack file to read the jack code from
        """
        file_content = None
        self.input_file_name = input_file

        # opening the input jack file
        print("file is  "+input_file)
        file = open(input_file, "r")
        if file.mode == "r":
            # extracting the entire text
            self.file_content = file.read()

            # removing jack documentation
            self.file_content = re.sub(r"(/{2}.*?\n)", "",file_content)
            self.file_content = re.sub(r"/\*{1,2}(.|\n)*?\*/", "", file_content, re.DOTALL)
            print(file_content)
        file.close()

        # creating a list and filtering the list from empty strings
        if self.file_content is not None:

            # setting other variables
            self.token_type = None
            self.token = None
            self.inside_string = False
            self.word = ""
            self.key_words = {"class", "constructor", "function", "method",
                              "field", "static", "var", "int", "char", "true",
                              "boolean", "void", "false", "null", "this",
                              "let", "do", "if", "else", "while", "return"}

            self.symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+",
                            "-", "*", "/", "&", "|", "<", ">", "=", "~"}
            self.double_symbols = {"<=", ">=", "!="}#todo

    def get_token(self):
        return self.token

    def get_token_type(self):
        return self.token_type

    def has_more_tokens(self):
        """
        :return: true if there are more tokens in the file,
        false otherwise
        """
        return self.file_content != ""

    def set_word(self, cut):
        self.token = self.word[:cut]
        self.word = self.word[cut:]

    def extract_token(self):
        if self.symbols.__contains__(self.word[0]):
            if self.double_symbols.__contains__(self.word[:2]):
                cut_index = 2
            else:
                cut_index = 1
            self.token_type = "symbol"

        else:
            text = re.search("^[a-zA-Z_][a-zA-Z_\\d]*", self.word, re.MULTILINE)
            if text is not None:
                if self.key_words.__contains__(text.group()):
                    self.token_type = "keyword"
                else:
                    self.token_type = "identifier"
                cut_index = text.span()[1]+1
            else:
                text = re.search("^\\d+", self.word, re.MULTILINE)
                if text is not None:
                    self.token_type = "integerConstant"
                    cut_index = text.span()[1]+1
        self.set_word(cut_index)

    def advance(self):
        if self.word != "" or self.word != " " or self.word != "\n":
            self.extract_token()
        else:
            if self.inside_string and self.token == "\"":
                string_content = re.search("[^\"]*", self.file_content)
                self.token = string_content.group()
                self.token_type = "stringConstant"
                self.file_content = self.file_content[string_content.span()[1]:]

            elif self.has_more_tokens():
                separator = re.search(" |\n|\"", self.file_content)
                if separator.group() == "\"":
                    self.inside_string = not self.inside_string
                    cut_at = separator.span()[0]+1
                    self.word = self.file_content[:cut_at]
                    self.file_content = self.file_content[cut_at:]
                else:
                    cut_at = separator.span()[0]
                    self.word = self.file_content[:cut_at]
                    self.file_content = self.file_content[cut_at+1:]
                self.extract_token()


