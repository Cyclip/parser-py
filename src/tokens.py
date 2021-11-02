"""Token classes"""
class Token:
    def __init__(self, _type, val=None):
        self.type = _type
        self.val = val
    
    def __str__(self):
        return f"Token({self.type}, {self.val})"
    
    def __repr__(self):
        return self.__str__()
