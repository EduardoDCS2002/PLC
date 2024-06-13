import re 

#----------------------------------------------------------------------------------------------------------------------------------

# Calcular a frequência de registos por Província e por Local (de preferência considerar apenas o Concelho quando 
# referido após o lugar
def alineaA():
    f = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')

    #Saltar a primeira linha
    char = f.read(1)
    while char != '\n':
        char = f.read(1)
    #Criar dicionário com cada provincia e valor de frequencia que aparece
    dic_provincias = {}
    dic_localidades = {}

    print("\n-----------------Alínea a-----------------\n")
    print("Frequência de registos por Província e por Local (Concelho):\n")
    #Começar pelas províncias
    print("Províncias:\n")

    #Tem que corresponder ao padrao "Primeiro letra maiscula até chegar a '::'" por cada linha
    #Criar um dicionário com a sua frequência
    for linha in f:
        y = re.search (r'^[A-Z][^::]+',linha) #Tem que começar por letra maiúscula
        if y and (y.group() not in dic_provincias): #Se a parte de y que satisfez o search
            dic_provincias[y.group()] = 1
        else: 
            if y: dic_provincias[y.group()] = dic_provincias.get(y.group(), 0)+1

    #Dar print da frequencia 
    for provincia in dic_provincias:        
        print ("A província {provincia} tem {x} registo(s) neste documento"
               .format(provincia = provincia, x =dic_provincias[provincia]))

    print("\n\n")

    #localidades/Concelhos

    fd = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')
    print("Concelhos:\n")

    #Saltar a primeira linha
    char = fd.read(1)
    while char != '\n':
        char = fd.read(1)

    for linha in fd:
        #Dividir por "::"
        y = re.split(r'::',linha)
        x = y[1] #Segundo elemento de cada array criado

        d2 = r'd2.*' #Caso não tenha a localidade na 2ª posição e tem o link da música (d2)
        d1 = r'd1.*' #Caso não tenha a localidade na 2ª posição e tem o link da música (d1)
        jR = r"José dos Reis (palheta)" #Caso específico do José Reis que não tem localidade identificada
        nome_provincia = r'^[A-Z][^::]+' #O primeiro elemento tem que ser provincia (por padrão)
        nome_localidade = r'[A-Z].*' #O segundo elemento tem que ser Localidade (por padrão)
        if (re.match(d2,y[2])) or (not(re.match(nome_provincia,y[0]))) or (not(re.match(nome_provincia,y[1]))): 
            continue #Se não satisfazer os requeridos passa para o próximo
        if (re.match(d1,y[3])): 
            continue #Exemplo da Afinação da gaita galega
        if (jR == y[2]): 
            continue #Não funciona com match
        if re.search(";",y[1]):
            continue #Se tiver ponto de vírgula refere-se à parte musical

        #Fazer um dicionário localidade:frequencia eliminando espaços amais e '?'
        if x not in dic_localidades:
            dic_localidades[re.sub(r'\s+', " ", re.sub(r'\s\?' , "" ,x))] = 1
        else: 
            dic_localidades[re.sub(r'\s+', " ", re.sub(r'\s\?' , "" ,x))] = dic_localidades.get(re.sub(r'\s+', " ", re.sub(r'\s\?' , "" ,x)), 0)+1

    #print do local/concelho e da sua frequencia no documento 
    for local_concelho in dic_localidades:
        if re.search(",",local_concelho):
            if dic_localidades[local_concelho] == 1: #Singular        
                print(f"A localidade de \"{local_concelho}\" tem {dic_localidades[local_concelho]} registo neste documento")
            else: #Plural
                print(f"A localidade de \"{local_concelho}\" tem {dic_localidades[local_concelho]} registos neste documento")
        else:
            if dic_localidades[local_concelho] == 1: #Singular        
                print(f"O concelho de \"{local_concelho}\" tem {dic_localidades[local_concelho]} registo neste documento")
            else: #Plural
                print(f"O concelho de \"{local_concelho}\" tem {dic_localidades[local_concelho]} registos neste documento")

#----------------------------------------------------------------------------------------------------------------------------------

