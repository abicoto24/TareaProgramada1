#Importa expresiones regulares
import re

#Importa la fecha y hora actual
from datetime import datetime

def mostrarMenu():
    """
    Funcionamiento:
    Muestra el menú principal del sistema con todas
    las opciones disponibles para el usuario.

    Entradas:
    Esta función no recibe entradas.

    Salidas:
    Esta función no retorna valores.
    """

    #Muestra el menú principal
    print ("\nMenú\n1. Cargar Tokens\n2. Mostrar Tokens\n3. Agregar/modificar Tokens\n4. Guardar Tokens\n5. Traducir código\n6. Generar CSV\n7. Generar HTML\n8. Submenú de bitácora\n9. Salir\n")

def mostrarSubmenu():
    """
    Funcionamiento:
    Muestra las opciones disponibles en el submenú
    de bitácora.

    Entradas:
    Esta función no recibe entradas.

    Salidas:
    Esta función no retorna valores.
    """

    #Muestra el título del submenú
    print("Submenú de bitácora\n")

    #Muestra las opciones del submenú
    print("A)Acciones por día recogido\nB)Acciones con algunas palabras clave\nC)Salir del submenú")

def submenuBitacora():
    """
    Funcionamiento:
    Controla el funcionamiento del submenú de
    bitácora y permite seleccionar diferentes
    opciones hasta que el usuario decida salir.

    Entradas:
    Esta función no recibe entradas.

    Salidas:
    Esta función no retorna valores.
    """

    #Variable para almacenar la opción seleccionada
    opcionSub = ""

    #Ciclo que se mantiene hasta que el usuario salga
    while opcionSub != "C" and opcionSub != "c":

        #Muestra el submenú
        mostrarSubmenu()

        #Solicita una opción al usuario
        opcionSub = input("Elija una opción: ").strip()

        #Verifica si el usuario eligió la opción A
        if opcionSub == "A" or opcionSub == "a":

            print("Filtrar por día")

        #Verifica si el usuario eligió la opción B
        elif opcionSub == "B" or opcionSub == "b":

            print("Filtrar por palabra clave")

        #Verifica si el usuario desea salir
        elif opcionSub == "C" or opcionSub == "c":

            print("Volviendo al menú principal...")

        #Mensaje de error si la opción no existe
        else:

            print("Opción no válida")

def traducirLinea(linea, tokens, conteos):
    """
    Funcionamiento:
    Traduce una línea de texto reemplazando las
    palabras encontradas en la lista de tokens.
    Además, actualiza la cantidad de veces que
    cada token fue utilizado.

    Entradas:
    - linea(str): Línea de texto a traducir.
    - tokens(list): Lista de tuplas con los tokens
      originales y sus reemplazos.
    - conteos(list): Lista con la cantidad de usos
      de cada token.

    Salidas:
    - (str): Línea traducida.
    """

    #Separa palabras, símbolos y espacios
    partes = re.findall(r'\b\w+\b|[^\w\s]|\s+', linea)

    #Lista donde se almacenará el resultado final
    resultado = []

    #Recorre cada parte encontrada
    for parte in partes:

        #Variable para saber si hubo reemplazo
        reemplazado = False

        #Recorre todos los tokens
        for token in tokens:

            #Verifica si la palabra coincide con un token
            if parte == token[0].strip():

                #Agrega el reemplazo
                resultado.append(token[1].strip())

                #Indica que sí hubo reemplazo
                reemplazado = True

                #Recorre los conteos
                for i in range(len(conteos)):

                    #Busca el token correspondiente
                    if conteos[i][0] == token[0].strip():

                        #Aumenta el contador de uso
                        conteos[i] = (conteos[i][0], conteos[i][1] + 1)

                        break

                break

        #Si no hubo reemplazo deja la palabra original
        if not reemplazado:

            resultado.append(parte)

    #Une todas las partes traducidas
    return "".join(resultado)

def abrirArchivo(nombreArchivo, modo):
    """
    Funcionamiento:
    Abre un archivo utilizando el nombre y modo
    especificados.

    Entradas:
    - nombreArchivo(str): Nombre del archivo.
    - modo(str): Modo de apertura del archivo.

    Salidas:
    - (file): Archivo abierto correctamente.
    - (None): Si el archivo no existe.
    """

    #Intenta abrir el archivo
    try:

        archivo = open(nombreArchivo, modo, encoding="utf-8")

        return archivo

    #Captura error si el archivo no existe
    except FileNotFoundError:

        print("Archivo no encontrado.")

        return None

