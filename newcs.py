import curses
import pyfiglet,random
import time
from pygame import mixer

'w = 30 , h = 117'
'f(x) = w/2 - (tam text) /2.'

paci = None
menu = ['Formulario','Diagnostico','Numeros de pacientes','Sair']
dese = [""]
lista_ps = {}
cdt= {1:"Nome:",2:"Idade:",3:"Sexo:"}
perguntas = ["Temperatura","Nauseas","Dor Lombar","Dificuldade de Urinar","Dor ao Urinar","Queimação na Ureta"]

tempmax = 40.0
tempmin= 34.0

resposta = []
buffer = 40

def play_musica(caminho,ops):
  if ops == True:
     mixer.init()
     mixer.music.load(caminho)
     mixer.music.set_volume(10)
     mixer.music.play()
  else:
     mixer.music.pause()

def RNA(stdscr,temp, resposta):
  from rnae import RNAE
  from numpy import array


  rna = RNAE.carregar_modelo("../modelos/Diagnostico.txt")

  temperatura = temp
  normalizado=(temperatura - tempmin) / (tempmax-tempmin);

  entrada = array([normalizado,resposta[1],resposta[2],resposta[3],resposta[4],resposta[5]])
  pred = rna.propagacao(entrada)

  #stdscr.addstr(7,90,str(entrada))
  txt = pyfiglet.figlet_format("Diagnostico do Paciente:",font="small")
  stdscr.addstr(0,0,txt,curses.color_pair(1))
  stdscr.refresh()


  if pred[0][0] == 0 and pred[0][1] == 0:
     play_musica("../musica/03.wav",True)
     stdscr.addstr(9,30,"\nPaciente Saudavel"+str(pred),curses.color_pair(1))
     stdscr.refresh()

  elif pred[0][0] == 0 and pred[0][1] == 1:
        play_musica("../musica/03.wav",True)
        stdscr.addstr(9,30,"\nInflamação renal de origem pelvica"+str(pred),curses.color_pair(1))
        stdscr.refresh()

  elif pred[0][0] == 1 and pred[0][1] == 0:
        play_musica("../musica/03.wav",True)
        stdscr.addstr(9,30,"\nInflamação Urinar"+str(pred),curses.color_pair(1))
        stdscr.refresh()

  elif pred[0][0] == 1 and  pred[0][1] == 1:
       play_musica("../musica/03.wav",True)
       stdscr.addstr(9,30,"\nPaciente em estado terminal"+str(pred),curses.color_pair(1))
       stdscr.refresh()

  resposta.clear()#Limpar Lista
  entrada = []#limpar vetor
  id = stdscr.getch()

def diagnostico_paciente(stdscr):
   stdscr.clear()
   RNA(stdscr,resposta[0], resposta)

aux = 0
def validacao(stdscr,id):
   play_musica("../musica/01.wav",True)
   stdscr.clear()
   global aux
   if id is 0:
    stdscr.addstr(0,20,'''
    + Sintomas\n
    1-Temperatura\n
    2-Nauseas\n
    3-Dor Lombar\n
    4-Dificuldade de Urinar\n
    5-Dor ao Urinar\n
    6-Queimação na Ureta\n
    ''',curses.color_pair(4))


    stdscr.addstr(18,0,4*"-*-"+"Registro do Paciente:"+29*"-*-",curses.color_pair(1))
    for chave in cdt:
       aux +=1
       stdscr.addstr(19+(chave),10,"{0} {1}\n".format(chave,cdt[chave],curses.color_pair(1)))
       stdscr.refresh()
       paci =stdscr.getstr(19+(chave),10+11,buffer)
       lista_ps[aux] = paci




    for i in range(0,len(perguntas)):
     if i is 0:
      stdscr.addstr(23+(i+1),20,str(i+1)+"-"+"Qual a sua temperatura=",curses.color_pair(1))
      key = stdscr.getstr(23+(i+1),50,15)
      resposta.append(float(key))
      stdscr.addstr(23+(i+1),50,key)
      stdscr.refresh()

     else:
      stdscr.addstr(23+(i+1),20,str(i+1)+"-"+"voce tem " + perguntas[i] + " S/N",curses.color_pair(1))
      stdscr.refresh()
      key = stdscr.getch()
      resposta.append(chr(key))
      stdscr.addstr(23+(i+1),60,chr(key))
      stdscr.refresh()



    for i in range(1,len(perguntas)):
      if resposta[i] is 'S' or resposta[i] is 's':
          resposta[i] = 1
      else:
          resposta[i] = 0

    stdscr.addstr(29,20,str(resposta[i]))
    stdscr.refresh()



    stdscr.addstr(28,80,"S/N!",curses.color_pair(1))
    stdscr.refresh()
    key = stdscr.getch()


   else:
     stdscr.clear()
     stdscr.addstr(0,0,"Treinamento da Rede Neural...\n")
     stdscr.addstr(20,0,"ops S/N:",curses.color_pair(3))
     stdscr.refresh()



