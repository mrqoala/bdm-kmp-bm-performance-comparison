import funcionesauxiliares as faux
#Con esta función solo estamos chequeando si es que existe el texto adn, que es el que contiene todos los caracteres necesarios para realizar esta comparación.
faux.chequeadordearchivo()
a=None;
a=int(input("Coloca un numero entre el 6 al 10 para crear una muestra de 2** el numero que elegiste \n"))
while a not in [6,7,8,9,10]:
     print("no válido, realiza de nuevo")
     a=int(input("Coloca un numero entre el 6 al 10 para crear una muestra de 2** el numero que elegiste \n"))
muestra= faux.muestra('adn.txt',a)
