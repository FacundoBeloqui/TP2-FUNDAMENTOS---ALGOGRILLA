import argparse, datetime, random, csv


def main():
    parser = argparse.ArgumentParser(description='Generador de Algogrillas')
    parser.add_argument('-s', '--solucion', action='store_true', help='imprimir la solución')
    parser.add_argument('-n', '--numero', help='número de algogrilla')
    args = parser.parse_args()

    if args.numero and args.numero.isdigit():
        numero_de_algogrilla = int(args.numero)
    else:
        numero_de_algogrilla = int(datetime.datetime.now().timestamp())
    random.seed(numero_de_algogrilla)

    imprimir_solucion = args.solucion  # es True si el usuario incluyó la opción -s

    frase, columnas, autores = elegir_frase()
    subfrase_1, subfrase_2 = separar_frase(frase)
    palabras_de_la_frase, silabas, descripcion = guardar_palabras(subfrase_1, subfrase_2, columnas)
    print(frase)
    grilla = crear_grilla(subfrase_1, subfrase_2, columnas, palabras_de_la_frase)

    if imprimir_solucion:
        mostrar_grilla(grilla, silabas, descripcion, autores)
    else:
        modo_interactivo(grilla, silabas, descripcion, autores, palabras_de_la_frase, columnas)


def normalizar(caracter):
    """Convierte las letras vocales que llevan tilde en su version normal(sin tilde)"""
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u'
    }

    if caracter in reemplazos:
        caracter = reemplazos[caracter]
    return caracter


def elegir_frase():
    """Elige una frase random del archivo frases.csv y devuelve por separado la solo la frase en si misma
    y las columnas en las que iran cada una de sus letras que compartan con las palabras seleccionadas"""
    try:
        with open('frases.csv') as archivo_frases:
            reader = csv.reader(archivo_frases, delimiter='|', quoting=csv.QUOTE_NONE)
            fila = random.choice(list(reader))
            frase = fila[0]
            frase = frase.split('"')[1]
            columnas = fila[1]
            autores = fila[2]
            return frase, columnas, autores
    except FileNotFoundError:
        print("No se encontro uno o mas archivos necesarios para la ejecucion del programa")
        exit()


def dividir_columnas(columnas):
    """separa las columnas del archivo frases.csv para poder ser usadas individualmente"""
    columnas = columnas.split(',')
    return int(columnas[0]) - 1, int(columnas[1]) - 1


def separar_frase(frase):
    """junta toda la frase eliminando espacios y caracteres no alfabeticos(ademas de convertir las vocales con tilde en su version normal)
    y luego la separa en 2 devolviendo las 2 subfrases respectivamente"""
    frase_caracteres_alfabeticos = ''
    for caracter in frase:
        caracter = caracter.lower()
        if caracter.isalpha():
            frase_caracteres_alfabeticos += normalizar(caracter)
    mitad = len(frase_caracteres_alfabeticos) // 2
    if len(frase_caracteres_alfabeticos) % 2 == 0:
        subfrase_1 = frase_caracteres_alfabeticos[:mitad]
        subfrase_2 = frase_caracteres_alfabeticos[mitad:]
    else:
        subfrase_1 = frase_caracteres_alfabeticos[:mitad + 1]
        subfrase_2 = frase_caracteres_alfabeticos[mitad + 1:len(frase_caracteres_alfabeticos) + 1]
    return subfrase_1, subfrase_2


def guardar_palabras(subfrase_1, subfrase_2, columnas):
    """Elige una palabra de palabras.csv que cumpla con que la posición de sus letras coincida con las de las columnas de la frase de la grilla,
       además devuelve sus sílabas y descripción en forma de diccionario para después ser usadas en la función mostrar grilla."""
    palabras_de_la_frase = {}
    silabas_de_la_frase = {}
    descripcion_de_la_frase = {}
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)

    try:
        with open('palabras.csv') as archivo_palabras:
            for linea in archivo_palabras:
                palabra, silabas, descripcion = linea.rstrip("\n").split('|')
                i = 0
                palabra_encontrada = False

                while i < max(len(subfrase_1), len(subfrase_2)):
                    if len(subfrase_1) > len(subfrase_2) and i == len(subfrase_1) - 1:
                        if columna_subfrase_2 > len(palabra) > columna_subfrase_1 and palabra[columna_subfrase_1] == \
                                subfrase_1[i]:
                            if i + 1 not in palabras_de_la_frase:
                                palabras_de_la_frase[i + 1] = palabra
                                silabas_de_la_frase[i + 1] = silabas
                                descripcion_de_la_frase[i + 1] = descripcion
                                palabra_encontrada = True
                                break
                    else:
                        if len(palabra) > max(columna_subfrase_1, columna_subfrase_2) and \
                                palabra[columna_subfrase_1] == subfrase_1[i] and palabra[columna_subfrase_2] == \
                                subfrase_2[i]:
                            if i + 1 not in palabras_de_la_frase:
                                palabras_de_la_frase[i + 1] = palabra
                                silabas_de_la_frase[i + 1] = silabas
                                descripcion_de_la_frase[i + 1] = descripcion
                                palabra_encontrada = True
                                break

                    i += 1
                if not palabra_encontrada:
                    continue

    except FileNotFoundError:
        print("No se encontró uno o más archivos necesarios para la ejecución del programa")
        exit()
    return dict(sorted(palabras_de_la_frase.items())), dict(sorted(silabas_de_la_frase.items())), dict(
        sorted(descripcion_de_la_frase.items()))


