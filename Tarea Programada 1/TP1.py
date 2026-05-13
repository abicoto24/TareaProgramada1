#Elaborado por: Abigail Coto Chaves y Felipe Durán
#Fecha de creacion: 24/4/2026
#Ultima modificacion: 12/5/2026
#Version: 3.15
 
from funciones import *
 
tokens = []
conteos = []
 
#Variables para estadísticas del HTML
duracion = 0.0
totalPalabras = 0
 
opcion = ""
while opcion != "9":
    mostrarMenu()
    opcion = input("Elija una opción: ").strip()
    if opcion == "1":
        cargarTokens(tokens)
    elif opcion == "2":
        mostrarTokens(tokens)
    elif opcion == "3":
        agregarTokens(tokens)
    elif opcion == "4":
        guardarTokens(tokens)
    elif opcion == "5":
        #Recibe los tres valores de retorno de traducirCodigo
        resultado = traducirCodigo(tokens, conteos)
        conteos = resultado[0]
        duracion = resultado[1]
        totalPalabras = resultado[2]
    elif opcion == "6":
        generarCSV(tokens, conteos)
    elif opcion == "7":
        generarHTML(tokens, conteos, duracion, totalPalabras)
    elif opcion == "8":
        submenuBitacora()
    elif opcion == "9":
        print("Ha salido con éxito")
    else:
        print("Opción no válida")