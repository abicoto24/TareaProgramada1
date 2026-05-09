
from funciones import *
tokens = []
conteos = []

opcion = ""
while opcion != "9":
    mostrarMenu()
    opcion = input("Elija una opción: ")
    if opcion == "1":
        cargarTokens(tokens)
    elif opcion == "2":
        print("Mostrar tokens")
    elif opcion == "3":
        agregarTokens(tokens)
    elif opcion == "4":
        print("Guardar tokens")
    elif opcion == "5":
        traducirCodigo(tokens, conteos)
    elif opcion == "6":
        print("Generar CSV")
    elif opcion == "7":
        generarHTML(tokens, conteos)
    elif opcion == "8":
        submenuBitacora()
    elif opcion == "9":
        print("Ha salido con éxito")
    else:
        print("Opción no válida")