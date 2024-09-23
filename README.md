# 
TP2 - La Algogrilla
Consigna

El objetivo del trabajo práctico es implementar un generador de grillas interactivo.
Archivos de datos

Se dispone de dos archivos de datos: uno de frases y otro de palabras.

El archivo frases.csv tiene el siguiente formato:

frase|columnas|autor

Dentro de la columna frase, la frase propiamente dicha se encuentra delimitada por comillas.

El archivo palabras.csv tiene el siguiente formato:

palabra|sílabas|definición

Las sílabas se encuentran separadas por guiones.

Partiendo de una entrada del archivo de frases tomada al azar (una distinta cada vez que se ejecuta) se debe generar una grilla utilizando palabras también elegidas al azar del otro archivo.
La Algogrilla

Una grilla es un juego de ingenio en el que hay que adivinar una serie de palabras, dadas sus definiciones y con la ayuda de conocer las sílabas que las conforman. Como recompensa, al completar todas las palabras de la grilla develamos una frase que se forma al leer en vertical sobre las palabras de la grilla.

Para construir la grilla debe tomarse la frase (y solo la frase) seleccionada y quedarse únicamente con sus caracteres alfabéticos. La frase se parte al medio y se coloca en vertical en las columnas indicadas por el archivo. Se tiene entonces tantas filas como la mitad del largo de la frase.

Luego se buscan palabras que se crucen con las letras de la frase en las columnas indicadas. Se debe buscar palabras para cada fila sin repetir palabras.

Una vez acomodadas toda las palabras con respecto a la frase, se tiene creada nuestra Algogrilla.
Ejemplo

Supongamos que tenemos la frase ¡Vamos Algogrilla! atribuida a Alan Turing, y que corresponda a columnas 2 y 5.

En primer lugar, trabajaremos sobre la frase vamosalgogrilla y al partirla en dos nos quedarán dos subfrases vamosalg y ogrilla.

La primera palabra tendrá que tener una v en la posición 2 y una o en la 5, la segunda tendrá a y g en 2 y 5 respectivamente, y así. La última palabra tendrá una g en la segunda posición pero tendrá que medir menos de 5 caracteres.

Para la primera palabra podríamos usar cualquiera de estas palabras: avalorar, avetoro, aviso, avizorado, avizorar, aviñonés, avícola, evaporar, evaporiza, overol, oviforme, ovinos, ovívoro o uviforme. Supongamos que elegimos evaporar.

Repitiendo para las demás posiciones podemos elegir: evaporar, categoría, impar, nórdico, escalón, cabello, ilegal y ogro.

Nuestra grilla entonces será:

   *  *
1 eVapOrar
2 cAteGoría
3 iMpaR
4 nÓrdIco
5 eScaLón
6 cAbeLlo
7 iLegAl
8 oGro

Nota 1: Como puede observarse para nuestro crucigrama las mayúsculas y minúsculas son equivalentes (por ejemplo, las de la frase) y las vocales son indiferentes a las tildes (por ejempo, la o de vamos encaja con la ó de nórdico). Se sugiere hacer funciones que puedan convertir palabras a versiones normalizadas de ellas (por ejemplo, la versión normalizada de Panamá sería panama).

Nota 2: Si bien son bajas las chances de que ocurra, es posible que no exista una combinación de palabras que resuelven el problema para una frase. En caso de llegar a una condición que no pueda resolverse, elegir otra frase de entre las disponibles.
Salida

El programa debe imprimir la grilla lista para ser jugada, mostrando los casilleros disponibles para las letras, los números de palabras, las definiciones de cada palabra, las sílabas disponibles y el autor de la frase.

Se deja a libre elección el formato en el que se muestra cada elemento, pero se sugiere un ejemplo a continuación.

Si el programa recibe la opción -s (ejemplo: python tp2.py -s), además debe imprimir la solución de la grilla y terminar la ejecución.

En caso de que no se pida ver la solución, el programa entrará al modo interactivo en el cual el usuario podrá resolver la grilla.
Interacción

En el modo interactivo el programa esperará un número de palabra, luego de validado esperará la solución para esa palabra. Si la palabra ingresada como solución por el usuario es efectivamente la respuesta acertada se marcará como resuelta esa palabra.

Las palabras resueltas tendrán que aparecer completas en la grilla, además de que se dejará de mostrar su definición y sus sílabas.

En caso de que el usuario en vez del número de una palabra ingrese el 0 se terminará la ejecución del programa.
Ejemplo

Supongamos el siguiente ejemplo de ejecución, en base a la grilla del ejemplo anterior:

$ python tp2.py
ALGOGRILLA NÚMERO 1234

   *  *
1 ........
2 .........
3 .....
4 .......
5 .......
6 .......
7 ......
8 ....

