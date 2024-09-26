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
    with open('frases.csv') as frases:
        reader = csv.reader(frases, delimiter='|', quoting=csv.QUOTE_NONE)
        fila = random.choice(list(reader))
        frase = fila[0]
        return frase


def separar_frase(frase):
    frase_caracteres_alfabeticos = ''
    frase_sin_espacios = frase.strip(' ')
    for caracter in frase_sin_espacios:
        caracter = caracter.lower()
        if caracter.isalpha():
            frase_caracteres_alfabeticos += normalizar(caracter)
    subfrase_1, subfrase_2 = frase_caracteres_alfabeticos[
                             :len(frase_caracteres_alfabeticos) // 2], frase_caracteres_alfabeticos[
                                                                       len(frase_caracteres_alfabeticos) // 2:]
    return subfrase_1, subfrase_2