# b) Calcular a percentagem de canções que têm pelo menos uma gravação "mp3", indicando o título dessas canções;
#re.findall(pattern, string[, flags])
def alineaB():
    f = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')

    #Saltar a primeira linha
    char = f.read(1)
    while char != '\n':
        char = f.read(1)

    print("\n-----------------Alínea b-----------------\n")
    print("Calcular a percentagem de canções que têm pelo menos uma gravação \"mp3\": \n")
    
    cancoes=[]
    countmp3=0
    count=0
    for linha in f:
        count+=1 # contagem de todas as canções
        if re.search("mp3", linha):
            countmp3+=1 # contagem das canções com mp3
            x = re.split("::", linha) # a organização do texto coloca as canções em 3º lugar
            if len(x)>=3:
                if not(re.search("mp3", x[2])):                      #ignorar as instâncias mp3 no nome
                    if not(re.search(";", x[2])):                    #ignorar o que não são canções
                        if not(re.search("Não identificado", x[2])): #Ignora "Não identificado"
                            if not(re.search("José dos Reis", x[2])):#Ignora caso específico "José dos Reis"
                                if not(re.search(r"[0-9]",x[2])):    #Não pode ter números
                                    if x[2] not in cancoes: # Não repetir canções   
                                        cancoes.append(x[2])

    percentagem=(countmp3/count)*100 # percentagem de mp3
    for cancao in cancoes:
        print(f"- \"{cancao}\"")
    print("A percentagem de canções com pelo menos um mp3 é {p}\n".format(p=percentagem))

#----------------------------------------------------------------------------------------------------------------------------------

#Calcular a distribuição por instrumento musical
def alineaC():
    f = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')

    #Saltar a primeira linha
    char = f.read(1)
    while char != '\n':
        char = f.read(1)

    print("\n-----------------Alínea c-----------------\n")
    dic = {}
    for linha in f:
        x = re.split(r"::", linha)
        elemento = x[3] # ficar com o cantor(instrumento)
        elemento = elemento.lower() # 
        
        if re.search(r"[0-9]", elemento): # ignorar coisas com dígitos
            continue

        if(re.search(r"[(]", elemento)): # se o instrumento estiver entre parenteses temos de separar do resto
            instrumentosParenteses = re.split(r"[()]", elemento) # queremos o que está entre os parenteses, ou seja indice 1 da lista

            instrumentosVirgulas =  re.split(r";", instrumentosParenteses[1]) # separar os vários instrumentos
            if len(instrumentosVirgulas) == 1: # se nao há ; nos parenteses
                if instrumentosParenteses[1] in dic:
                    qt = dic[instrumentosParenteses[1]]
                    dic[instrumentosParenteses[1]] = qt + 1
                else:
                    dic[instrumentosParenteses[1]] = 1
                continue
            else:
                for instrumentoVirgula in instrumentosVirgulas:
                    instrumentosOu = re.split("ou", instrumentoVirgula) # separar instrumentos
                    if len(instrumentosOu) == 1: # se nao há OU nos parenteses
                        if instrumentoVirgula in dic:
                            qt = dic[instrumentoVirgula]
                            dic[instrumentoVirgula] = qt + 1
                        else:
                            dic[instrumentoVirgula] = 1
                        continue
                    else:
                        for instrumentoOu in instrumentosOu:
                            if instrumentoOu in dic:
                                qt = dic[instrumentoOu]
                                dic[instrumentoOu] = qt +1
                            else:
                                dic[instrumentoOu] = 1
    del dic["ver anexo"] #Caso específico do "ver anexo"
    for instrumento in dic:
        if dic[instrumento] == 1:
            print("O instrumento " + instrumento +" acontece "+ str(dic[instrumento]) + " vez")
        else:
            print("O instrumento " + instrumento +" acontece "+ str(dic[instrumento]) + " vezes")

#----------------------------------------------------------------------------------------------------------------------------------

