import ply.yacc as yacc
import sys
import re
from PLC_TP2_Lexico import tokens

def notInConjunto(p):
    res = True
    if (p in parser.inteiros): res = False
    elif(p in parser.strings): res = False
    elif(p in parser.bools): res = False
    elif(p in parser.arrays): res = False
    elif(p in parser.matrizes): res = False
    return res

def elementosLista(p): #Dividir elementos de p[2]
    s = []
    for elemento in p:
        if isinstance(elemento, list):
            s.extend(elementosLista(elemento)) # Chama recursivamente a funcao para listas aninhadas
        else:
            s.append(elemento) 
    return s
#Axioma
def p_axioma(p):
    'axioma : programa'
    p[0] = p[1]
    for x in p[0]:
        if (x != None and x !=''): 
            print(x,end="")
    if(parser.nPops > 0): 
        print(f"POP{parser.nPops}")
        parser.nPops = 0

def p_programa(p):
    'programa : declaracoes corpo'
    p[0] = elementosLista([p[1]]) + elementosLista([p[2]])

#--------------declaracoes----------------------#

def p_declaracoes_declaracoesDeclaracao(p):
    'declaracoes : declaracoes declaracao'
    p[0] = [p[1]] + [p[2]]
    p[0] = elementosLista(p[0])

def p_declaracoes_empty(p):
    'declaracoes : '

#--------------declaracao----------------------------#

def p_declaracao_seqDecl(p):
    'declaracao : tipo seqDecl PV'
    parser.tipos = str(p[1])
    p[0] = str(p[2])

#--------------SEQDECL-------------------------------#

def p_seqDecl_atrVIRGseqDecl(p):
    'seqDecl : atr VIRG seqDecl'
    p[0] = p[1] + str(p[3]) 
    parser.tipos = ""

def p_seqDecl_atr(p):
    'seqDecl : atr'
    p[0] = p[1]


#--------------atr------------------------------#

def p_atr_VAR(p):
    'atr : VAR'
    if (notInConjunto(p[1])):
        match parser.tipos:
            case "INT":
                parser.inteiros[p[1]] = parser.posicao
                p[0] = f"PUSHI0\n"
                parser.posicao += 1
                parser.nPops += 1
            case "STRING":
                parser.strings[p[1]] = parser.posicao
                p[0] = f"PUSHS \"\"\n"
                parser.posicao += 1
                parser.nPops += 1
            case "BOOL":#default TRUE
                parser.bools[p[1]] = parser.posicao
                p[0] = f"PUSHI1\n" 
                parser.posicao += 1
                parser.nPops += 1
            case "" :
                print("ERRO: Nao atribuido o tipo")
    else:
        print(f"ERRO: A variavel {p[1]} ja foi declarada")
        exit()

def p_atr_VAROPAToperacao(p):
    'atr : VAR OPAT operacao'
    if(not notInConjunto(p[1])):
        print(f"ERRO: A variavel {p[1]} ja foi declarada!")
        exit()
    if(parser.tipos != "STRING" and parser.tipos != "BOOL" and parser.tipos != "INT"): 
        print("ERRO: Esse tipo de dados nao existe.")
        exit()
    if (parser.tipos == "INT" and notInConjunto(p[1])):
        parser.inteiros[p[1]] = parser.posicao #Associa o numero a variavel no dicionario
    if (parser.tipos == "STRING" and notInConjunto(p[1])):
        parser.strings[p[1]] = parser.posicao
        p[0] = p[3]
    if (parser.tipos == "BOOL" and notInConjunto(p[1])):
        parser.bools[p[1]] = parser.posicao
        p[0] = p[3]
    p[0] = f"{p[3]}"
    parser.posicao += 1
    parser.nPops +=1

def p_atr_VARARRAY(p):
    'atr : VAR PRE NUMINT PRD'
    if (parser.tipos == 'ARRAY' and notInConjunto(p[1])):
        tamanho = int(p[3])
        parser.arrays[p[1]] = (parser.posicao,tamanho)
        p[0] = 'PUSHN'+str(tamanho) +'\n'
        parser.posicao += tamanho
        parser.nPops += tamanho
    elif (parser.tipos [0] != 'ARRAY'):
        print(f"ERRO: A variavel {p[1]} nao e do tipo ARRAY.")
        exit()
    elif(not notInConjunto(p[1])):
        print(f"ERRO: Variavel {p[1]} ja declarada anteriormente")
        exit()

