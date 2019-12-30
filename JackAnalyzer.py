import sys
import os
import tokenizer2
import CompilationEngine


def analyze_file(given_file):
    """
    creates a tokenizer for the given file, extracts all tokens
    and...
    :param given_file: a jack file
    :return: None
    """
    cur_tokenizer = tokenizer2.Tokenizer(given_file)
    engine = CompilationEngine.CompilationEngine(cur_tokenizer)
    engine.compile()
    # while cur_tokenizer.has_more_tokens():
    #     cur_tokenizer.advance()
    #     print(cur_tokenizer.token)
    #     print("<",cur_tokenizer.token_type,">")


if __name__ == "__main__":
    path = sys.argv[1].rsplit(".", 1)[0]
    output_file_path = path+".xml"
    if os.path.isdir(sys.argv[1]):
        for current_file in os.listdir(sys.argv[1]):
            if current_file.endswith(".jack"):
                analyze_file(path+'/'+current_file)
    else:
        analyze_file(sys.argv[1])
