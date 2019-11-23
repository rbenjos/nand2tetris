import re

KEY_WORD_START = "<keyword> "
KEY_WORD_END = " </keyword>"
SYMBOL_START = "<symbol> "
SYMBOL_END = " </symbol>"
INTEGER_START = "<integerConstant> "
INTEGER_END = " </integerConstant>"
STRING_START = "<stringConstant> "
STRING_END = " </stringConstant>"
IDENTIFIER_START = "<identifier> "
IDENTIFIER_END = " </identifier>"


class Tokenizer:

    def compress_word_list(self):
        """
        compresses the list by merging string constants that
        were separated while the text was split
        :return: None
        """
        start = None
        stop = None
        i = 0
        while i < len(self.words):
            if "\"" in self.words[i]:
                if start is None:
                    start = i
                    i += 1
                else:
                    stop = i
                    self.words = self.words[:start] + ["".join(self.words[start:stop + 1])] + self.words[stop + 1:]
                    i = start + 1
                    start = None
                    stop = None
            elif start is not None and stop is None:
                self.words[i] = self.words[i] + " "
                i += 1
            else:
                i += 1

    def __init__(self, input_file):
        """
        A constructor of a tokenizer. Mainly prepares the input as
        a list to work with.
        :param input_file: a jack file to read the jack code from
        """
        file_content = None
        self.input_file_name = input_file

        # opening the input jack file
        file = open(input_file, "r")
        if file.mode == "r":
            # extracting the entire text
            file_content = file.read()

            # removing jack documentation

            one_line = r"(//.*?\n)"
            block = r"(/[*]{2}.*?[*]{1}/)"

            file_content = re.sub(one_line, "", file_content, re.DOTALL | re.MULTILINE)
            file_content = re.sub(block, "", file_content, re.DOTALL | re.MULTILINE)

        file.close()

        # creating a list and filtering the list from empty strings
        if file_content is not None:
            self.words = re.split("\\s", file_content)
            self.words = list(filter(lambda text: text != "", self.words))
            print(self.words)

            self.compress_word_list()
            print(self.words)

        # setting other variables
        self.token_type = None
        self.token = None
        self.pointer = 0
        self.key_words = {"class", "constructor", "function", "method",
                          "field", "static", "var", "int", "char", "true",
                          "boolean", "void", "false", "null", "this",
                          "let", "do", "if", "else", "while", "return"}

        self.symbols = {"{", "}", "(", ")", "[", "]", ".", ",", ";", "+",
                        "-", "*", "/", "&", "|", "<", ">", "=", "~"}

    def get_token(self):
        return self.token

    def get_token_type(self):
        return self.token_type

    def getFileName(self):
        return self.input_file_name

    def has_more_tokens(self):
        """
        :return: true if there are more tokens in the file,
        false otherwise
        """
        return self.pointer < len(self.words)

    def result_set(self, extracted_word):
        """
        sets the required advance() result in the right format
        and sets the pointer to the next time advance() is called
        :param extracted_word: the extracted token
        :return: a string in the required format containing
        the required tokenized data
        """
        if extracted_word.group() != self.words[self.pointer]:
            indexes = extracted_word.span()
            self.words[self.pointer] = self.words[self.pointer][indexes[1]:]
        else:
            self.pointer += 1
        return extracted_word.group()

    def advance(self):
        """
        Reads the next token in the file(word list).
        :return: a string in the required format containing
        the required tokenized data
        """
        # check if word has a KeyWord token
        if self.key_words.__contains__(self.words[self.pointer]):
            self.token = self.words[self.pointer]
            self.token_type = "keyword"
            self.pointer += 1
            return self.token

        # check if word has a symbol token
        elif self.symbols.__contains__(self.words[self.pointer][0]):
            if len(self.words[self.pointer]) == 1:
                self.token = self.words[self.pointer]
                self.pointer += 1
            else:
                self.token = self.words[self.pointer][0]
                self.words[self.pointer] = self.words[self.pointer][1:]
            self.token_type = "symbol"
            return self.token

        else:
            # check if word has an Identifier token
            word = re.search("^[a-zA-Z_]+", self.words[self.pointer], re.MULTILINE)
            if word is not None:
                self.token_type = "identifier"
                self.token = self.result_set(word)
                return self.token

            # check if word has an Integer token
            word = re.search("\\d+", self.words[self.pointer])
            if word is not None:
                self.token_type = "integerConstant"
                self.token = self.result_set(word)
                return self.token

            # check if word has a String token
            word = re.search("\".*\"", self.words[self.pointer])
            if word is not None:
                self.token_type = "stringConstant"
                self.token = self.result_set(word)
                return self.token