def crear_grilla(subfrase_1, subfrase_2, columnas, palabras_de_la_frase):
    """Crea una lista de listas que simula ser la grilla, la cual posee como cantidad de filas la mitad de la frase,
    a medida que se itera sobre cada fila, se inserta la letra de la subfrase que coincide con la columna especificada en la frase"""
    cant_filas = max(len(subfrase_1), len(subfrase_2))
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)
    grilla = []
    for _ in range(cant_filas):
        fila = []
        for _ in range(columna_subfrase_2):
            fila.append(" ")
        grilla.append(fila)
    for i in range(len(palabras_de_la_frase)):
        palabras = list(palabras_de_la_frase[i + 1])
        grilla[i] = palabras
        if len(subfrase_1) > len(subfrase_2) and i == len(subfrase_1) - 1:
            grilla[i][columna_subfrase_1] = grilla[i][columna_subfrase_1].upper()
            if len(subfrase_2) < columna_subfrase_2:
                grilla[i][columna_subfrase_2] = grilla[i][columna_subfrase_2].upper()
        else:
            grilla[i][columna_subfrase_1] = grilla[i][columna_subfrase_1].upper()
            grilla[i][columna_subfrase_2] = grilla[i][columna_subfrase_2].upper()
    return grilla


def mostrar_grilla(grilla, diccionario_silabas, diccionario_descripciones, autores):
    """Muestra la solucion de la grilla por pantalla"""
    for indice, fila in enumerate(grilla):
        fila_numero = f"{indice + 1} "
        if indice < 9:
            fila_numero = " " + fila_numero
        print(fila_numero + "".join(fila))
    print()
    print("DEFINICIONES")
    for indice, descripcion in diccionario_descripciones.items():
        print(indice, descripcion)
    print()
    print("SILABAS")
    for silabas in diccionario_silabas.values():
        silaba = silabas.split('-')
        silaba = random.choice(silaba)
        print(f"{silaba}, ", end='')
    print()
    print(f"Al finalizar se mostrara una frase de {autores}")


def quedan_puntos(grilla):
    """Devuelve False en caso de que no queden palabras sin rellenar y asi saber si el usuario termino el juego"""
    for fila in grilla:
        if '.' in fila:
            return True
    return False


def inicializar_diccionario_palabras(palabras, columnas):
    """Inicializa el diccionario con las palabras de la grilla para poder luego comparar con las ingresadas por el usuario"""
    diccionario_palabras = {}
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)
    for indice, palabra in palabras.items():
        palabra = palabra.lower()
        if len(palabra) > max(columna_subfrase_1, columna_subfrase_2):
            palabra = list(palabra)
            palabra[columna_subfrase_1] = palabra[columna_subfrase_1].upper()
            palabra[columna_subfrase_2] = palabra[columna_subfrase_2].upper()
        diccionario_palabras[indice] = ''.join(palabra)
    return diccionario_palabras


def normalizar_diccionario_palabras(diccionario_palabras):
    """Se les saca todas las posibles tildes a las palabras del diccionario para que luego no haya conflictos con las palabras
    ingresadas por el usuario"""
    for clave, palabra in diccionario_palabras.items():
        palabra_normalizada = []
        for letra in palabra:
            letra_normalizada = normalizar(letra)
            palabra_normalizada.append(letra_normalizada)
        diccionario_palabras[clave] = ''.join(palabra_normalizada)


def limpiar_grilla(grilla):
    """Convierte todos los caracteres de la grilla en puntos para que el usuario no sepa cuales son las palabras en cuestion"""
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            grilla[i][j] = '.' if grilla[i][j].isalpha() else grilla[i][j]


def pedir_numero_palabra():
    """Se inicia el ciclo en el cual se le pregunta al usuario por un numero que forme parte de la grilla
    y en caso contrario se lanza una excepcion hasta que se ingrese una respuesta acorde"""
    while True:
        try:
            numero_ingresado = int(input("Ingrese un numero de palabra o 0 para continuar: "))
            if numero_ingresado < 0:
                print("Ingrese un número del 0 en adelante")
            else:
                return numero_ingresado
        except ValueError:
            print("Ingrese un número válido, no una palabra.")


def verificar_palabra(grilla, diccionario_palabras, diccionario_silabas, diccionario_descripciones, autores,
                      numero_ingresado, palabra_ingresada):
    """Verifica si la palabra ingresada es correcta y actualiza la grilla y los diccionarios de silabas y frases."""
    if numero_ingresado in diccionario_palabras and palabra_ingresada == diccionario_palabras[numero_ingresado].lower():
        grilla[numero_ingresado - 1] = diccionario_palabras[numero_ingresado]
        print("Correcto!")
        del diccionario_descripciones[numero_ingresado]
        del diccionario_silabas[numero_ingresado]

        mostrar_grilla(grilla, diccionario_silabas, diccionario_descripciones, autores)
    else:
        print("¡Incorrecto!")


def modo_interactivo(grilla, diccionario_silabas, diccionario_descripciones, autores, palabras, columnas):
    """Función principal del modo interactivo del juego."""
    diccionario_palabras = inicializar_diccionario_palabras(palabras, columnas)
    limpiar_grilla(grilla)
    mostrar_grilla(grilla, diccionario_silabas, diccionario_descripciones, autores)

    normalizar_diccionario_palabras(diccionario_palabras)

    while True:
        if not quedan_puntos(grilla):
            print("Felicidades! Adivinaste todas las palabras")
            break

        numero_ingresado = pedir_numero_palabra()

        if numero_ingresado == 0:
            break

        palabra_ingresada = input("Ingrese la definicion de la palabra: ").lower()
        verificar_palabra(grilla, diccionario_palabras, diccionario_silabas, diccionario_descripciones, autores,
                          numero_ingresado, palabra_ingresada)


main()
