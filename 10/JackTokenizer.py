


class JackTokenizer:

    def __init__ (self, input_file_name):

        with open(input_file_name) as input_file:
            self.input_string = input_file.read()

        # split it into meaningful lines
        self.input_list = self.input_string.split(';')




    def has_more_tokens(self):

    def advance(self):

    def token_type(self):

    def key_word(self):

    def symbol(self):

    def identifier(self):

    def int_val(self):

    def string_val(self):
