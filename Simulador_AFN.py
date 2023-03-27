file = open("AFN.txt","r")
lines = []
lines = file.readlines()
count=0
alfabeto = []
estados = []
finais = []
transicoes = []
cadeia = []
caminhos = []
loop_control=[]

for line in lines:
  count += 1
  #le alfabeto
  if count == 1 :
    txt = line.strip()
    txt = txt.replace(" ","")
    aux= txt.split("=");
    alfabeto = aux[1].split(",")
  #le estados
  if count == 2 :
    txt = line.strip()
    txt = txt.replace(" ","")
    aux= txt.split("=");
    estados = aux[1].split(",")
  #le inicial
  if count == 3 :
    txt = line.strip()
    txt = txt.replace(" ","")
    aux= txt.split("=");
    inicial = aux[1]
  #le finais
  if count == 4 :
    txt = line.strip()
    txt = txt.replace(" ","")
    aux= txt.split("=");
    finais = aux[1].split(",")
  #le transicoes
  if count > 5:
    txt = line.strip()
    txt = txt.replace(" ","")
    aux= txt.split(",");
    transicoes.append(aux.copy())


transicoes = sorted(transicoes)
aux.clear()

file.close() #fim da leitura

#validação da AFN
print("Validando a AFN ... \n")
for transicao in transicoes:
  if transicao==[]:
    break
  if not (transicao[2] in alfabeto):
    if transicao[2] != 'epsilon':
      print(transicao)
      print("Eh uma transicao com simbolo invalido")
      exit(1)

for transicao in transicoes:
  if transicao==[]:
    break
  if (not(transicao[0] in estados)) or (not(transicao[1] in estados)):
    print(transicao)
    print("Eh uma transicao com estado invalido")
    exit(1)

if not (inicial in estados):
  print(inicial)
  print("Estado inicial nao eh valido")
  exit(1)

if finais != ['']:
  for final in finais:
    if not(final in estados):
      print("O estado final " + final+ " não eh valido")
      exit(1)
      
print("O automato eh valido!") #fim da validacao

#funcao de processamento
def process(estado_atual, transicoes, estados, finais, cadeia):
  if len(cadeia) == 0: #verifica se terminou de percorrer a cadeia
    if finais == ['']: # automaticamente rejeita se não houver estados finais
      caminhos.append(aux.copy())
      caminhos[-1].append("rejeita")
      return 0
    for final in finais: #verifica se o estado atual eh um estado final
       if estado_atual == final:
         x = aux.copy()
         x.append("aceita")
         caminhos.append(x)
         return 1
    for transicao1 in transicoes: #verifica se tem transicoes epsilon a percorrer
      if transicao1[0] == estado_atual:
        if transicao1[2] == "epsilon":
          for transicao2 in loop_control:
            if transicao1 == transicao2:
              aux.pop()
              return 0
          loop_control.append(transicao1)
          aux.append(transicao1)
          process(transicao1[1], transicoes, estados, finais, cadeia) 
          loop_control.pop()
          aux.pop()
    caminhos.append(aux.copy())
    if len(caminhos) >= 2:
      y = caminhos[-2].copy()
      tamanho = len(y)
      for i in range(tamanho):
        if caminhos[-1]==y:
          caminhos.pop()
          return 0
        y.pop()

    caminhos[-1].append("rejeita")
    return 0
    
  for transicao in transicoes:
    if transicao == []:
      break
    if transicao[0] == estado_atual: 
      if transicao[2] == "epsilon":
        aux.append(transicao)
        for transicao2 in loop_control:
            if transicao == transicao2:
              aux.pop()
              return 0
        loop_control.append(transicao)
        process(transicao[1], transicoes, estados, finais, cadeia)
        loop_control.pop()
        aux.pop()
      if cadeia[0] == transicao[2]:
        aux.append(transicao)
        process(transicao[1], transicoes, estados, finais, cadeia[1:])
        aux.pop()
  caminhos.append(aux.copy())
  
  if len(caminhos) >= 2:
    y = caminhos[-2].copy()
    tamanho = len(y)
    for i in range(tamanho):
      if caminhos[-1]==y:
        caminhos.pop()
        return 0
      y.pop()
  caminhos[-1].append("rejeita")
  return 0



cadeia = input("Digite a cadeia de entrada para ser processada: \n")

process(inicial, transicoes, estados, finais, cadeia)

for caminho in caminhos:
  if caminhos == ['']:
    print("['" + inicial + "', 'rejeita']")
    quit(0)
  if caminho == ['rejeita']:
    break
  print(caminho)
