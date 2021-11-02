INSTRUCTIONS = {
    "SUM":  0b00001,
    "SUB":  0b00010,
    "MULT": 0b00011,
    "DIV":  0b00101,
}

def instrFor(instr):
    return INSTRUCTIONS[instr]