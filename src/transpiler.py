from lexer import Token

TOKEN_TO_C = {
    "SHAFT": "int",
    "BALLS": "double",
    "EDGE": "void",
    "NUT": "return",
    "SPIT": "printf",
    "KEEP_PUMPING": "while",
    "STROKE": "for",
    "HORNY": "if",
    "LIMP": "else",
}

def transpile(tokens: list[Token]) -> str:
    parts = ['#include <stdio.h>', '']

    for token in tokens:
        if token.type == "EOF":
            continue

        value = TOKEN_TO_C.get(token.type, token.value)
        parts.append(value)

    return " ".join(parts)
