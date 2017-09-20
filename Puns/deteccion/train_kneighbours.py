import sys
from utils import *
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pickle

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Deteccion de puns (tarea 7.1 Semeval)
# Metodo: K vecinos mas cercanos
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Parametros
if len(sys.argv) != 3:
	print ("Uso: python3 train_kneighbours.py <fichero_data> <fichero_gold>")
	sys.exit(1)

# Parametros
f_data = sys.argv[1]
f_gold = sys.argv[2]

# Cargamos las frases del corpus
frases = cargar_frases_txt(f_data)

# Cargamos las salidas de las frases
frases_y = y_tarea_deteccion(f_gold)

# Cargamos stopwords
stopwords = obtener_stopwords(frases)

# Tokenizamos las frases
frases_tok = tokenizar_frases(frases,stopwords)

# Cargamos el modelo word2vec
f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/GoogleNews-vectors-negative300.bin'
#f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/wikipedia_w2v.bin'
model = cargar_modelo_w2v(f_w2v)

# Obtenemos la similitud entre pares de palabras de cada frase
distancias_frases = {}
for k in frases_tok:
	palabras = frases_tok[k]
	palabras_frase = []
	for p in frases[k].split(" "):
		palabras_frase.append(p.lower())
	distancias_pares = []
	for i in range(len(palabras)):
		for j in range(i+1,len(palabras)):
			p1 = palabras[i]
			p2 = palabras[j]
			if p1 != p2 and not(contiguas(p1,p2,frases[k])):
				d_min = metrica_sentidos(p1,p2,model)
				d_min = ponderar_distancia(p2,d_min,palabras_frase)
				if d_min != float("Inf"):
					pos_p1 = posicion_palabra_frase(p1,palabras_frase)
					pos_p2 = posicion_palabra_frase(p2,palabras_frase)
					distancias_pares.append((d_min,pos_p1,pos_p2))
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos la diferencia entre los dos pares con menor distancia
diferencias = []
y_train = []
for k in distancias_frases:
	distancias_pares = distancias_frases[k]
	aux = sorted(distancias_pares)
	c1 = aux[0][0]
	c2 = aux[0][2]
	c3 = aux[0][1]-aux[0][2]
	diferencias.append([c1,c2,c3])
	y = frases_y[k]
	y_train.append(y)

#------------------------------------------
# MODELO
#------------------------------------------
neigh = KNeighborsClassifier(n_neighbors=20)

#------------------------------------------
# ENTRENAMIENTO
#------------------------------------------
x_train = np.array(diferencias)
y_train = np.array(y_train)
neigh.fit(x_train,y_train)

#------------------------------------------
# Almacenamos el modelo obtenido
#------------------------------------------
f_out = open("model_kneighbours","wb")
pickle.dump(neigh,f_out)
f_out.close()