def p_atr_VARARRAYcomConteudo(p):
    'atr : VAR PRE NUMINT PRD OPAT ABRIR_CH seqNumInt FECHAR_CH'
    if(not notInConjunto(p[1])):
        print(f"ERRO: Variavel {p[1]} ja foi declarada anteriormente")
        exit()
    if(parser.nArray == int(p[3])): #Conteudo com numero certo de elementos
        if (parser.tipos == 'ARRAY' and notInConjunto(p[1])):
            tamanho = int(p[3])
            parser.arrays[p[1]] = (parser.posicao,tamanho)
            p[0] = p[7]
            parser.posicao += tamanho
            parser.nPops += tamanho
    else:
        print(f"ERRO: A variavel {p[1]} tem limite {int(p[3])} e foram colocados {parser.nArray} elementos!")
        exit()

def p_atr_matrizDefault(p):
    'atr : VAR PRE NUMINT PRD PRE NUMINT PRD'
    if (parser.tipos == 'ARRAY' and notInConjunto(p[1])):
        tamanho = int(p[3]) * int(p[6])
        #Guarda a posicao de onde comeca na stack e os parametros de tamanho
        parser.matrizes[p[1]] = (parser.posicao,int(p[3]),int(p[6]))
        p[0] = f"PUSHN{tamanho}\n"
        parser.posicao += tamanho
        parser.nPops += tamanho
    elif (parser.tipos [0] != 'ARRAY'):
        print(f"ERRO: A variavel {p[1]} nao e do tipo ARRAY.")
        exit()
    elif(not notInConjunto(p[1])):
        print(f"ERRO: Variavel {p[1]} ja foi declarada anteriormente")
        exit()

def p_atr_matrizComConteudo(p):
    'atr : VAR PRE NUMINT PRD PRE NUMINT PRD OPAT ABRIR_CH seqNumInt FECHAR_CH'
    if(not notInConjunto(p[1])):
        print(f"ERRO: Variavel {p[1]} ja foi declarada anteriormente")
        exit()
    if(parser.nArray == int(p[3])): #Conteudo com número certo de elementos
        if (parser.tipos == 'ARRAY' and notInConjunto(p[1])):
            tamanho = int(p[3]) * int(p[6])
            parser.matrizes[p[1]] = (parser.posicao,int(p[3]),int(p[6]))
            p[0] = p[10]
            parser.posicao += tamanho
            parser.nPops += tamanho
    else:
        print(f"ERRO: A variavel {p[1]} tem limite {int(p[3])} e foram colocados {parser.nArray} elementos!")
        exit()


#--------------seqNumInt--------------------------#

def p_seqNumInt_NUMINT(p):
    'seqNumInt : NUMINT'
    parser.nArray += 1
    p[0] = f"PUSHI{p[1]}\n"
    
def p_seqNumInt_NumMaisNum(p):
    'seqNumInt : NUMINT VIRG seqNumInt'
    parser.nArray += 1
    p[0] = f"PUSHI{p[1]}\n" + p[3]

#--------------corpo----------------------------#

def p_corpo_instrucao(p):
    'corpo : corpo instrucao'
    parser.tipos = "DECLDONE"
    p[0] = [p[1]] + [p[2]]
    p[0] = elementosLista(p[0])
    s = ""
    for elemento in p[0]:
        if elemento != None:
            s+=elemento
    p[0] = s
    
def p_corpo_VAZIO(p):
    'corpo : '
    parser.tipos = "DECLDONE"
    p[0] = ""

#--------------instrucao----------------------------#

def p_instrucao_ifelsestatement(p):
    'instrucao : ifelsestatement'
    p[0] =  p[1] 

def p_instrucao_print(p):
    'instrucao : print PV'
    p[0] = p[1]