def validarEntrada(valor):
    """
    Funcionamiento:
    Verifica que una entrada no esté vacía.

    Entradas:
    - valor(str): Texto ingresado por el usuario.

    Salidas:
    - (bool): True si la entrada es válida.
    - (bool): False si está vacía.
    """

    #Verifica si el texto está vacío
    if valor.strip() == "":

        print("Este espacio no puede estar vacío.")

        return False

    #Retorna verdadero si la entrada es válida
    return True



def cargarTokens(tokens):
    """
    Funcionamiento:
    Carga tokens desde un archivo de texto y los
    almacena en una lista.

    Entradas:
    - tokens(list): Lista donde se almacenarán los
      tokens cargados.

    Salidas:
    Esta función no retorna valores.
    """

    #Solicita el nombre del archivo
    nombreArchivo = input("Ingrese el nombre del archivo: ")

    #Valida la entrada
    if not validarEntrada(nombreArchivo):

        return

    #Solicita el separador
    separador = input("Ingrese el separador (->): ")

    #Valida el separador
    if not validarEntrada(separador):

        return

    #Abre el archivo en modo lectura
    archivo = abrirArchivo(nombreArchivo, "r")

    #Verifica si el archivo existe
    if archivo is None:

        return

    #Recorre cada línea del archivo
    for linea in archivo:

        #Divide la línea usando el separador
        partes = linea.strip().split(separador)

        #Verifica que existan dos partes
        if len(partes) == 2:

            #Guarda el token y su reemplazo
            tokens.append((partes[0].strip(), partes[1].strip()))

        else:

            #Mensaje si la línea está mal escrita
            print(f"Línea mal formateada con separador '{separador}', se omite: {linea.strip()}")

    #Cierra el archivo
    archivo.close()

    #Muestra cantidad de tokens cargados
    print("Tokens cargados:", len(tokens))

    #Muestra cada token
    for token in tokens:

        print(token[0], "->", token[1])

def mostrarTokens(tokens):
    """
    Funcionamiento:
    Despliega en consola todas las equivalencias
    de tokens actualmente en memoria, con un formato
    de tabla clara y numerada para el usuario.

    Entradas:
    - tokens(list): Lista de tuplas con los tokens.

    Salidas:
    Esta función no retorna valores.
    """
    #Verifica si hay tokens cargados
    if len(tokens) == 0:
        print("No hay tokens cargados en memoria.")
        return
    #Encabezado de la tabla
    print("\n" + "=" * 46)
    print(f"  {'#':<5} {'Palabra Original':<20} {'Reemplazo'}")
    print("=" * 46)
    #Recorre y muestra cada token numerado
    for i in range(len(tokens)):
        print(f"  {i + 1:<5} {tokens[i][0]:<20} {tokens[i][1]}")
    #Pie de la tabla
    print("=" * 46)
    print(f"  Total de tokens en memoria: {len(tokens)}")
    print("=" * 46 + "\n")

def agregarTokens(tokens):
    """
    Funcionamiento:
    Permite agregar nuevos tokens o modificar
    tokens existentes dentro de la lista.

    Entradas:
    - tokens(list): Lista de tokens del sistema.

    Salidas:
    Esta función no retorna valores.
    """

    #Título de la opción
    print("Agregar/modificar tokens")

    #Solicita los tokens
    cadena = input("ingrese los tokens o escriba 'cancelar' para salir: ")

    #Verifica si el usuario canceló
    if cadena.lower() == "cancelar":

        print("Ha cancelado")

    else:

        #Solicita el separador
        separador = input("Ingrese el separador (->) y separe cada token con (|): ")

        #Separa cada par de tokens
        pares = cadena.split("|")

        #Recorre cada par
        for par in pares:

            #Divide usando el separador
            partes = par.strip().split(separador)

            #Verifica que el formato sea correcto
            if len(partes) == 2:

                #Obtiene la palabra original
                palabra = partes[0].strip()

                #Obtiene el nuevo token
                nuevoToken = partes[1].strip()

                #Variable para verificar si existe
                encontrado = False

                #Recorre la lista de tokens
                for i in range(len(tokens)):

                    #Verifica si el token ya existe
                    if tokens[i][0] == palabra:

                        encontrado = True

                        #Actualiza el token
                        tokens[i] = (palabra, nuevoToken)

                        print("Token actualizado: ", palabra, "->", nuevoToken)

                        break

                #Si no existe lo agrega
                if not encontrado:

                    tokens.append((palabra, nuevoToken))

                    print("Token agregado: ", palabra, "->", nuevoToken)

