import sys
import os

sys.path.append(os.path.abspath('src'))

"""Start test"""
from tokenizer import Tokenizer


def tokenize(expr):
    tokenizer = Tokenizer(expr)
    return tokenizer.tokenize()


def main():
    expressions = [
        "1 + 2",
        "3 - 4 + 2",
        "3+4 - 5",
        "2 - -3",
        "10 + 203   - 5",
    ]

    for expr in expressions:
        print(f"EXPRESSION: {expr}")
        tokens = tokenize(expr)
        for token in tokens:
            print("{0:<8}{1:>15}".format(token.type, "-" if token.val is None else token.val))
        
        print("\n" * 2)


if __name__ == "__main__":
    main()