def p_instrucao_VARopatOPERACAO(p):
    'instrucao : VAR OPAT operacao PV'
    if(not notInConjunto(p[1])):
        if(p[1] in parser.inteiros): #Variavel declarada mas nao inteira
            padrao_string = r'\sPUSH[SG].*'
            if (re.match(r'PUSHI.*',p[3])):
                p[0] = p[3] + f"STOREG{parser.inteiros[p[1]]}\n"
            else: 
                print("ERRO: A Varivel nao e do tipo INT.")
                exit()
            p[0] = p[3] + f"STOREG{parser.inteiros[p[1]]}\n"
        elif(p[1] in parser.bools):
            padrao_bool = r'\s\sPUSH[IG].*'
            if (re.match(padrao_bool,p[3])):
                p[0] = p[3] + f"STOREG{parser.bools[p[1]]}\n"
            else: 
                print("ERRO: A Varivel nao e do tipo BOOL.")
                exit()
        elif(p[1] in parser.strings):
            padrao_string = r'\sPUSH[SG].*'
            if (re.match(padrao_string,p[3])):
                p[0] = p[3] + f"STOREG{parser.strings[p[1]]}\n"
            else: 
                print("ERRO: A Varivel nao e do tipo STRING.")
                exit()
    elif (notInConjunto(p[1])):
        print("ERRO: Varivel nao declarada corretamente.")
        exit()

def p_instrucao_mudarindexarray(p):
    'instrucao : VAR PCE NUMINT PCD OPAT operacao PV'
    if(not notInConjunto(p[1])):
        if(p[1] not in parser.arrays): #Variavel declarada mas nao do tipo ARRAY
            print(f"ERRO: A variavel {p[1]} nao e do tipo ARRAY")
            exit()
        else:#Se for variavel declarada do tipo certo
            p[0] = p[6] + f"STOREG{parser.arrays[p[1]][0]+p[3]}\n"
    else:
        print(f"ERRO: A variavel {p[1]} nao foi declarada")

def p_instrucao_mudarindexMatriz(p):
    'instrucao : VAR PCE NUMINT PCD PCE NUMINT PCD OPAT operacao PV '
    if(not notInConjunto(p[1])):
        if(p[1] not in parser.matrizes): #Variavel declarada mas nao do tipo ARRAY
            print(f"ERRO: A variavel {p[1]} nao e do tipo ARRAY")
            exit()
        else:#Se for variavel declarada do tipo certo
            #Se quiser mudar o valores de x[z1][z2]  da matriz x[y1][y2] y1 linhas e y2 colunas
            # tenho que aceder na stack a posicao:
            # posicao da matriz na stack + (y2 * z1) + z2
            pm = parser.matrizes[p[1]][0] + (parser.matrizes[p[1]][2] * p[3]) + p[6]
            p[0] = p[9] + f"STOREG{pm}\n"
    else:
        print(f"ERRO: A variavel {p[1]} nao foi declarada")

def p_instrucao_tojumpPV(p):
    'instrucao : tojump PV'
    p[0] = p[1]

def p_instrucao_jumptoPV(p):
    'instrucao : jumpto PV'
    p[0] = p[1]
 

#--------------operacao-----------------------#

def p_operacao_termo(p):
    'operacao : termo'
    p[0] = p[1]

def p_operacao_adicao(p):
    'operacao : operacao OPAD termo'
    p[0] = p[3] + p[1] + "ADD\n"

def p_operacao_subtracao(p):
    'operacao : operacao OPSUB termo'
    p[0] = p[3] + p[1] + "SUB\n"


#--------------TERMO-----------------------------#

def p_termo_fator(p):
    'termo : fator'
    p[0] = p[1]

def p_termo_mult(p):
    'termo : termo OPMUL fator'
    p[0] = p[1] + p[3] + 'MUL\n'

def p_termo_DIV(p):
    'termo : termo OPDIV fator'
    p[0] = p[1] + p[3] + 'DIV\n'


#--------------FATOR-----------------------------#
    
def p_fator_NUMINT(p):
    'fator : NUMINT'
    p[0] = f"PUSHI{p[1]}\n"

def p_fator_VAR(p):
    'fator : VAR'
    if (p[1] in parser.inteiros):
        p[0]= f"PUSHG {parser.inteiros[p[1]]}\n"
    elif (p[1] in parser.bools):
        p[0]= f"PUSHG {parser.bools[p[1]]}\n"
    elif (p[1] in parser.strings):
        p[0]= f" PUSHG {parser.strings[p[1]]}\n"
    elif (p[1] in parser.arrays): #GUARDAR A QUANTIDADE DE WRITES A FAZER NO PRINT
        i = 0
        a = parser.arrays[p[1]][i]
        s = ""
        while(i<parser.arrays[p[1]][1]):
            s += f"PUSHG {a}\n"
            i+=1
            a+=1
        p[0] = s
    elif(p[1] in parser.matrizes):#GUARDAR A QUANTIDADE DE WRITES A FAZER NO PRINT
        i1 = 0
        i2 = 1
        #O tamanho e dado pelo nmr_linhas * nmr_colunas
        tamanho = parser.matrizes[p[1]][1] * parser.matrizes[p[1]][2]
        # a = posicao do array na stack
        a = parser.matrizes[p[1]][0]
        s = ""
        while(i1<tamanho):
            s += f"PUSHG {a}\n"
            a += 1
            i1 += 1
            i2 += 1
        p[0] = s

