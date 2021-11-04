import time
import json
from tokenizer import Tokenizer
from cparser import Parser

def parseArgs(args):
    print(f"Args: {args}")

    tokens = Tokenizer(args).tokenize()
    print("tokens:", json.dumps([str(i) for i in tokens], indent=4))

    parsed = Parser(tokens).parse()
    print("parsed:", json.dumps(parsed, indent=4))


testData = [
    "1 + 2 * 3 + 4",
    "3 * 2 / 2",
    "4 + 2 + 1 - 3"
]

expectedOutputs = [eval(i) for i in testData]

for i, arg in enumerate(testData):
    print(f"-- TEST {i + 1} --")
    parseArgs(arg)
    print("\n\n\n")