def desenho(stdscr,h,w):
    play_musica("../musica/01.wav",True)
    i=0;start = True
    curses.curs_set(1)
    h,w = stdscr.getmaxyx()
    #curses.start_color()
    txt = pyfiglet.figlet_format("RNAE-IA",font="small")
    stdscr.addstr(0,0,"Nome:Allan Ferreira de Souza e Matheus Herbert da Silva\nTrabalho:IA\nProfessor:Eduardo Pereira\nProjeto:RNAE",curses.color_pair(2))
    stdscr.refresh()


    win2=curses.newwin(9,44,6,50)
    value2 = pyfiglet.figlet_format("RNAE",font="doom")

    while i < 20 and start != False:
      i+=1
      win2.addstr(0,0,value2,curses.color_pair(1))
      win2.refresh()
      time.sleep(0.1)
      win2.addstr(0,0,value2,curses.color_pair(2))
      win2.refresh()
      time.sleep(0.1)
      if i >=20:
          start = False
          break
    win2.clear()
    win2.addstr(0,0,txt,curses.color_pair(1))
    win2.addstr(0,0,"Diagnostico",curses.color_pair(1))
    win2.refresh()
    time.sleep(3)


def rna_statico(stdscr):
    h,w = stdscr.getmaxyx()
    txt = pyfiglet.figlet_format("Diagnostico",font="small")
    stdscr.addstr(0,0,"diagnostico",curses.color_pair(2))
    stdscr.refresh()

    win2=curses.newwin(9,44,6,50)
    value2 = pyfiglet.figlet_format("RNAE",font="doom")
    win2.addstr(0,0,value2,curses.color_pair(2))
    win2.refresh()



def print_menu(stdscr, index):
    curses.echo()
    #screen = curses.initscr()
    stdscr.clear()
    h,w = stdscr.getmaxyx()
    global x,y
    for idx, row in enumerate(menu):
       x = w//2 - len(row)//2
       y = h//2 - len(menu)//2 + idx
       if idx is index:
          stdscr.attron(curses.color_pair(4))
          stdscr.addstr(y,x,str(idx+1)+" "+row)
          stdscr.attroff(curses.color_pair(4))
       else:
           stdscr.addstr(y,x,row)
    stdscr.refresh()

def main(stdscr):
      curses.curs_set(0)
      curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
      curses.init_pair(2, curses.COLOR_WHITE,curses.COLOR_BLACK)
      curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
      curses.init_pair(4, curses.COLOR_BLACK,curses.COLOR_WHITE)

      index = 0
      tempo = 4
      start = True


      h,w = stdscr.getmaxyx()
      desenho(stdscr,h,w)
      print_menu(stdscr,index)

      while True:
          for i in range(40):
            for j in range(30):
              stdscr.addstr(j,i,3*"-",curses.color_pair(1))
              stdscr.refresh()


          play_musica("../musica/01.wav",False)
          key = stdscr.getch()
          if key == curses.KEY_UP and index > 0:
              index -=1
              curses.beep()

          elif key == curses.KEY_DOWN and index < len(menu)-1:
              index +=1
              curses.beep()

          elif  key == curses.KEY_ENTER or key in [10,13] and index is 0:
               validacao(stdscr,index)


          elif  key == curses.KEY_ENTER or key in [10,13] and index is 1:
              diagnostico_paciente(stdscr)


          elif  key == curses.KEY_ENTER or key in [10,13] and index is 2:
                play_musica("../musica/01.wav",True)
                stdscr.clear()
                for k,v in lista_ps.items():
                 stdscr.addstr(0+(k),0,"{0} {1}\n".format(k,v),curses.color_pair(1))
                 stdscr.refresh()
                key = stdscr.getch()


          elif  key == curses.KEY_ENTER or key in [10,13] and index is 3:
               play_musica("../musica/01.wav",True)
               stdscr.clear()
               for s in menu:
                tempo-=1
                sec_et = pyfiglet.figlet_format("Fechando {0}".format(tempo),font="slant")
                stdscr.addstr(0,0,sec_et,curses.color_pair(1))
                stdscr.refresh()
                time.sleep(1)
               break

          elif key == ord('w'):
              stdscr.clear()
              for s in menu:
               tempo-=1
               sec_et = pyfiglet.figlet_format("Fechando {0}".format(tempo),font="slant")
               stdscr.addstr(0,0,sec_et,curses.color_pair(1))
               stdscr.refresh()
               time.sleep(1)
              break


          elif key == ord('s'):
               f = open("C:/Users/Allan/Documents/Allan/IA/Redes Neurais/rnae/example/modelos/Diagnostico.txt", "r")
               print(f.read())
               curses.flash()
               break



          else:
               stdscr.clear()
               sec_et = pyfiglet.figlet_format("Ops\nInvalida\n Tente novamente",font="slant")
               stdscr.addstr(0,0,sec_et,curses.color_pair(1))
               stdscr.refresh()
               key = stdscr.getch()

          print_menu(stdscr,index)

          stdscr.refresh()
curses.wrapper(main)
