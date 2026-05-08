import re
from datetime import datetime

tokens = []
conteos = []

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

def traducirLinea(linea, tokens, conteos):
    partes = re.findall(r'\b\w+\b|[^\w\s]|\s+', linea)
    resultado = []
    for parte in partes:
        reemplazado = False
        for token in tokens:
            if parte == token[0].strip():
                resultado.append(token[1].strip())
                reemplazado = True
                for i in range (len(conteos)):
                    if conteos[i][0] == token[0].strip():
                        conteos[i] = (conteos[i][0], conteos[i][1] + 1)
                        break
                break
        if not reemplazado:
            resultado.append(parte)
    return "".join(resultado)

opcion = ""
while opcion != "9":
    mostrarMenu()
    opcion = input ("Elija una opción: ")

    if opcion == "1":
        print("Cargar Tokens")
        nombreArchivo = input("Ingrese el nombre del archivo: ")
        separador = input("Ingrese el separador (->): ")
        try:
            with open(nombreArchivo, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(separador)
                    if len(partes) == 2:
                        tokens.append((partes[0].strip(), partes[1].strip()))
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
        cadena = input("ingrese los tokens o escriba 'cancelar' para salir: ")
        if cadena.lower() == "cancelar":
            print("Ha cancelado")
        else:
            separador = input("Ingrese el separador (->) y separe cada token con (|): ")
            pares = cadena.split("|")
            for par in pares:
                partes = par.strip().split(separador)
                if len(partes) == 2:
                    palabra = partes[0].strip()   
                    nuevoToken = partes[1].strip()
                    encontrado = False
                    for i in range (len(tokens)):
                        if tokens[i][0] == palabra:
                            encontrado = True
                            tokens[i] = (palabra, nuevoToken)
                            print("Token actualizado: ", palabra, "->", nuevoToken)
                            break
                    if not encontrado: 
                        tokens.append((palabra, nuevoToken))
                        print ("Token agregado: ", palabra, "->", nuevoToken)

    elif opcion == "4":
        print("Guardar tokens")
    elif opcion == "5":
        print("Traducir código")
        archivoTraducir = input("Ingrese el nombre del archivo a traducir: ")
        archivoSalida = input("Ingrese el nombre de archivo de salida: ")
        try: 
            with open(archivoTraducir, "r", encoding = "utf-8") as entrada:
                with open(archivoSalida, "w", encoding = "utf-8") as salida:
                    for linea in entrada:
                        lineaTraducida = traducirLinea(linea, tokens, conteos)
                        salida.write(lineaTraducida)
            print("Traducción completada con éxito.")
        except FileNotFoundError:
            print("Archivo no encontrado.")
       
    elif opcion == "6":
        print("Generar CSV")
    elif opcion == "7":
        print("Generar HTML")
        titulo = input("Ingrese el título del reporte: ")
        archivoTraducir = input("Ingrese el archivo a traducir: ")
        ahora = datetime.now()
        fechaHora = ahora.strftime("%d/%m/%y-%H:%M:%S")
        nombreHTML = "reporteHTML_" + fechaHora.replace("/", "-").replace(":", "-") + ".html"
        for token in tokens:
            conteos.append((token[0], 0))
        with open(nombreHTML, "w", encoding="utf-8") as html:
                html.write("<!DOCTYPE html>\n")
                html.write("<html>\n")
                html.write(f"<head><title>{titulo}</title></head>\n")
                html.write("<body>\n")
                html.write("<h1>Reporte de Traducción</h1>\n")
                html.write(f"<h2>Generado el: {fechaHora}</h2>\n")
                html.write("<table border='1' style='width:100%; text-align:center;'>\n")
                html.write("<tr><th>Palabra Original</th><th>Reemplazo</th><th>Cantidad</th></tr>\n")
                
                for i in range(len(conteos)):
                    if i % 2 == 0:
                        color = "#f7983f"
                    else:
                        color = "#f752b5"
                    html.write(f"<tr style='background-color:{color};'>")
                    html.write(f"<td>{conteos[i][0]}</td>")
                    html.write(f"<td>{tokens[i][1]}</td>")
                    html.write(f"<td>{conteos[i][1]}</td>")
                    html.write("</tr>\n")
                
                html.write("</table>\n")
                html.write("</body>\n")
                html.write("</html>\n")

        print("Reporte HTML generado:", nombreHTML)
                



    elif opcion == "8":
        submenuBitacora() 
    elif opcion == "9":
        print("Ha salido con éxito") 
    else:
        print("Opción no valida")

