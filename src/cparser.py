
import logging
from exceptions import ParseException
from instructions import instrFor

class Parser:
    """
    Grammar:
        <exp>       ::= <term> + <term> | <term> - <term> | term
        <term>      ::= <factor> * <term> | <factor> / <term> | factor
        <factor>    ::= integer | ( <exp> )
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[self.pos]
        self.__logger = logging.getLogger("parserLog")

    def parse(self):
        return self.exp()


    """Grammar mechanics"""
    def next(self):
        self.pos += 1
        self.updateCurrent()
        self.__logger.debug(f"Increased pos to {self.pos}: {str(self.current)}")
    
    def prev(self):
        self.pos -= 1
        self.updateCurrent()
        self.__logger.debug(f"Decreased pos to {self.pos}: {str(self.current)}")

    def updateCurrent(self):
        self.current = self.tokens[self.pos] if len(self.tokens) > self.pos else None

    def rule(f):
        def wrapper(*args):
            self = args[0]

            self.__logger.debug(f"Calling {f.__name__}() at pos {self.pos}/{len(self.tokens) - 1}")
            rv = f(*args)
            self.__logger.debug(f"{f.__name__}() returned {rv}")

            return rv

        return wrapper
    
    def reachedEOF(self):
        self.__logger.debug(f"Reached EOF at pos {self.pos}")
        return self.current is None

    def expect(self, type_, error=False):
        if error:
            if self.current.type != type_:
                raise ParseException(f"Expected token {type_}, got {self.current.type} ({self.current.val})")
        else:
            return self.current.type == type_

    """Grammar"""
    @rule
    def exp(self):
        self.__logger.debug(f"Finding term1")
        term1 = self.term()
        self.__logger.debug(f"Found term1 {term1}")

        self.next()

        while not self.reachedEOF():
            if self.expect("PLUS"):
                self.__logger.debug(f"Current is plus")
                self.next()
                term2 = self.term()

                term1 += term2
            elif self.expect("MINUS"):
                self.__logger.debug(f"Current is minus")
                self.next()
                term2 = self.term()

                term1 -= term2
            else:
                self.prev()
                break
            
            self.next()

        return term1
    
    @rule
    def term(self):
        self.__logger.debug(f"Finding factor")
        factor = self.factor()
        self.__logger.debug(f"Factor is {factor}")

        self.next()

        if not self.reachedEOF():
            if self.expect("MULT"):
                self.__logger.debug(f"Current is mult")
                self.next()
                term = self.term()

                return factor * term
            elif self.expect("DIV"):
                self.__logger.debug(f"Current is div")
                self.next()
                term = self.term()

                return factor / term
            
            self.prev()
        self.__logger.debug(f"Current ({str(self.current)}) is neither * or /")
        return factor
    
    @rule
    def factor(self):
        self.__logger.debug(f"Current: {str(self.current)}")
        if self.expect("NUMBER"):
            self.__logger.debug(f"Current is a number")
            rv = self.current.val
            return rv
        elif self.expect("PARENOPEN"):
            self.__logger.debug(f"Current is (, parsing exp")
            self.next()
            exp = self.exp()
            self.expect("PARENCLOSE", error=True)

            return exp
            
