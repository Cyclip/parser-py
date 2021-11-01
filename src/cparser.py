import logging
from exceptions import ParseException

class Parser:
    def __init__(self):
        self.pos = -1
        self.__logger = logging.getLogger("parserlog")
    
    def parse(self, tokens):
        self.__logger.debug(f"Parsing {len(tokens)} tokens")
        self.tokens = tokens
        return self.parseExpression()
    
    def parseExpression(self):
        self.__logger.debug(f"Parsing expression at pos {self.pos} ({str(self.tokens[self.pos])})")
        match = self.match("sum")
        self.__logger.debug(f"Matches: {match}")


    def match(self, *rules):
        for rule in rules:
            self.__logger.debug(f"Matching rule {rule} at pos {self.pos} ({str(self.tokens[self.pos])})")
            rv = getattr(self, "rule" + rule.capitalize())()
            if rv:
                return rv
        
        raise ParseException(f"No rule matches: {', '.join(rules)}")
    
    """Rules"""
    def ruleSum(self):
        pos = self.pos + 1

        if self.expect("NUMBER", pos):
            num1 = self.tokens[pos]
            pos += 1

            if self.expect("PLUS", pos):
                pos += 1

                if self.expect("NUMBER", pos):
                    num2 = self.tokens[pos]

                    return ("SUM", num1, num2)
            
    
    """Rule mechanics"""
    def expect(self, type_, pos):
        self.__logger.debug(f"Expecting {type_} at pos {pos} ({str(self.tokens[self.pos])})")
        result = self.tokens[pos].type == type_
        self.__logger.debug(result)

        return result