import funcionesauxiliares as faux
import time
#Con esta función solo estamos chequeando si es que existe el texto adn, que es el que contiene todos los caracteres necesarios para realizar esta comparación.
faux.chequeadordearchivo()
a=None;
a=int(input("Coloca un numero entre el 6 al 10 para crear una muestra de 2** el numero que elegiste \n"))
while a not in [6,7,8,9,10]:
     print("no válido, realiza de nuevo")
     a=int(input("Coloca un numero entre el 6 al 10 para crear una muestra de 2** el numero que elegiste \n"))
with open('adn.txt','r') as file:
     c= file.read()
     texto=list(c)
patron= faux.muestra('adn.txt',a)

tiempo1bdm=time.perf_counter()
faux.bdm(patron,texto)
tiempo2bdm=time.perf_counter()
tiempobdm=tiempo2bdm-tiempo1bdm

#La implementacion del kpm trabaja con strings, así que los convertire el patrón a una string
stringpatron="".join(patron)
indiceskpm=[0]* len(stringpatron)
tiempo1kpm= time.time()
faux.pattern_search(c,stringpatron,indiceskpm)
tiempo2kpm= time.time()
tiempokpm=tiempo2kpm-tiempo1kpm

#implementacion del algoritmo bm

indicesbm=[0]*len(stringpatron)
index=[-1]
tiempo1bm=time.time()
faux.search_pattern(c,stringpatron,indicesbm,index)
tiempo2bm=time.time()
tiempobm=tiempo2bm-tiempo1bm


print("los tiempos de ejecución de los algoritmos BDM, KPM, y BM con 2^"+str(a)+"son"+"\n"+"BDM= "+str(tiempobdm)+"\nKPM= "+str(tiempokpm) +'\n BM= '+str(tiempobm))