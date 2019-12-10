import os,random,time
from numpy import array
delay = 1.0

tempmax = 40.0
tempmin= 34.0
sintomas = []

perguntas = ["Temperatura","Nauseas","Dor Lombar","Dificuldade de Urinar","Dor ao Urinar","Queimação na Ureta"]
nome = '''
          -Trabalho:IA
          -nome:Allan Ferreira de Souza
          -Professor:Eduardo Pereira\n
          - vs->1.0'''
print(nome)
time.sleep(delay)

def paciente_diag():
    pass

def RNA(temp, resposta):
  from rnae import RNAE
  from numpy import array
  rna = RNAE.carregar_modelo("../modelos/Diagnostico.txt")

  temperatura = temp
  normalizado=(temperatura - tempmin) / (tempmax-tempmin);

  entrada = array([normalizado,resposta[1],resposta[2],resposta[3],resposta[4],resposta[5]])
  pred = rna.propagacao(entrada)
  #print("\n\nPerguntas:"+str(entrada))
  #print("Diagnostico: "+str(pred))

  if pred[0][0] == 0 and pred[0][1] == 0:
        print("\nDiagnostico do Paciente:\n"+"Paciente Saudavel"+str(pred))

  elif pred[0][0] == 0 and pred[0][1] == 1:
        print("\nDiagnostico do Paciente:\nInflamação renal de origem pelvica"+str(pred))

  elif pred[0][0] == 1 and pred[0][1] == 0:
        print("\nDiagnostico do Paciente:\nInflamação Urinar"+str(pred))

  elif pred[0][0] == 1 and  pred[0][1] == 1:
       print("\nDiagnostico do Paciente:"+"\nPaciente em estado terminal"+str(pred))


  x=input("\nfim")


def menu():
    print('\nDiagnostico IA\n'
    '''
    - 1 start
    - 2 Treinamento
    - 3 exit
    \n''')
    ops = int(input("ops:"))
    return ops

def ficha():
    print('''
    \nSintomas do Paciente

                       1-Temperatura\n
                       2-Nauseas\n
                       3-Dor Lombar\n
                       4-Dificuldade de Urinar\n
                       5-Dor ao Urinar\n
                       6-Queimação na Ureta
    \n''')
    nome = input("Nome:")
    Data = input("Data:")
    sexo = input("Sexo:")

    return sintomas
ids = []
while True:
    cls = os.system('clear' if os.name == 'posix' else 'cls')
    ops =  menu()
    if ops == 1:
         cls = os.system('clear' if os.name == 'posix' else 'cls')
         print("Diagbostico")
         ficha()
         print("Perguntas\n\n")
         for i in range(0,len(perguntas)):
             if i is 0:
                ids.append(float(input(str(i+1)+"-"+"A sua Temperatura esta alta=")))
             else:
                 ids.append(input(str(i+1)+"-"+"voce "+ " tem " + perguntas[i] + " S/N="))
                 if ids[i] is 'S' or ids[i] is's':
                   ids[i]=1
                 else:
                   ids[i] = 0

         x = input("\n-----")
         RNA(ids[0],ids)

    elif ops == 2:
         cls = os.system('clear' if os.name == 'posix' else 'cls')
         f = open("C:/Users/Allan/Documents/Allan/IA/Redes Neurais/rnae/example/modelos/Diagnostico.txt", "r")
         print(f.read())
         x  =input()
    else:
         cls = os.system('clear' if os.name == 'posix' else 'cls')
         print("sair")
         break