def guardarTokens(tokens):
    """
    Funcionamiento:
    Persiste la lista actual de tokens en un archivo
    de texto nuevo. Solicita al usuario el nombre
    del archivo y el separador a utilizar.

    Entradas:
    - tokens(list): Lista de tuplas con los tokens.

    Salidas:
    Esta función no retorna valores.
    """
    #Verifica si hay tokens para guardar
    if len(tokens) == 0:
        print("No hay tokens cargados para guardar.")
        return
    #Solicita el nombre del archivo de destino
    nombreArchivo = input("Ingrese el nombre del archivo de salida (ej: tokens.txt): ")
    #Valida la entrada
    if not validarEntrada(nombreArchivo):
        return
    #Solicita el separador a usar en el archivo
    separador = input("Ingrese el separador a usar (ej: ->, =, ,): ")
    #Valida el separador
    if not validarEntrada(separador):
        return
    #Abre el archivo en modo escritura
    archivo = abrirArchivo(nombreArchivo, "w")
    #Verifica si se abrió correctamente
    if archivo is None:
        return
    #Escribe cada token en el archivo con el separador elegido
    for token in tokens:
        archivo.write(f"{token[0]}{separador}{token[1]}\n")
    #Cierra el archivo
    archivo.close()
    print(f"Se guardaron {len(tokens)} token(s) en '{nombreArchivo}' con el separador '{separador}'.")

def traducirCodigo(tokens, conteos):
    """
    Funcionamiento:
    Traduce el contenido de un archivo utilizando
    los tokens cargados y guarda el resultado
    en un nuevo archivo.

    Entradas:
    - tokens(list): Lista de tokens.
    - conteos(list): Lista de conteos de reemplazos.

    Salidas:
    - (list): Lista actualizada de conteos.
    """

    #Verifica si existen tokens cargados
    if len(tokens) == 0:

        print("No hay tokens cargados. Use la opción 1 primero.")

        return conteos

    #Solicita archivo de entrada
    archivoTraducir = input("Ingrese el nombre del archivo a traducir: ")

    #Valida entrada
    if not validarEntrada(archivoTraducir):

        return conteos

    #Solicita archivo de salida
    archivoSalida = input("Ingrese el nombre del archivo de salida: ")

    #Valida entrada
    if not validarEntrada(archivoSalida):

        return conteos

    #Verifica que no sean iguales
    if archivoTraducir == archivoSalida:

        print("El archivo de entrada y salida no pueden ser el mismo.")

        return conteos

    #Abre el archivo de entrada
    entrada = abrirArchivo(archivoTraducir, "r")

    #Verifica si se abrió correctamente
    if entrada is None:

        return conteos

    #Abre el archivo de salida
    salida = abrirArchivo(archivoSalida, "w")

    #Verifica si hubo error al abrir salida
    if salida is None:

        entrada.close()

        return conteos

    #Limpia la lista de conteos
    conteos.clear()

    #Inicializa los conteos en cero
    for token in tokens:

        conteos.append((token[0], 0))

    #Recorre cada línea del archivo
    for linea in entrada:

        #Traduce la línea
        lineaTraducida = traducirLinea(linea, tokens, conteos)

        #Escribe la línea traducida
        salida.write(lineaTraducida)

    #Cierra archivos
    entrada.close()
    salida.close()

    print("Traducción completada con éxito.")

    return conteos

