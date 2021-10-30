from tokens import Token
from exceptions import TokenizerException

class Tokenizer:
    KEYWORDS = {
        
    }

    OPERATORS = {
        "+": "PLUS",
        "-": "MINUS",
    }

    def __init__(self, string, debug=False):
        """Construct a Tokenizer class to convert a 
        string of text into an array of tokens.

        Args:
            string (string): String of text to tokenize
        """
        self.__string = string.replace(" ", "")
        self.__len = len(self.__string)
        self.__iterlen = self.__len - 1
        self.__debug = debug
    
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
            if self.__debug: print(f"[{charIndex}/{self.__iterlen}] current \"{current}\" with char \"{char}\"")

            nextChar = self.__peek(charIndex)
            if self.__debug: print(f"nextChar: \"{nextChar}\"")

            if nextChar == " " or nextChar in self.OPERATORS.keys() or char in self.OPERATORS.keys() or nextChar == None:
                tmp = self.OPERATORS.get(char)
                if tmp is None:
                    # not an operator, must be a number
                    if current.isdigit():
                        if self.__debug: print(f"[=] Appending digit token {current}")
                        tokens.append(Token("NUMBER", val=int(current)))
                        current = ""
                    else:
                        self.__raiseException(TokenizerException, charIndex, f"Unknown token \"{current}\"")
                else:
                    if self.__debug: print(f"[=] Appending operator token \"{char}\"")
                    current = ""
                    tokens.append(Token(tmp))
            
            if self.__debug: print(f"Tokens: {tokens}\n")

            if nextChar is None:
                break

        return tokens
    
    def __peek(self, index):
        if index == self.__iterlen:
            return None
        else:
            return self.__string[index + 1]

    def __raiseException(self, exc, index, text):
        """Generate and raise an exception method pointing
        towards the origin of the error in the string

        Args:
            exc (Exception): Exception to be raised
            index (int): Index of the string
            text (string): Error information

        Raises:
            TokenizerException: [description]
        """
        string = self.__string.split("\n")
        
        c = 0
        for item in string:
            length = len(item)

            if c + length >= index:
                indicatorText = f"{item}\n{' ' * (index-length)}^"
                break
            else:
                c += length

        raise exc(f"{text}\nLocated here:\n{indicatorText}")

