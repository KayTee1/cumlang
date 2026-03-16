from dataclasses import dataclass
from keywords import KEYWORDS


@dataclass
class Token:
    type: str
    value: str
    position: int


MULTI_CHAR_TOKENS = {
    "==": "EQEQ",
    "!=": "NOTEQ",
    "<=": "LTE",
    ">=": "GTE",
    "+=": "PLUSEQ",
    "-=": "MINUSEQ",
    "++": "PLUSPLUS",
    "--": "MINUSMINUS",
}

SINGLE_CHAR_TOKENS = {
    "(": "LPAREN",
    ")": "RPAREN",
    "{": "LBRACE",
    "}": "RBRACE",
    ";": "SEMICOLON",
    ",": "COMMA",
    "=": "EQUALS",
    "<": "LT",
    ">": "GT",
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
}


def lex(source: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0

    while i < len(source):
        char = source[i]

        if char.isspace():
            i += 1
            continue

        if i + 1 < len(source):
            two_char = source[i:i + 2]
            if two_char in MULTI_CHAR_TOKENS:
                tokens.append(Token(MULTI_CHAR_TOKENS[two_char], two_char, i))
                i += 2
                continue

        if char in SINGLE_CHAR_TOKENS:
            tokens.append(Token(SINGLE_CHAR_TOKENS[char], char, i))
            i += 1
            continue

        if char.isalpha() or char == "_":
            start = i
            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1

            value = source[start:i]
            token_type = KEYWORDS.get(value, "IDENTIFIER")
            tokens.append(Token(token_type, value, start))
            continue

        if char.isdigit():
            start = i
            has_dot = False

            while i < len(source) and (source[i].isdigit() or source[i] == "."):
                if source[i] == ".":
                    if has_dot:
                        raise ValueError(f"Invalid number at position {i}")
                    has_dot = True
                i += 1

            value = source[start:i]
            tokens.append(Token("NUMBER", value, start))
            continue

        if char == '"':
            start = i
            i += 1

            while i < len(source) and source[i] != '"':
                if source[i] == "\\" and i + 1 < len(source):
                    i += 2
                else:
                    i += 1

            if i >= len(source):
                raise ValueError(f"Unterminated string starting at position {start}")

            i += 1
            value = source[start:i]
            tokens.append(Token("STRING", value, start))
            continue

        raise ValueError(f"Unexpected character '{char}' at position {i}")

    tokens.append(Token("EOF", "", len(source)))
    return tokens
