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
    with open('frases.csv') as frases:
        reader = csv.reader(frases, delimiter='|', quoting=csv.QUOTE_NONE)
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
    return lista_columnas


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


def crear_grilla(subfrase_1, subfrase_2, columnas):
    """Crea una lista de listas que simula ser la grilla, la cual posee como cantidad de filas la mitad de la frase,
    a medida que se itera sobre cada fila, se inserta la letra de la subfrase que coincide con la columna especificada en la frase"""
    cant_filas = len(subfrase_1)
    columnas = dividir_columnas(columnas)
    grilla = []
    for _ in range(cant_filas):
        fila = []
        for _ in range(max(columnas) + 2):
            fila.append(" ")
        grilla.append(fila)
    for i in range(cant_filas):
        grilla[i][columnas[0]] = subfrase_1[i]
        grilla[i][columnas[1]] = subfrase_2[i]
    return grilla


frase, columnas = elegir_frase()
subfrase_1, subfrase_2 = separar_frase(frase)
grilla = crear_grilla(subfrase_1, subfrase_2, columnas)
print(frase)
for fila in grilla:
    print("".join(fila))
