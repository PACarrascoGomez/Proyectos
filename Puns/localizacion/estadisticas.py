import sys
from utils import *
import numpy as np
import random

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Localizacion de puns (tarea 7.2 Semeval)
# Metodo: Estadisticas para la tarea de localizacion
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 estadisticas.py <f_xml> <f_gold>")
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

print ("---------------------------------------------------------------")
print ("d_coseno:")
print ("---------------------------------------------------------------")

# Obtenemos el distancias entre pares de palabras de cada frase
distancias_frases = {}
for k in frases_tok:
	distancias_pares = []
	palabras = frases_tok[k]
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			d_cos = distancia_coseno(p1,p2,w2v)
			if d_cos != None:
				distancias_pares.append((d_cos,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)

print ("---------------------------------------------------------------")
print ("d_coseno + no contiguas")
print ("---------------------------------------------------------------")

# Obtenemos el distancias entre pares de palabras de cada frase
distancias_frases = {}
for k in frases_tok:
	distancias_pares = []
	palabras = frases_tok[k]
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if not(contiguas(p1,p2,frases[k])):
				d_cos = distancia_coseno(p1,p2,w2v)
				if d_cos != None:
					distancias_pares.append((d_cos,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)

print ("---------------------------------------------------------------")
print ("d_coseno + no contiguas + p1 != p2")
print ("---------------------------------------------------------------")

# Obtenemos el distancias entre pares de palabras de cada frase
distancias_frases = {}
for k in frases_tok:
	distancias_pares = []
	palabras = frases_tok[k]
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if p1 != p2 and not(contiguas(p1,p2,frases[k])):
				d_cos = distancia_coseno(p1,p2,w2v)
				if d_cos != None:
					distancias_pares.append((d_cos,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)

print ("---------------------------------------------------------------")
print ("Metrica embeddings sentidos")
print ("---------------------------------------------------------------")

distancias_frases = {}
for k in frases_tok:
	palabras = frases_tok[k]
	distancias_pares = []
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			d_min = metrica_sentidos(p1,p2,w2v)
			if d_min != float("Inf"):
				distancias_pares.append((d_min,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)

print ("---------------------------------------------------------------")
print ("Metrica embeddings sentidos + palabras no contiguas")
print ("---------------------------------------------------------------")

distancias_frases = {}
for k in frases_tok:
	palabras = frases_tok[k]
	distancias_pares = []
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if not(contiguas(p1,p2,frases[k])):
				d_min = metrica_sentidos(p1,p2,w2v)
				if d_min != float("Inf"):
					distancias_pares.append((d_min,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)

print ("---------------------------------------------------------------")
print ("Metrica embeddings sentidos + palabras no contiguas + p1 != p2")
print ("---------------------------------------------------------------")

distancias_frases = {}
for k in frases_tok:
	palabras = frases_tok[k]
	distancias_pares = []
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if p1 != p2 and not(contiguas(p1,p2,frases[k])):
				d_min = metrica_sentidos(p1,p2,w2v)
				if d_min != float("Inf"):
					distancias_pares.append((d_min,(p1,p2)))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos el numero de frases eliminadas a causa de los embeddings
print ("Frases analizadas:",len(distancias_frases),"de",len(frases))

# Obtenemos cuantas veces el pun se encuentra entre el primer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1]:
			pun_in += 1
print ("El pun se encuentra en el par con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el segundo par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 1:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los dos pares con menor distancia:",pun_in,"de",j)

# Obtenemos cuantas veces el pun se encuentra entre el primer par o el tercer par de palabras ordenado
pun_in = 0
j = 0
for k in distancias_frases:
	if k in puns and len(distancias_frases[k]) > 2:
		pun = puns[k]
		j += 1
		l_aux = distancias_frases[k][:]
		l_aux.sort(key=lambda distancia: distancia[0])
		if pun in l_aux[0][1] or pun in l_aux[1][1] or pun in l_aux[2][1]:
			pun_in += 1
print ("El pun se encuentra en uno de los tres pares con menor distancia:",pun_in,"de",j)
