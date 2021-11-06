import time
import json
import logging
from tokenizer import Tokenizer
from cparser import Parser


def parseArgs(args):
    print(f"Args: {args}")

    tokens = Tokenizer(args).tokenize()
    print("tokens:", json.dumps([str(i) for i in tokens], indent=4))

    parsed = Parser(tokens).parse()
    print("parsed:", json.dumps(parsed, indent=4))
    return parsed


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] (%(levelname)s) %(funcName)s  =>  %(message)s",
)

testData = [
    "5 + 3",
    "3 * 2 / 2",
    "4 + 2 + 1 - 3",
    "1 + 2 * 3 + 4",
    "1 + 2 * 3 * 4 + 5",
    "1 + 5(3 - 2)",
]

expectedOutputs = [8, 3.0, 4, 11, 30, 6,]

argsI = -1
args = testData[argsI]
print(f"Args: {args}")
parseArgs(args)
print(f"Expected output: {expectedOutputs[argsI]}")