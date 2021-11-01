class ParentParsingException(Exception):
    """Main parsing exception

    Args:
        Exception (Exception): Main parsing exception
    """
    def __init__(self, message, string=None, index=None):
        if message is None or index is None:
            super().__init__(message)
        else:
            string = message.split("\n")
        
            c = 0
            for item in string:
                length = len(item)

                if c + length >= index:
                    print(index, length)
                    indicatorText = f"{item}\n{' ' * (14 + length - index)}^"
                    break
                else:
                    c += length

            super().__init__(f"{message}\nLocated here:\n{indicatorText}")


class TokenizerException(ParentParsingException):
    """Called when there's an error while tokenizing"""
    pass

class ParseException(ParentParsingException):
    """Called when there's an error while parsing tokens"""
    pass