def p_fator_VARARRAY(p):
    'fator : VAR PCE NUMINT PCD'
    if (parser.tipos == "ARRAY" or parser.tipos == "DECLDONE"):
        p[0] = f"PUSHG{parser.arrays[p[1]][0]+p[3]}\n"
    else:
        print("ERRO: A varivel nao e do tipo ARRAY.")
        exit()

def p_fator_VARMATRIZ(p):
    'fator : VAR PCE NUMINT PCD PCE NUMINT PCD'
    if (parser.tipos == "ARRAY" or parser.tipos == "DECLDONE"):
        pm = parser.matrizes[p[1]][0] + (parser.matrizes[p[1]][2] * p[3]) + p[6]
        p[0] = f"PUSHG{pm}\n"
    else:
        print("ERRO: A varivel nao e do tipo ARRAY.")
        exit()

def p_fator_bool(p):
    'fator : bool'
    if (parser.tipos == "BOOL" or parser.tipos == "DECLDONE"):
        p[0] = p[1]
    else:
        print("ERRO: A varivel nao e do tipo BOOL.")
        exit()

def p_fator_PAL(p):
    'fator : PAL'
    if (parser.tipos == "STRING" or parser.tipos == "DECLDONE"):
        p[0] = f" PUSHS {p[1]}\n"
    else:
        print("ERRO: A varivel nao e do tipo STRING.")
        exit()

def p_fator_NOTcondicao(p):
    'fator : NOT PCE condicao PCD'
    p[0] = p[3] + "NOT\n"

def p_fator_lerInput(p):
    'fator : LER PCE PCD'
    p[0] = "READ\nATOI\n"


#--------------IFELSESTATEMENT-------------------#

def p_ifselsetatement(p):
    'ifelsestatement : IF PCE condicao PCD ABRIR_CH corpo FECHAR_CH ELSE ABRIR_CH corpo FECHAR_CH'
    if_ = parser.posicaoIf
    p[0] = f"{p[3]}\nJZ elselabel{if_}\n{p[6]}JUMP iflabel{if_}\nelselabel{if_}:\n{p[10]}iflabel{if_}:\n"
    parser.posicaoIf += 1
        

#--------------condicao--------------------------#
def p_condicao_operacao(p):
    'condicao : operacao'
    p[0] = p[1]

def p_condicao_igualigual(p):
    'condicao : operacao IGUAL operacao'
    p[0] = p[1] + p[3] + "EQUAL\n"

def p_condicao_DIFF(p):
    'condicao : operacao DIFF operacao'
    p[0] = p[1] + p[3] + "EQUAL\n" + "NOT\n"

def p_condicao_MENOR(p):
    'condicao : operacao LESS operacao'
    p[0] = p[1] + p[3] + "INF\n"

def p_condicao_MAIOR(p):
    'condicao : operacao GREATER operacao'
    p[0] = p[1] + p[3] + "SUP\n"

def p_condicao_MENORouIGUAL(p):
    'condicao : operacao LEQ operacao'
    p[0] = p[1] + p[3] + "INFEQ\n"

def p_condicao_MAIORouIGUAL(p):
    'condicao : operacao GEQ operacao'
    p[0] = p[1] + p[3] + "SUPEQ\n"

def p_condicao_OU(p):
    'condicao : PCE condicao PCD OR PCE condicao PCD'
    p[0] = p[2] + p[6] + "OR\n"

def p_condicao_AND(p):
    'condicao : PCE condicao PCD AND PCE condicao PCD'
    p[0] = p[2] + p[6] + "AND\n"


#--------------tojump----------------------------#
    
