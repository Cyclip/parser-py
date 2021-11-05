
import logging
from exceptions import ParseException
from instructions import instrFor

class Parser:
    """
    Grammar:
        exp     ::= term op exp | term
        op      ::= / | * | + | -
        term    ::= number | (exp)
            * implement parenthesis
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = tokens[0]
        self.__logger = logging.getLogger("parserLog")

    def parse(self):
        return self.exp()


    """Grammar mechanics"""
    def incrPos(self):
        """Go to the next token"""
        self.tokens = self.tokens[1:]
        self.current = self.tokens[0] if len(self.tokens) > 0 else None
      
    def incrPosReturn(f):
        """
        Decorator to increase position upon grammar rule return
        Implemented as a decorator to incrPos() after returning
        so it does not affect the return value.
        """
        def wrapper(*args):
            self = args[0]

            if self.current is None:
                return None

            rv = f(*args)
            self.__logger.debug(f"{self.current} returns {rv} \t{[str(i) for i in self.tokens]}")
            self.incrPos()
            return rv

        return wrapper

    """Grammar"""
    @incrPosReturn
    def exp(self):
        data = {"type": "exp"}

        try:
            # term 1
            self.__logger.debug("Getting term1")
            data['term1'] = self.term()
            
            if len(self.tokens) >= 2:
                # if there are atleast 2 tokens remaining, it should be a full exp
                self.__logger.debug("Getting operator")
                # find operator (ors)
                data['op'] = self.op()
            
                self.__logger.debug(f"Getting term2 - {len(self.tokens)} left")
                # term 2
                data['term2'] = self.exp()
            else:
                self.__logger.debug(f"Transforming {data} => term\nCurrent: {self.current}")
                # transform exp into term
                data = data['term1']
                self.__logger.debug(f"Transformed to {data}")
        except IndexError:
            raise ParseException(f"Invalid syntax at end")

        return data
    
    @incrPosReturn
    def op(self):
        self.__logger.debug("op " + str(self.current))
        if self.current.type in ("DIV", "MULT", "PLUS", "MINUS"):
            return {
                "type": "op",
                "val": self.current.type
            }

        raise ParseException(f"Unknown operator token \"{self.current.val}\"")
    
    @incrPosReturn
    def term(self):
        self.__logger.debug("term " + str(self.current))
        if self.current.type == "NUMBER":
            return {
                "type": self.current.type,
                "val": self.current.val
            }
        
        # must be exp
        return {
            "type": self.current.type,
            "val": self.exp()
        }
