import random as rand
import os
import sys
#Esta funcion que creamos, se llama creadorAleatorioDeCadenas, y tiene 3 argumentos tipo str int str -> None , no retorna un elemento explicitamente.
#Entregas una lista, el largo que quieres que sea la cadena resultante, y el nombre de un archivo para colocarla
def creadorAleatorioDeCadenas(a,b,c):
    lista=[]
    for i in range(b):
        lista.append(rand.choice(a))
    cadena=''.join(lista) 
    with open(c,'w') as file:
        file.write(cadena)

#Función que sirve para chequear si existe el archivo deseado, si este es el caso, se omite, en cambio si no existe, se crea utilizando la función creada arriba y los parámetros de la tarea, se podría abstraer más pero no es necesario.
def chequeadordearchivo():
    directorioactual=os.getcwd()
    if os.path.exists((directorioactual+'/adn.txt')):
        pass
    else:
        creadorAleatorioDeCadenas(['A','T','C','G'],2**20,'adn.txt')

def muestra(a,b):
    muestra=[]
    with open(a,'r') as file:
        c=file.read()
        d=(list(c))
        i=rand.randint(0,len(d)-(2**b))
        j=0
        while j< (2**b):
            muestra.append(d[i])
            j+=1
            i+=1
    return muestra

def delta(q,p,i):
    a={(f"q_{i}",f"p_,{i}"):f"q_{i+1}"}
    return a

def deltaEpsilon(q,i):
    a={(f"q_{0}","ε"):f"q_{i}"}
    return a


def S(p):
    estados=set()
    transicion=[]
    m=len(p)
    #Creamos el estado inicial de forma q_(m+1)
    estados.add(f"q_{m+1}")
    for i in range(m,0,-1):
        estados.add(f"q_{i}")
        transicion.append(delta('q','p',i))
    estados.add(f"q_{0}")
    for i in range(1,m):
        transicion.append(deltaEpsilon('q',i))
   
    class Automata:
        def __init__(self,name,estados,transicion):
            self.name=name
            self.estados=sorted(estados)
            self.transiciones=transicion
    
    a=Automata('sufijos',estados,transicion)
    return a 

