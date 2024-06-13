import ply.lex as lex
import sys 

tokens = (
    'INT',      # Declarar inteiro
    'STRING',   # Declarar string
    'PAL',      # Palavra string
    'ARRAY',    # Declarar array
    'VAR',      # Variável que contém o valor
    'NUMINT',   # Número inteiro
    'VIRG',     # ,
    'PCE',      # (
    'PCD',      # )
    'PRE',      # [
    'PRD',      # ]
    'ABRIR_CH', # {
    'FECHAR_CH',# }
    'PV',       # ;            
    'OPAT',     # =
    'OPAD',     # +
    'OPSUB',    # -
    'OPDIV',    # /
    'OPMUL',    # *
    'IGUAL',    # ==
    'DIFF',     # !=
    'LEQ',      # <=
    'LESS',     # <
    'GEQ',      # >=
    'GREATER',  # >
    'FALSE',    # false
    'TRUE',     # true
    'IF',       # if
    'ELSE',     # else
    "AND",      # E lógico
    "OR",       # OU lógico
    'JUMP',     # JUMP
    'BOOL',     # TIPO BOOL
    'NOT',      # NOT lógico
    'MARK',     # MARK
    'PRINT',    # PRINT
    'COMMENT',  # ??...??
    'LER'       # READ do EWVM
)

#OP     = + | - | / | *
#TIPO   = INT|BOOL|ARRAY|STRING
#BOOL   = TRUE | FALSE
#OPLOG  = AND | OR
#OPCOND = '==' | '!=' | '<' | '<=' | '>' | '>='

def t_COMMENT(t):
    r'\?\?(.*)?\?\?|\?\*([\s\S]*?)\*\?'
    pass

t_OPSUB = r"\-"
t_PCE = r"\("
t_PCD = r"\)"
t_ABRIR_CH = r"\{"
t_FECHAR_CH = r"\}"
t_PV = r"\;"
t_IGUAL = r"\=\="
t_OPAT = r"\="
t_OPAD = r"\+"
t_OPDIV = r"\/"
t_OPMUL = r"\*"
t_DIFF = r"\!\="
t_LEQ = r"\<\="
t_LESS = r"\<"
t_GEQ = r"\>\="
t_GREATER = r"\>"
t_PRE = r'\['
t_PRD = r'\]'

def t_LER(t):
    r'LER'
    return t

def t_PRINT(t):
    r"PRINT"
    return t

def t_NOTHING(t):
    r"NOTHING"
    return t

def t_NOT(t):
    r"NOT"
    return t

def t_BOOL(t):
    r"BOOL"
    return t

def t_NUMFLOAT(t):
    r"-?\d+\.\d+"
    t.value = float(t.value)
    return t

def t_NUMINT(t):
    r"-?\d+"
    t.value = int(t.value)
    return t

def t_PAL(t):
    r'"([^"]*)"'
    return t

def t_INT(t):
    r"INT"
    return t

def t_FLOAT(t):
    r"FLOAT"
    return t

def t_STRING(t):
    r"STRING"
    return t

def t_ARRAY(t):
    r"ARRAY"
    return t

def t_VIRG(t):
    r","
    return t

def t_FALSE(t):
    r"FALSE"
    return t

def t_TRUE(t):
    r"TRUE"
    return t

def t_IF(t):
    r"IF"
    return t

def t_ELSE(t):
    r"ELSE"
    return t

def t_RETURN(t):
    r"RETURN"
    return t

def t_AND(t):
    r"AND"
    return t

def t_OR(t):
    r"OR"
    return t

def t_JUMP(t):
    r"JUMP"
    return t

def t_VAR(t):
    r"[a-z][a-zA-Z0-9_]*"
    return t

def t_MARK(t):
    r'MARK'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Carater ilegal '{t.value[0]}' na linha {t.lineno}, posição {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

'''programa = """INT i;
ARRAY ar[4];

MARK IF (i<4) {
    i = i + (1);
} JUMP
ar(0) = i; ??COMENTARIO??
ar(1) = i; ?? OUTRO COMENTARIO ??
ar(2) = i;
ar(3) = i;"""

lexer.input(programa)

while tok := lexer.token():
    print(tok)

print("\nFim da Análise léxica\n")'''