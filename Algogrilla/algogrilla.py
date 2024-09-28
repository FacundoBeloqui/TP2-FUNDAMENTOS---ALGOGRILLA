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

    frase, columnas = elegir_frase()
    subfrase_1, subfrase_2 = separar_frase(frase)
    palabras_de_la_frase, silabas, descripcion = guardar_palabras(subfrase_1, subfrase_2, columnas)
    grilla = crear_grilla(subfrase_1, subfrase_2, columnas, palabras_de_la_frase)

    print(frase)
    print(palabras_de_la_frase)
    for index, fila in enumerate(grilla):
        fila_numero = f"{index + 1} "
        if index < 9:
            fila_numero = " " + fila_numero
        print(fila_numero + "".join(fila))


def normalizar(caracter):
    """Convierte las letras vocales que llevan tilde en su version normal(sin tilde)"""
    reemplazos = (
        ('a', 'á'),
        ('e', 'é'),
        ('i', 'í'),
        ('o', 'ó'),
        ('u', 'ú')
    )
    for letra_normal, letra_con_tilde in reemplazos:
        if caracter == letra_con_tilde:
            caracter = letra_normal
    return caracter


def elegir_frase():
    """Elige una frase random del archivo frases.csv y devuelve por separado la frase en si misma
    y las columnas en las que iran cada una de sus letras que compartan con las palabras seleccionadas"""
    with open('frases.csv') as archivo_frases:
        reader = csv.reader(archivo_frases, delimiter='|', quoting=csv.QUOTE_NONE)
        fila = random.choice(list(reader))
        frase = fila[0]
        columnas = fila[1]
        return frase, columnas


def dividir_columnas(columnas):
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
    mitad = len(frase_caracteres_alfabeticos) // 2
    subfrase_1 = frase_caracteres_alfabeticos[:mitad]
    subfrase_2 = frase_caracteres_alfabeticos[mitad:]
    return subfrase_1, subfrase_2


def guardar_palabras(subfrase_1, subfrase_2, columnas):
    """Elige una palabra de palabras.csv que cumpla con que la posicion de sus letras coincida con las de las columnas de la frase de la grilla,
       ademas devuelve sus silabas y descripcion para despues ser usadas en la funcion mostrar grilla"""
    palabras_de_la_frase = []
    silabas_de_la_frase = []
    descripcion_de_la_frase = []
    columna_subfrase_1, columna_subfrase_2 = dividir_columnas(columnas)
    with open('palabras.csv') as archivo_palabras:
        reader = csv.reader(archivo_palabras, delimiter='|')
        lista_palabras = list(reader)
        for i, letra_1 in enumerate(subfrase_1):
            if i < len(subfrase_2):
                letra_2 = subfrase_2[i]
                for palabra, silabas, descripcion in lista_palabras:
                    if len(palabra) > max(columna_subfrase_1, columna_subfrase_2):
                        if palabra[columna_subfrase_1] == letra_1 and palabra[columna_subfrase_2] == letra_2:
                            palabras_de_la_frase.append(palabra)
                            silabas_de_la_frase.append(silabas)
                            descripcion_de_la_frase.append(descripcion)
                            break
    return palabras_de_la_frase, silabas_de_la_frase, descripcion_de_la_frase

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
main()