def generarCSV(tokens, conteos):
    """
    Funcionamiento:
    Genera un archivo .csv con la información de
    los reemplazos realizados: palabra original,
    token de reemplazo y cantidad de reemplazos.
    Entradas:
    - tokens(list): Lista de tuplas con los tokens.
    - conteos(list): Lista de conteos de reemplazos.
    """
    #Verifica si hay tokens cargados
    if len(tokens) == 0:
        print("No hay tokens cargados.")
        return
    #Verifica si ya se realizó una traducción
    if len(conteos) == 0:
        print("No hay traducción realizada. Use la opción 5 primero.")
        return
    #Solicita el nombre del archivo CSV
    nombreCSV = input("Ingrese el nombre del archivo CSV (ej: reporte.csv): ")
    #Valida la entrada
    if not validarEntrada(nombreCSV):
        return
    #Agrega la extensión si el usuario no la escribió
    if not nombreCSV.endswith(".csv"):

        nombreCSV += ".csv"
    #Abre el archivo en modo escritura
    archivo = abrirArchivo(nombreCSV, "w")
    #Verifica si se abrió correctamente
    if archivo is None:
        return
    #Escribe la fila de encabezado
    archivo.write("Palabra Original,Token de Reemplazo,Cantidad de Reemplazos\n")
    #Recorre los conteos para escribir cada fila
    for i in range(len(conteos)):
        #Obtiene la palabra original y su cantidad de usos
        palabraOriginal = conteos[i][0]
        cantidad = conteos[i][1]
        #Busca el reemplazo correspondiente en la lista de tokens
        reemplazo = ""
        for token in tokens:
            if token[0] == palabraOriginal:
                reemplazo = token[1]
                break
        #Escribe la fila en el CSV
        archivo.write(f"{palabraOriginal},{reemplazo},{cantidad}\n")
    #Cierra el archivo
    archivo.close()
    print(f"Reporte CSV generado: '{nombreCSV}' con {len(conteos)} registro(s).")

def generarHTML(tokens, conteos):
    """
    Funcionamiento:
    Genera un reporte HTML con la información de
    los tokens utilizados y la cantidad de veces
    que fueron reemplazados.

    Entradas:
    - tokens(list): Lista de tokens.
    - conteos(list): Lista de conteos de reemplazos.

    Salidas:
    Esta función no retorna valores.
    """

    #Verifica si hay tokens cargados
    if len(tokens) == 0:

        print("No hay tokens cargados.")

        return

    #Verifica si ya hubo traducción
    if len(conteos) == 0:

        print("No hay traducción realizada. Use la opción 5 primero.")

        return

    #Solicita título del reporte
    titulo = input("Ingrese el título del reporte: ")

    #Valida entrada
    if not validarEntrada(titulo):

        return

    #Obtiene fecha y hora actual
    ahora = datetime.now()

    #Da formato a la fecha
    fechaHora = ahora.strftime("%d/%m/%y-%H:%M:%S")

    #Genera nombre automático del archivo
    nombreHTML = "reporteHTML_" + fechaHora.replace("/", "-").replace(":", "-") + ".html"

    #Abre el archivo HTML
    html = abrirArchivo(nombreHTML, "w")

    #Verifica si hubo error
    if html is None:

        return

    #Escribe estructura HTML
    html.write("<!DOCTYPE html>\n")
    html.write("<html>\n")
    html.write(f"<head><title>{titulo}</title></head>\n")
    html.write("<body>\n")
    html.write("<h1>Reporte de Traducción</h1>\n")
    html.write(f"<h2>Generado el: {fechaHora}</h2>\n")
    html.write("<table border='1' style='width:100%; text-align:center;'>\n")
    html.write("<tr><th>Palabra Original</th><th>Reemplazo</th><th>Cantidad</th></tr>\n")

    #Recorre los conteos
    for i in range(len(conteos)):

        #Alterna colores entre filas
        if i % 2 == 0:

            color = "#f7983f"

        else:

            color = "#f752b5"

        #Escribe fila de la tabla
        html.write(f"<tr style='background-color:{color};'>")
        html.write(f"<td>{conteos[i][0]}</td>")
        html.write(f"<td>{tokens[i][1]}</td>")
        html.write(f"<td>{conteos[i][1]}</td>")
        html.write("</tr>\n")

    #Cierra etiquetas HTML
    html.write("</table>\n")
    html.write("</body>\n")
    html.write("</html>\n")

    #Cierra el archivo
    html.close()

    print("Reporte HTML generado:", nombreHTML)