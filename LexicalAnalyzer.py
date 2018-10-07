s_EOI, s_Mul, s_Div, s_Mod, s_Add, s_Sub, s_Negate, s_Not, s_Lss, s_Leq, s_Gtr, s_Geq, s_Eq, s_Neq, s_Assign, \
s_And, s_Or, s_If, s_Else, s_While, s_Print, s_Putc, s_LeftParen, s_RightParen, s_LeftBrace, s_RightBrace, s_Semi, \
s_Comma, s_Ident, s_Integer, s_String = range(31)

all_syms = ["End_of_input", "Op_multiply", "Op_divide", "Op_mod", "Op_add", "Op_subtract",
    "Op_negate", "Op_not", "Op_less", "Op_lessequal", "Op_greater", "Op_greaterequal",
    "Op_equal", "Op_notequal", "Op_assign", "Op_and", "Op_or", "Keyword_if",
    "Keyword_else", "Keyword_while", "Keyword_print", "Keyword_putc", "LeftParen",
    "RightParen", "LeftBrace", "RightBrace", "Semicolon", "Comma", "Identifier",
    "Integer", "String"]

symbols = {'{': s_LeftBrace, '}': s_RightBrace, '(': s_LeftParen, ')': s_RightParen, '+': s_Add, '-': s_Sub, '*': s_Mul, '%': s_Mod, ';': s_Semi, ',': s_Comma}

key_word = {'if': s_If, 'else': s_Else, 'print': s_Print, 'putc': s_Putc, 'while': s_While}

the_ch = " "
the_col = 0
the_line = 1
input_file = None


def follow(expect, ifyes, ifno, err_line, err_col):
    if next_ch() == expect:
        next_ch()
        return ifyes, err_line, err_col
    return ifno, err_line, err_col


def gettok():
    while the_ch.isspace():
        next_ch()

    err_line = the_line
    err_col = the_col

    if len(the_ch) == 0:
        return s_EOI, err_line, err_col
    elif the_ch == '/':
        return divOrComment(err_line, err_col)
    elif the_ch == '\'':
        return char_lit(err_line, err_col)
    elif the_ch == '<':
        return follow('=', s_Leq, s_Lss, err_line, err_col)
    elif the_ch == '>':
        return follow('=', s_Geq, s_Gtr, err_line, err_col)
    elif the_ch == '=':
        return follow('=', s_Eq, s_Assign, err_line, err_col)
    elif the_ch == '!':
        return follow('=', s_Neq, s_Not, err_line, err_col)
    elif the_ch == '&':
        return follow('&', s_And, s_EOI, err_line, err_col)
    elif the_ch == '|':
        return follow('|', s_Or, s_EOI, err_line, err_col)
    elif the_ch == '"':
        return string_lit(the_ch, err_line, err_col)
    elif the_ch in symbols:
        sym = symbols[the_ch]
        next_ch()
        return sym, err_line, err_col
    else:
        return ident_or_int(err_line, err_col)


def next_ch():
    global the_ch, the_col, the_line

    the_ch = input_file.read(1)
    the_col += 1
    if the_ch == '\n':
        the_line += 1
        the_col = 0
    return the_ch

def char_lit(err_line, err_col):
    n = ord(next_ch())
    if the_ch == '\\':
        next_ch()
        if the_ch == 'n':
            n = 10
        elif the_ch == '\\':
            n = ord('\\')
    next_ch()
    return s_Integer, err_line, err_col, n

def divOrComment(err_line, err_col):
    if next_ch() != '*':
        return s_Div, err_line, err_col
    next_ch()
    while True:
        if the_ch == '*':
            if next_ch() == '/':
                next_ch()
                return gettok()
        else:
            next_ch()

# string
def string_lit(start, err_line, err_col):
    text = ""

    while next_ch() != start:
        text += the_ch
    next_ch()
    return s_String, err_line, err_col, text

# identifiers and integers
def ident_or_int(err_line, err_col):
    is_number = True
    text = ""

    while the_ch.isalnum() or the_ch == '_':
        text += the_ch
        if not the_ch.isdigit():
            is_number = False
        next_ch()

    if text[0].isdigit():
        n = int(text)
        return s_Integer, err_line, err_col, n

    if text in key_word:
        return key_word[text], err_line, err_col

    return s_Ident, err_line, err_col, text


while True:
    t = gettok()
    tok = t[0]
    line = t[1]
    col = t[2]

    print("%5d  %5d   %-14s" % (line, col, all_syms[tok]))

    if tok == s_Integer:
        print("   %5d" % (t[3]))
    elif tok == s_Ident:
        print("  %s" % (t[3]))
    elif tok == s_String:
        print('  "%s"' % (t[3]))
    else:
        print("")

    if tok == s_EOI:
        break