DEFINICIONES
1 Convertir un cuerpo líquido o sólido en vapor
2 Fig. Jerarquía, grupo en que se puede clasificar distintos objetos
3 Número que no es exactamente divisible por dos
4 Del norte
5 Peldaño de una escalera
6 Pelo que nace en la cabeza del hombre, y conjunto de todos ellos
7 Ilícito, que es contra la ley
8 Según los cuentos y creencias populares, gigante que se alimentaba de carne humana

SÍLABAS
a, be, ca, ca, ca, co, di, e, es, gal, go, gro, i, im, le, llo, lón, nór, o, par, po, rar, rí, te, va

Al finalizar leerá una frase de Alan Turing, matemático inglés.

Ingrese un número de palabra o 0 para terminar: _

Ahora el usuario ingresa 3 seguido de impar:

Ingrese un número de palabra o 0 para terminar: 3
Ingrese la definición de la palabra: impar
¡Correcto!

   *  *
1 ........
2 .........
3 iMpaR
4 .......
5 .......
6 .......
7 ......
8 ....

DEFINICIONES
1 Convertir un cuerpo líquido o sólido en vapor
2 Fig. Jerarquía, grupo en que se puede clasificar distintos objetos
4 Del norte
5 Peldaño de una escalera
6 Pelo que nace en la cabeza del hombre, y conjunto de todos ellos
7 Ilícito, que es contra la ley
8 Según los cuentos y creencias populares, gigante que se alimentaba de carne humana

SÍLABAS
a, be, ca, ca, ca, co, di, e, es, gal, go, gro, i, le, llo, lón, nór, o, po, rar, rí, te, va

Ingrese un número de palabra o 0 para terminar: _

Ahora el usuario ingresa 4 seguido de boreal:

Ingrese un número de palabra o 0 para terminar: 4
Ingrese la definición de la palabra: boreal
¡Incorrecto!

Ingrese un número de palabra o 0 para terminar: _

El programa seguirá hasta que se ingrese 0 y se aborte o se resuelvan todas las palabras en cuyo caso se mostrará la frase (por ejemplo ¡Vamos algogrilla!) y se terminará.
Parámetros de la línea de comandos

Como se mencionó, se espera que cuando el usuario ejecute la aplicación con -s se modifique el comportamiento del programa para mostrar la solución y no interactuar.

Además, para que el usuario pueda continuar una Algogrilla ya jugada (o el programador probar con casos ya conocidos) se pide que si el usuario ingresa -n <numerodegrilla> se genere la grilla en cuestión.

Dado que el procesamiento de los argumentos de la línea de comandos excede el alcance de este trabajo se provee el siguiente fragmento que implementa la lógica de ambas cosas:

import argparse, datetime, random

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

    imprimir_solucion = args.solucion # es True si el usuario incluyó la opción -s

    ...

main()

Dentro de main() y al final de ese fragmento estarán definidas dos variables: imprimir_solucion booleana que nos dice si se ejecutó con -s y numero_de_algogrilla que nos da un número que debería servirnos para repetir la secuencia de valores pseudoaleatorios de esta ejecución en cualquier otra.
Restricciones y condiciones de entrega

    El programa nunca debe finalizar con una excepción no capturada.
    En caso de algún error al procesar los archivos CSV (error de entrada/salida), el programa debe finalizar mostrando un mensaje de error apropiado.
    Se puede asumir que el contenido de los archivos respeta el formato especificado.
    Los archivos solo pueden recorrerse una única vez.
    El código debe estar correctamente modularizado, documentado, y seguir las convenciones y buenas prácticas establecidas por el lenguaje y el curso.
    El código debe ser eficiente, con uso responsable de archivos y eligiendo las estructuras correctas para la solución de los problemas correspondientes.
    El uso de módulos de la biblioteca estándar de Python deberá ser previamente autorizado por un docente. El módulo csv está permitido sin previa autorización.
    No se permite el uso de bibliotecas no estándar de Python.
    No se permite el uso de variables globales (sí el de constantes!).
    No se permite el uso de las instrucciones eval, exec.
    No se permite el uso de funcion(*argumentos).

Entrega

    Se deberá entregar únicamente el o los archivos .py desarrollados.
    No subir los archivos CSV utilizados.
    Realizar la entrega mediante el formulario de entregas bajo la sección TP2.

Material

Archivos CSV con 3.000 frases y 18.000 definiciones de palabras: archivos.zip

Observación al respecto de frases.csv: Como se mencionó en la especificación, la frase propiamente dicha se encuentra en la primera columna delimitada por comillas. Si bien no es obligatorio (ni necesario) utilizar el módulo csv de Python, en caso de usarlo tomar en cuenta que hay que decirle al reader que no interprete a las comillas como cualificador, además de que el delimitador es el carácter pipe (|). Esto se puede seleccionar al crear el reader con la siguiente sintaxis:

csv.reader(archivo, delimiter='|', quoting=csv.QUOTE_NONE)


