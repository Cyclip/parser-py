import logging
from tokens import Token
from exceptions import TokenizerException

class Tokenizer:
    OPERATORS = {
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULT",
        "/": "DIV",
    }

    def __init__(self, string):
        """Construct a Tokenizer class to convert a 
        string of text into an array of tokens.

        Args:
            string (string): String of text to tokenize
        """
        self.__string = string.replace(" ", "")
        self.__len = len(self.__string)
        self.__iterlen = self.__len - 1
        self.__logger = logging.getLogger("parserlog")
    
    def tokenize(self):
        """Tokenize the currently contained string

        Returns:
            list<tokens.Token>: A list of Tokens
        """
        tokens = []
        current = ""

        for charIndex in range(self.__len):
            char = self.__string[charIndex]
            current += char
            self.__logger.debug(f"[{charIndex}/{self.__iterlen}] current \"{current}\" with char \"{char}\"")

            nextChar = self.__peek(charIndex)
            self.__logger.debug(f"nextChar: \"{nextChar}\"")

            if nextChar == " " or nextChar in self.OPERATORS.keys() or char in self.OPERATORS.keys() or nextChar == None:
                tmp = self.OPERATORS.get(char)
                if tmp is None:
                    # not an operator, must be a number
                    if current.isdigit():
                        self.__logger.debug(f"[=] Appending digit token {current}")
                        tokens.append(Token("NUMBER", val=int(current)))
                        current = ""
                    else:
                        raise TokenizerException(f"Unknown token \"{current}\"", string=self.__string, index=charIndex)
                else:
                    self.__logger.debug(f"[=] Appending operator token \"{char}\"")
                    current = ""
                    tokens.append(Token(tmp))
            
            self.__logger.debug(f"Tokens: {tokens}\n")

            if nextChar is None:
                break

        return tokens
    
    def __peek(self, index):
        if index == self.__iterlen:
            return None
        else:
            return self.__string[index + 1]