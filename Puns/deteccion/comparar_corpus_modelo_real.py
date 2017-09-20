import sys
from utils import *
import numpy as np
import pickle

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Deteccion de puns (tarea 7.1 Semeval)
# Metodo: Compara los corpus para ver si hay diferencias
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Parametros
if len(sys.argv) != 5:
	print ("Uso: python3 comparar_corpus_train_test.py <fichero_xml> <fichero_gold_xml> <fichero_txt> <fichero_gold_txt>")
	sys.exit(1)

# Parametros
f_xml = sys.argv[1]
f_gold_xml = sys.argv[2]
f_txt = sys.argv[3]
f_gold_txt = sys.argv[4]

# Cargamos las frases del corpus de test
frases_test = cargar_frases(f_xml)

# Cargamos las salidas de las frases de test
frases_y_test = y_tarea_deteccion(f_gold_xml)

# Cargamos las frases del corpus de train
frases_train = cargar_frases_txt(f_txt)

# Cargamos las salidas de las frases de train
frases_y_train = y_tarea_deteccion(f_gold_txt)

# Cargamos stopwords
stopwords = obtener_stopwords(frases_test)

# Tokenizamos las frases
frases_test_tok = tokenizar_frases(frases_test,stopwords)

# Cargamos stopwords
stopwords = obtener_stopwords(frases_train)

# Tokenizamos las frases
frases_train_tok = tokenizar_frases(frases_train,stopwords)

# Convertimos los diccionarios a listas
l_frases_test = []
for k in frases_test_tok:
	l_frases_test.append(frases_test_tok[k])

# Evitamos que hayan frases repetidas en el train
print (len(frases_train_tok))
dic_invertido = {}
for k in frases_train_tok:
	dic_invertido[" ".join(frases_train_tok[k])] = k
frases_train_tok = {}
for aux_frase_tok in dic_invertido:
	frases_train_tok[dic_invertido[aux_frase_tok]] = aux_frase_tok.split(" ")
print (len(frases_train_tok))

# Obtenemos la comparacion
# Separamos el corpus de frases al corpus de frases limpias (eliminando las que estan en el test)
f = open("frases_clean.txt","w")
iguales = 0
puns = 0
no_puns = 0
for k in frases_train_tok:
	if frases_train_tok[k] in l_frases_test:
		iguales += 1
	else:
		if frases_y_train[k] == 1:
			puns += 1
		else:
			no_puns += 1
		f.write(str(k) + "\t" + frases_train[k] + "\n")
f.close()

# Resultados
print ("Hay",iguales,"frases de",len(frases_train_tok))
print ("De las",len(frases_train_tok)-iguales,",",puns,"son puns y",no_puns,"son no puns.")



