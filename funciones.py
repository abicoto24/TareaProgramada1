import re
from datetime import datetime

def mostrarMenu():
    print ("\nMenú\n1. Cargar Tokens\n2. Mostrar Tokens\n3. Agregar/modificar Tokens\n4. Guardar Tokens\n5. Traducir código\n6. Generar CSV\n7. Generar HTML\n8. Submenú de bitácora\n 9. Salir\n")

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

def abrirArchivo(nombreArchivo, modo):
    try:
        archivo = open(nombreArchivo, modo, encoding="utf-8")
        return archivo
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return None
    
def validarEntrada(valor):
    if valor.strip() == "":
        print("Este espacio no puede estar vacío.")
        return False
    return True
    
def cargarTokens(tokens):
    nombreArchivo = input("Ingrese el nombre del archivo: ")
    if not validarEntrada(nombreArchivo):
        return
    
    separador = input("Ingrese el separador (->): ")
    if not validarEntrada(separador):
        return
    
    archivo = abrirArchivo(nombreArchivo, "r")
    if archivo is None:
        return
    
    for linea in archivo:
        partes = linea.strip().split(separador)
        if len(partes) == 2:
            tokens.append((partes[0].strip(), partes[1].strip()))
        else:
            print(f"Línea mal formateada con separador '{separador}', se omite: {linea.strip()}")
    archivo.close()
    
    print("Tokens cargados:", len(tokens))
    for token in tokens:
        print(token[0], "->", token[1])

def agregarTokens(tokens):
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

def traducirCodigo(tokens, conteos):
    if len(tokens) == 0:
        print("No hay tokens cargados. Use la opción 1 primero.")
        return conteos
    
    archivoTraducir = input("Ingrese el nombre del archivo a traducir: ")
    if not validarEntrada(archivoTraducir):
        return conteos
    
    archivoSalida = input("Ingrese el nombre del archivo de salida: ")
    if not validarEntrada(archivoSalida):
        return conteos
    
    entrada = abrirArchivo(archivoTraducir, "r")  # ← abrís para leer
    if entrada is None:
        return conteos
    
    salida = abrirArchivo(archivoSalida, "w")     # ← abrís para escribir
    if salida is None:
        entrada.close()                            # ← cerrás entrada si salida falló
        return conteos
    
    conteos.clear()
    for token in tokens:
        conteos.append((token[0], 0))
    
    for linea in entrada:
        lineaTraducida = traducirLinea(linea, tokens, conteos)
        salida.write(lineaTraducida)
    
    entrada.close()                                # ← cerrás ambos al final
    salida.close()
    
    print("Traducción completada con éxito.")
    return conteos

def generarHTML(tokens, conteos):
    if len(tokens) == 0:
        print("No hay tokens cargados.")
        return
    
    if len(conteos) == 0:
        print("No hay traducción realizada. Use la opción 5 primero.")
        return
    
    titulo = input("Ingrese el título del reporte: ")
    if not validarEntrada(titulo):
        return
    
    ahora = datetime.now()
    fechaHora = ahora.strftime("%d/%m/%y-%H:%M:%S")
    nombreHTML = "reporteHTML_" + fechaHora.replace("/", "-").replace(":", "-") + ".html"
    
    html = abrirArchivo(nombreHTML, "w")  # ← abrís para escribir
    if html is None:
        return
    
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
    
    html.close()  # ← cerrás el archivo
    print("Reporte HTML generado:", nombreHTML)
 