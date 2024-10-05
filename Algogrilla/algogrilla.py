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
    grilla = crear_grilla(subfrase_1, columnas, palabras_de_la_frase)
    if imprimir_solucion:
        print(frase)
        mostrar_grilla(grilla, silabas, descripcion, autores)
    else:
        modo_interactivo(grilla, silabas, descripcion, autores, palabras_de_la_frase, columnas)


def normalizar(caracter):
    """Convierte las letras vocales que llevan tilde en su version normal(sin tilde)"""
    reemplazos = {
        'a': 'á',
        'e': 'é',
        'i': 'í',
        'o': 'ó',
        'u': 'ú'
    }
    for letra_normal, letra_con_tilde in reemplazos.items():
        if caracter == letra_con_tilde:
            caracter = letra_normal
    return caracter


def elegir_frase():
    """Elige una frase random del archivo frases.csv y devuelve por separado la frase en si misma
    y las columnas en las que iran cada una de sus letras que compartan con las palabras seleccionadas"""
    try:
        with open('frases.csv') as archivo_frases:
            reader = csv.reader(archivo_frases, delimiter='|', quoting=csv.QUOTE_NONE)
            fila = random.choice(list(reader))
            frase = fila[0]
            if "(Primera parte)" in frase:
                frase = frase.strip("(Primera parte)")
            if "(Conclusión)" in frase:
                frase = frase.strip("(Conclusión)")
            columnas = fila[1]
            autores = fila[2]
            return frase, columnas, autores
    except FileNotFoundError:
        print("No se encontro uno o mas archivos necesarios para la ejecucion del programa")
        exit()


def dividir_columnas(columnas):
    """separa las columnas del archivo frases.csv para poder ser usadas individualmente"""
    columnas = columnas.split(',')
    lista_columnas = []
    for columna in columnas:
        columna = int(columna)
        lista_columnas.append(columna)
    columna_subfrase_1, columna_subfrase_2 = lista_columnas[0] - 1, lista_columnas[1] - 1
    return columna_subfrase_1, columna_subfrase_2

def separar_frase(frase):
    """junta toda la frase eliminando espacios y caracteres no alfabeticos(ademas de convertir las vocales con tilde en su version normal)
    y luego la separa en 2 devolviendo las 2 subfrases respectivamente"""
    frase_caracteres_alfabeticos = ''
    for caracter in frase:
        caracter = caracter.lower()
        if caracter.isalpha():
            frase_caracteres_alfabeticos += normalizar(caracter)
    mitad = (len(frase_caracteres_alfabeticos) + 1) // 2
    subfrase_1 = frase_caracteres_alfabeticos[:mitad]
    subfrase_2 = frase_caracteres_alfabeticos[mitad:]
    return subfrase_1, subfrase_2


def guardar_palabras(subfrase_1, subfrase_2, columnas):
    """Elige una palabra de palabras.csv que cumpla con que la posicion de sus letras coincida con las de las columnas de la frase de la grilla,
       ademas devuelve sus silabas y descripcion en forma de diccionario para despues ser usadas en la funcion mostrar grilla"""
    palabras_de_la_frase = []
    silabas_de_la_frase = {}
    descripcion_de_la_frase = {}
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)
    try:
        with open('palabras.csv') as archivo_palabras:
            reader = csv.reader(archivo_palabras, delimiter='|')
            lista_palabras = list(reader)
            for i in range(min(len(subfrase_1), len(subfrase_2))):
                letra_1 = subfrase_1[i]
                letra_2 = subfrase_2[i]
                for palabra, silabas, descripcion in lista_palabras:
                    if len(palabra) > max(columna_subfrase_1, columna_subfrase_2):
                        if palabra[columna_subfrase_1] == letra_1 and palabra[columna_subfrase_2] == letra_2:
                            if palabra not in palabras_de_la_frase:
                                palabras_de_la_frase.append(palabra)
                                silabas_de_la_frase[i] = silabas
                                descripcion_de_la_frase[i] = descripcion
                                break
        return palabras_de_la_frase, silabas_de_la_frase, descripcion_de_la_frase
    except FileNotFoundError:
        print("No se encontro uno o mas archivos necesarios para la ejecucion del programa")
        exit()
def crear_grilla(subfrase_1, columnas, palabras_de_la_frase):
    """Crea una lista de listas que simula ser la grilla, la cual posee como cantidad de filas la mitad de la frase,
    a medida que se itera sobre cada fila, se inserta la letra de la subfrase que coincide con la columna especificada en la frase"""
    cant_filas = len(subfrase_1)
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)
    grilla = []
    for _ in range(cant_filas):
        fila = []
        for _ in range(columna_subfrase_2):
            fila.append(" ")
        grilla.append(fila)
    for i in range(cant_filas):
        if i < len(palabras_de_la_frase):
            palabras = list(palabras_de_la_frase[i])
            grilla[i] = palabras
            palabras[columna_subfrase_1] = palabras[columna_subfrase_1].upper()
            palabras[columna_subfrase_2] = palabras[columna_subfrase_2].upper()
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
        if indice < (len(diccionario_descripciones) + 1):
            print(indice + 1, descripcion)
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
    for i in range(len(palabras)):
        palabras[i] = palabras[i].lower()
        if len(palabras[i]) > max(columna_subfrase_1, columna_subfrase_2):
            palabras[i] = list(palabras[i])
            palabras[i][columna_subfrase_1] = palabras[i][columna_subfrase_1].upper()
            palabras[i][columna_subfrase_2] = palabras[i][columna_subfrase_2].upper()
        diccionario_palabras[i + 1] = ''.join(palabras[i])
    return diccionario_palabras


def normalizar_diccionario_palabras(diccionario_palabras):
    """Se les saca todas las posibles tilder a las palabras del diccionario para que luego no haya conflictos con las palabras
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
                raise ValueError("No se permiten numeros negativos.")
            return numero_ingresado
        except ValueError:
            print("Ingrese un número válido, no una palabra.")


def verificar_palabra(grilla, diccionario_palabras, diccionario_silabas, diccionario_descripciones, autores,
                      numero_ingresado, palabra_ingresada):
    """Verifica si la palabra ingresada es correcta y actualiza la grilla y los diccionarios."""
    if numero_ingresado in diccionario_palabras and palabra_ingresada == diccionario_palabras[numero_ingresado].lower():
        grilla[numero_ingresado - 1].append(diccionario_palabras[numero_ingresado])
        print("Correcto!")
        for i in range(len(grilla[numero_ingresado - 1])):
            if '.' in grilla[numero_ingresado - 1]:
                grilla[numero_ingresado - 1].remove('.')
        del diccionario_descripciones[numero_ingresado - 1]
        del diccionario_silabas[numero_ingresado - 1]

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
