import time
import json
import logging
from tokenizer import Tokenizer
from cparser import Parser

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s at %(funcName)s():%(lineno)s  =>  %(message)s",
)

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

print(f"Args: {testData[0]}")
parseArgs(testData[0])

"""for i, arg in enumerate(testData):
    print(f"-- TEST {i + 1} --")
    parseArgs(arg)
    print("\n\n\n")
    break"""