#Identificar todos os Musicos/cantores registados e calcular o número de vezes que são mencionados
def alineaD():
    f = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')

    #Saltar a primeira linha
    char = f.read(1)
    while char != '\n':
        char = f.read(1)

    print("\n-----------------Alínea d-----------------\n")
    print("Cantores e os seus Registos no documento:\n")

    #Criar dicionário cantor:frequencia
    dic_cantores = {}
    arr_cantores = []

    for linha in f:
        x = re.split('::',linha)
        x = x[3]

        #Um cantor tem que começar por letra Maiuscula e ter pelo menos 2 nomes
        ''' Elimina o Ms, HS, M'''
        padrao_cantor = r'^\s*[A-Z][a-z]+\s.*$'

        x = re.sub("\(.*\)","",x) #Retirar os instrumentos entre parenteses

        x = re.split(";",x)

        #Fazer por cada cantor um cantor:nmr_musicas e não pode ser um instrumento
        for cantor in x:
            if re.match(padrao_cantor,cantor) and not re.match(r'\s*Gaita de Foles\s*',cantor):
                if cantor not in dic_cantores:
                    dic_cantores[cantor] = 1
                else:
                    dic_cantores[cantor] += 1 
            else:
                continue

    #tirar dups e retirar os espaços amais no fim e no final passando para um dicionário auxiliar
    dic_cantores = list(dic_cantores.items())
    dic_cantores2 = {}
    for i in range (0,len(dic_cantores)):
        if dic_cantores[i][0] in dic_cantores2:
            dic_cantores2[re.sub(r'\s$',"",re.sub(r'^\s+', "", dic_cantores[i][0]))] = dic_cantores2.get(dic_cantores[i][0])+dic_cantores[i][1]
        else:
            dic_cantores2[re.sub(r'\s$',"",re.sub(r'^\s+', "", dic_cantores[i][0]))] = dic_cantores[i][1]   

    #Print dos cantores e da quantidade de músicas que tem retirando espaços em branco
    for cantor in dic_cantores2:
        if dic_cantores2[cantor] == 1:
            print ("O Musico/Grupo \"{cantor}\" tem {x} música neste documento"
                   .format(cantor = cantor, x = dic_cantores2[cantor]))    
        else:
            print ("O Musico/Grupo \"{cantor}\" tem {x} músicas neste documento"
                   .format(cantor = cantor, x = dic_cantores2[cantor]))  

#----------------------------------------------------------------------------------------------------------------------------------

#Construir um Grafo de Canções/Cantores que associa cada canção aos cantores/tocadores referidos no registo. Para
# visualizar o grafo, descarregue os triplos para uma ficheiro DOT que possa depois ser aberto por um visualizador
# como o que pode ser encontrado em http://www.webgraphviz.com/.
def alineaE():
    f = open("arq-son.txt", "r", encoding='utf-8', errors='ignore')

    #Saltar a primeira linha
    char = f.read(1)
    while char != '\n':
        char = f.read(1)

    #Definir um padrão para cada cantor (Começa com letra maiúscula e tem mais que 1 letra)
    padrao_cantor = r'^\s*[A-Z][a-z]+\s.*$'
    dic_cantores = {}

    print("\n-----------------Alínea e-----------------\n")
    print("Input para o grafo: \n")

    for linha in f:
        x = re.split('::',linha) #Separar por ::
        x2 = re.split(";",x[3]) #4º elemento é o cantor

        for cantor in x2:
            y = cantor
            y = re.sub("\(.*\)","",y) #Retirar os instrumentos entre parenteses
            y = re.sub(r'\s$',"",re.sub(r'^\s+', "",y)) #Retirar espaços amais

            if re.match(padrao_cantor,y) and (y!="Gaita de Foles"): #Tem que ter o padrão de cantor (Gaita de Foles caso específico)
                if y not in dic_cantores:
                    dic_cantores[y] = [re.sub(";.*","",x[2])] #Associar a música ao cantor retirando tudo após ";"
                else:
                    dic_cantores[y] = dic_cantores[y] + [re.sub(";.*","",x[2])]
                    #Elimina o que está para além do ponto e virgula 

    myKeys = list(dic_cantores.keys())
    myKeys.sort() #Ordenar alfabeticamente
    dic_sorted = {i: dic_cantores[i] for i in myKeys}

    #Dar print do grafo como um input para o "webgraphviz"
    print("digraph g{")
    print("    rankdir=LR;")

    #Pelo dicionário associar o cantor a sua musica
    for cantor in dic_sorted:
        for musica in dic_sorted[cantor]:
            print(f"    \"{musica}\" -> \"{cantor}\"")

    print("}")

#----------------------------------------------------------------------------------------------------------------------------------

#Print das alineas
print("Qual alínea? (a,b,c,d,e ou \"fim\")")

x = input()
while x !="fim":
    if (x == "a"):
        alineaA()
    if (x == "b"):
        alineaB()
    if (x == "c"):
        alineaC()
    if (x == "d"):
        alineaD()
    if (x == "e"):
        alineaE()
    print("Mais alguma alinea? (a,b,c,d,e ou \"fim\")")
    x = input()