#dowhile
def p_tojump_MARKABRIRCHcorpoFECHARCHif(p):    
    'tojump : MARK ABRIR_CH corpo FECHAR_CH IF PCE condicao PCD JUMP'
    cic = parser.posicaoCiclo
    p[0] = p[3]+f"labelwhile{cic}:\n"+p[7]+f"JZ endwhile{cic}\n"+p[3]+f"JUMP labelwhile{cic}\n"+f"endwhile{cic}:\n"
    parser.posicaoCiclo += 1


#--------------jumpto----------------------------#
    
#whiledo
def p_jumpto_MARKifCondcorpoJump(p):
    'jumpto : MARK IF PCE condicao PCD ABRIR_CH corpo FECHAR_CH JUMP'
    cic = parser.posicaoCiclo
    p[0] = f"labelwhile{cic}:\n"+p[4]+f"JZ endwhile{cic}\n"+p[7]+f"JUMP labelwhile{cic}\n"+f"endwhile{cic}:\n"
    parser.posicaoCiclo += 1


#--------------PRINT------------------------------#
def p_print(p):
    'print : PRINT PCE condicao PCD'
    padrao_string = r'\sPUSH[SG].*'
    if (re.match(padrao_string,p[3])):
        p[0] = f"{p[3]}WRITES\n"
    else:
        p[0] = f"{p[3]}WRITEI\n"

#--------------bool------------------------------#

def p_bool_TRUE(p):
    'bool : TRUE'
    p[0] = "  PUSHI1\n"

def p_bool_FALSE(p):
    'bool : FALSE'
    p[0] = "  PUSHI0\n"


#--------------------tipo------------------------#

def p_tipo_INT(p):
    'tipo : INT'
    parser.tipos = 'INT'
    p[0] = ""

def p_tipo_STRING(p):
    'tipo : STRING'
    parser.tipos = 'STRING'
    p[0] = ""

def p_tipo_BOOL(p):
    'tipo : BOOL'
    parser.tipos = 'BOOL'
    p[0] = ""

def p_tipo_ARRAY(p):
    'tipo : ARRAY'
    parser.tipos = 'ARRAY'
    p[0] = "" #N inteiros

#----------------------main----------------------#
def p_error(p):
    parser.success = False
    print('Syntax error!',p)

#inicio do parsing
parser = yacc.yacc() #Transforma automato num parser
parser.success = True
    
parser.nPops = 0            #Para limpar a stack
parser.posicaoIf = 0        #Guarda contagem de labels
parser.posicaoCiclo = 0     #Guarda contagem de labels
parser.posicao = 0      #Guardar posicoes na stack para declaracoes
parser.nArray = 0       #Saber o tamanho do array ao declarar
parser.tipos    = ""    #Para saber se o tipo e o declarado
parser.inteiros = {}    #Guardar posicoes das variaveis declaradas INT
parser.strings  = {}    #Guardar posicoes das variaveis declaradas STRING
parser.bools    = {}    #Guardar posicoes das variaveis declaradas BOOL
parser.arrays   = {}    #Guardar posicoes das variaveis declaradas ARRAY
parser.matrizes = {}    #Guardar posicoes das variaveis declaradas ARRAY (matriz)
parser.nWrites = 0
#Exemplo swap
#file = open("exemploswap.txt",'r')
#Exemplo IfElse
#file = open("exemploIfElse.txt",'r')
#Exemplo Declaracao de um array multi-dimensional
#file = open("exemploarrayMultiDim.txt",'r')
#Exemplo Declaracao de um array e um while
file = open("exemploarrayWhile.txt",'r')
#Exemplo Utilizacao de variaveis STRING e varias condicoes interligadas
#file = open("exemploVarStringCond.txt",'r')
#Exemplo Aninhamento de IfElse e leitura de Input
#file = open("exemploIfElseInput.txt",'r')
#Exemplo Erro de declaraço de variveis j declaradas
#file = open("exemploErroDeclaracao.txt",'r')
#Exemplo Erro de tipo no correspondente declaracao
#file = open("exemploErroNaoCorrespondenciaDecl.txt",'r')
#Exemplo Erro de tipo no correspondente corpo
#file = open("exemploErroNaoCorrespondenciaCorpo.txt",'r')
#Exemplo Erro de tipo no conjunto atribuído ao array maior que a sua capacidade
#file = open("exemploErroConjDemais.txt",'r')
parser.parse(file.read())