#!/usr/bin/env python3
"""
EXAMPLE - https://github.com/azmikamis/pipbook/blob/master/any/genome1.py
"""
from collections import namedtuple

TRANSFORM, SUMMARIZE = ("TRANSFORM", "SUMMARIZE")

Code = namedtuple("Code", "name code kind")

CODE = (
    Code(
        "Count",
"""
import re
matches = re.findall(target, genome)
if matches:
    result = len(matches)
else:
    error = "'{}' not found".format(target)
""",
        SUMMARIZE
    ),
    Code(
        "Replace",
"""
import re
result, count = re.subn(target, replace, genome)
if not count:
    error = "no '{}' replacements made".format(target)
""",
        TRANSFORM
    ),
    Code(
        "Exception Test",
"""
result = 0
for i in range(len(genome)):
    if genome[i] = "A":
        result += 1
""",
        SUMMARIZE
    ),
    Code(
        "Error Test",
"""
import re
matches = re.findall(target * 5, genome)
if matches:
    result = len(matches)
else:
    error = "'{}' not found".format(target)
""",
        TRANSFORM
    ),
    Code(
        "No Result Test",
"""
# No result
""",
        TRANSFORM
    ),
    Code(
        "Wrong Kind Test",
"""
result = len(genome)
""",
        TRANSFORM
    ),
    Code(
        "Termination Test",
"""
import sys
result = "terminating"
sys.exit()
""",
        SUMMARIZE
    ),
    Code(
        "Length",
"""
result = len(genome)
""",
        SUMMARIZE
    )
)

GENOME = """TGTTAGTCGCTCCTCGGTCTAAGACATCAAAGTCGGTCTGCGCGGCTGCTCCCTTAGCGCTG
CATAAGAGCGGGGCAGAGAGAGATAGGCGTTTTGACCGTGGCGAGCAAGGCGCGTCATAGTGTCGCCGTGACTG
ATCCTACTGGGTTCTTGCTACTGCCCGGGTCGCAATCCAAAATCTCCACGCGCTGCCACCCCGAAGAAGATATA
TGTCACTGAATTGTATTGGTAACATAGTCGAATTGGGTTCAGGTAAGTTAGTCGTTTAGCCGCTGCGACAGTGG
TGGAAGGGCGAATAGTGTAAAATTTCGCCTGTTAGTGAACATTATCAGGCTGCCATCGTTGATCGCCCCTCTTA
AACTCAGTCTTAAATGAGTTCCCGCCTAAGGTCATTCGTGCCTTGATGATTGATAGCTCGATTGGTCCCTTATG
AAACCGGACCAGAAATGTACCCGCTGAACCGGTGTCATAAGTGTCGCCGTCCCTACGATCGACACTTCCTGAGC
ACGAACGATTTGCGACGCTGTAATGCCACGAGGACTGCATTGAAGATTTTTTGTCCTAGGTGTATGTGCTTCTC
AGGAAGATGCACTACGCACTCCCCTTATCACGGGTGTGACCATCAGGTAGCGTAGGAAGATTAAGACCGCGTAA
CTATCCCTTTCCGTCGCACTCCGACGTCTCAGCACATGTGCGGGGGCCCCTAATTGAGAAACAGTCCATGGTTG
TCCGTAAGTTTCGGAAATCAACTTCACTGCTAGATGGTTGGACGCCAAGGCTCAATAGGTTGGACTCTAAGAAG
""".replace("\n", "")


def execute(code, context):
    try:
        exec(code.code, globals(), context)
        result = context.get("result")
        error = context.get("error")
        handle_result(code, result, error)
    except Exception as err:
        print(f"'{code.name}' raised an exception: {err}\n")


def handle_result(code, result, error):
    if error is not None:
        print(f"'{code.name}' error: {error}")
    elif result is None:
        print(f"'{code.name}' produced no result")
    elif code.kind == TRANSFORM:
        genome = result
        try:
            print(f"'{code.name}' produced a genome of length {len(genome)}")
        except TypeError as err:
            print(f"'{code.name}' error: expected a sequence result: {err}")
    elif code.kind == SUMMARIZE:
        print(f"'{code.name}' produced a result of {result}")
    print()


def main():
    genome = 3 * GENOME
    for code in CODE:
        context = dict(genome=genome, target="G[AC]{2}TT", replace="TCGA")
        execute(code, context)


if __name__ == "__main__":
    main()
