import sys
import os

sys.path.append(os.path.abspath('src'))

"""Start test"""
from tokenizer import Tokenizer
from cparser import Parser

testData = [
    "5 + 3",
    "3 * 2 / 2",
    "4 + 2 + 1 - 3",
    "1 + 2 * 3 + 4",
    "1 + 2 * 3 * 4 + 5",
    "1 + 5(3 - 2)",
]

expectedOutputs = [8, 3.0, 4, 11, 30, 6,]


def parse(args):
    tokens = Tokenizer(args).tokenize()
    parsed = Parser(tokens).parse()
    return parsed


def main():
    for i, arg in enumerate(testData):
        parsed = parse(arg)
        expected = expectedOutputs[i]
        print(f"Argument {arg}: Returned {parsed} (expected {expected})")


if __name__ == "__main__":
    main()