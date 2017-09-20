
############################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Transforma un texto en conjuntos de 3gramas
# Lenguaje: Python2.7
############################################################

# Nota: Debemos limpiar los corpus antes de ejecutar el programa
# Nota: Debemos separar el corpus de train en TRAIN+DEV
# Nota: Para limpiar y tokenizar usar limpiar_corpus.sh

# Corpus de entrada 
#corpus = "Corpus/train/training.clean.tok.en"
#corpus = "Corpus/train/training.clean.tok.es"
#corpus = "Corpus/test/test.clean.tok.en"
corpus = "Corpus/test/test.clean.tok.es"

# Fichero de salida
#salida = "train_3gramas.en"
#salida = "train_3gramas.es"
#salida = "test_3gramas.en"
salida = "test_3gramas.es"

# Abrimos el fichero de lectura
fichero = open(corpus,"r")

# Abrimos el fichero de escritura
fichero_salida = open(salida,"w")

# Convertimos las frases en Ngramas
for frase in fichero:
	palabras = frase.split("\n")[0].split(" ")
	aux = ""
	if len(palabras) == 1: # Si la frase se compone de una palabra hacemos un bigrama
		aux = "#_" + palabras[0] + "\n"
	else: # Si la frase tiene mas de 1 palabra hacemos trigramas
		for i in range(0,len(palabras)-1):
			if i == len(palabras)-2:
				if i == 0:
					aux += "#_" + palabras[i] + "_" + palabras[i+1] + "\n"
				else:
					aux += palabras[i-1] + "_" + palabras[i] + "_" + palabras[i+1] + "\n"
			elif i == 0:
				aux += "#_" + palabras[i] + "_" + palabras[i+1] + " "
			else:
				aux += palabras[i-1] + "_" + palabras[i] + "_" + palabras[i+1] + " "
	fichero_salida.write(aux)

# Cerramos los ficheros
fichero.close()
fichero_salida.close()