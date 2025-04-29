import random as rand
import os
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
    c=str()
    with open(a,'r'):
    c=rand.sample(a,)
