tokens = []

def mostrarMenu():
    print ("\nMenú\n")
    print ("1. Cargar Tokens")
    print ("2. Mostrar tokens")
    print ("3. Agregar/modificar token")
    print ("4. Guardar tokens")
    print ("5. Traducir código")
    print ("6. Generar CSV")
    print ("7. Generar HTML")
    print ("8. Submenú de bitácora")
    print ("9. Salir\n")

def mostrarSubmenu():
    print("Submenú de bitácora\n")
    print("A)Acciones por día recogido\nB)Acciones con algunas palabras clave\nC)Salir del submenú")

def submenuBitacora():
    opcionSub = ""
    while opcionSub != "C" and opcionSub != "c":
        mostrarSubmenu()
        opcionSub = input("Elija una opción: ")
        if opcionSub == "A" or opcionSub == "a":
            print("Filtrar por día")
        elif opcionSub == "B" or opcionSub == "b":
            print("Filtrar por palabra clave")
        elif opcionSub == "C" or opcionSub == "c":
            print("Volviendo al menú principal...")
        else:
            print("Opción no válida")

opcion = ""
while opcion != "9":
    mostrarMenu()
    opcion = input ("Elija una opción: ")

    if opcion == "1":
        print("Cargar Tokens")
        nombreArchivo = input("Ingrese el nombre del archivo: ")
        separador = input("Ingrese el separador usado (->): ")
        try:
            with open(nombreArchivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(separador)
                    if len(partes) == 2:
                        tokens.append((partes[0], partes[1]))
                    else:
                        print("Debe contener dos elementos")
            print("Tokens cargados: ", len(tokens))
                   
            for token in tokens:
                 print(token[0], "->", token[1])
                
        except FileNotFoundError:
            print("Archivo no encontrado.")

    elif opcion == "2":
        print("Mostrar tokens")
    elif opcion == "3":
        print("Agregar/modificar tokens")
    elif opcion == "4":
        print("Guardar tokens")
    elif opcion == "5":
        print("Traducir código")
    elif opcion == "6":
        print("Generar CSV")
    elif opcion == "7":
        print("Generar HTML")
    elif opcion == "8":
        submenuBitacora() 
    elif opcion == "9":
        print("Ha salido con éxito") 
    else:
        print("Opción no valida")

