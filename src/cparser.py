import logging
from exceptions import ParseException
from instructions import instrFor

class Parser:
    def __init__(self):
        self.pos = -1
        self.maxPos = None
        self.tokens = []
        self.__logger = logging.getLogger("parserlog")
    
    def parse(self, tokens):
        self.tokens = tokens
        self.maxPos = len(tokens) - 1

        self.__logger.debug(f"Parsing expression at pos {self.pos + 1} ({str(self.tokens[self.pos])})")

        match = self.match("expr")
        
        self.__logger.debug(f"Matches: {match}")
        return match
    
    """Rules"""
    def ruleExpr(self):
        pos = self.pos + 1

        data = {}

        if self.expect("NUMBER", pos):
            data['val1'] = self.tokens[pos]
            pos += 1
        
        if pos <= self.maxPos:
            if self.expect("PLUS", pos):
                data['operationType'] = "SUM"
            elif self.expect("MINUS", pos):
                data['operationType'] = "SUB"
            else:
                raise ParseException(f"Unknown operator \"{self.tokens[pos]}\"")

            self.pos = pos
            data['val2'] = self.ruleExpr()
            return data

        else:
            data['operationType'] = None
            return data
    
    
    """Rule mechanics"""
    def expect(self, type_, pos):

        if pos > self.maxPos:
            raise ParseException(f"Expected token at pos {pos} but reached EOL (max {self.maxPos})")

        result = self.tokens[pos].type == type_
        self.__logger.debug(f"Expecting {type_} at pos {pos} ({str(self.tokens[self.pos])}): {result}")

        return result

    def match(self, *rules):
        for rule in rules:
            self.__logger.debug(f"Matching rule {rule} at pos {self.pos + 1} ({str(self.tokens[self.pos])})")
            rv = getattr(self, "rule" + rule.capitalize())()
            if rv:
                return rv
        
        raise ParseException(f"No rule matches: {', '.join(rules)}")