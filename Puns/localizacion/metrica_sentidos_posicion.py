import sys
from utils import *
import numpy as np

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Localizacion de puns (tarea 7.2 Semeval)
# Metodo: Metrica sentidos * ponderacion posicion
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 metrica_sentidos_posicion.py <f_xml> <f_gold>")
	sys.exit(1)

# Parametros
f_xml = sys.argv[1]
f_gold = sys.argv[2]

# Cargamos las frases del corpus
frases = cargar_frases(f_xml)

# Cargamos stopwords
stopwords = obtener_stopwords(frases)

# Separamos un 30% para dev y un 70% para test del corpus de la competicion
# Nota: Se barajan los datos
(frases_dev,frases_test) = particionar_corpus(frases)

# Tokenizamos las frases
#frases_tok = tokenizar_frases(frases,stopwords) # Analisis todo el corpus
frases_tok = tokenizar_frases(frases_dev,stopwords) # Analisis sobre dev

# Cargamos el modelo word2vec
f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/GoogleNews-vectors-negative300.bin'
#f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/wikipedia_w2v.bin'
w2v = cargar_modelo_w2v(f_w2v)

# Cargamos los puns
puns = cargar_puns_subtask2(f_xml,f_gold)

# Obtenemos la similitud entre pares de palabras de cada frase
distancia_frases = {}
for k in frases_tok:
	palabras = frases_tok[k]
	palabras_frase = []
	for p in frases[k].split(" "):
		palabras_frase.append(p.lower())
	distancia_pares = []
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if p1 != p2 and not(contiguas(p1,p2,frases[k])):
				d_min = metrica_sentidos(p1,p2,w2v)
				d_min = metrica_sentidos_posicion(p2,d_min,palabras_frase)
				if d_min != float("Inf"):
					distancia_pares.append((d_min,(p1,p2)))
	if len(distancia_pares) > 0:
		distancia_frases[k] = distancia_pares

# Estadisticas
par_1 = 0
pun_der = 0
analizadas = 0
for k in distancia_frases:
	distancia_pares = distancia_frases[k]
	distancia_pares_ord = sorted(distancia_pares) # Ordena segun el primer elemento de la tupla
	pun = "-"
	if k in puns:
		pun = puns[k]
		analizadas += 1
		if pun in distancia_pares_ord[0][1]:
			par_1 += 1
			if pun == distancia_pares_ord[0][1][1]:
				pun_der += 1
print ("El pun se encuentra en el primer par:",par_1)
print ("El pun se encuentra en el primer par y en la ultima posicion:",pun_der)
print ("Total frases analizadas:",analizadas)
print ("Total Frases tarea:",len(frases))

	

