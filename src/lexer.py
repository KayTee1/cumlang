from dataclasses import dataclass
from keywords import KEYWORDS


@dataclass
class Token:
    type: str
    value: str
    line: int
    column: int


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
    line = 1
    column = 1

    while i < len(source):
        char = source[i]

        if char == "\n":
            i += 1
            line += 1
            column = 1
            continue

        if char.isspace():
            i += 1
            column += 1
            continue

        start_line = line
        start_column = column

        if i + 1 < len(source):
            two_char = source[i:i + 2]
            if two_char in MULTI_CHAR_TOKENS:
                tokens.append(Token(MULTI_CHAR_TOKENS[two_char], two_char, start_line, start_column))
                i += 2
                column += 2
                continue

        if char in SINGLE_CHAR_TOKENS:
            tokens.append(Token(SINGLE_CHAR_TOKENS[char], char, start_line, start_column))
            i += 1
            column += 1
            continue

        if char.isalpha() or char == "_":
            start = i

            while i < len(source) and (source[i].isalnum() or source[i] == "_"):
                i += 1
                column += 1

            value = source[start:i]
            token_type = KEYWORDS.get(value, "IDENTIFIER")
            tokens.append(Token(token_type, value, start_line, start_column))
            continue

        if char.isdigit():
            start = i
            has_dot = False

            while i < len(source) and (source[i].isdigit() or source[i] == "."):
                if source[i] == ".":
                    if has_dot:
                        raise ValueError(
                            f"Invalid number at line {line}, column {column}"
                        )
                    has_dot = True
                i += 1
                column += 1

            value = source[start:i]
            tokens.append(Token("NUMBER", value, start_line, start_column))
            continue

        if char == '"':
            start = i
            i += 1
            column += 1

            while i < len(source) and source[i] != '"':
                if source[i] == "\n":
                    raise ValueError(
                        f"Unterminated string at line {start_line}, column {start_column}"
                    )

                if source[i] == "\\" and i + 1 < len(source):
                    i += 2
                    column += 2
                else:
                    i += 1
                    column += 1

            if i >= len(source):
                raise ValueError(
                    f"Unterminated string at line {start_line}, column {start_column}"
                )

            i += 1
            column += 1

            value = source[start:i]
            tokens.append(Token("STRING", value, start_line, start_column))
            continue

        raise ValueError(
            f"Unexpected character '{char}' at line {line}, column {column}"
        )

    tokens.append(Token("EOF", "", line, column))
    return tokens
