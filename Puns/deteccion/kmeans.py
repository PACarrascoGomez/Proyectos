import sys
from sklearn.cluster import KMeans
from utils import *
import numpy as np

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Deteccion de puns (tarea 7.1 Semeval)
# Metodo: Clustering (kmeans) como detector
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Parametros
if len(sys.argv) != 3:
	print ("Uso: python3 kmeans.py <fichero_data> <fichero_out>")
	sys.exit(1)

# Parametros
f_data = sys.argv[1]
f_out = sys.argv[2]

# Cargamos las frases del corpus
frases = cargar_frases_txt(f_data)

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
					distancias_pares.append(d_min)
	if len(distancias_pares) > 0:
		distancias_frases[k] = distancias_pares

# Obtenemos la diferencia entre los dos pares con menor distancia
diferencias = []
keys_d = []
for k in distancias_frases:
	distancias_pares = distancias_frases[k]
	if len(distancias_pares) > 1:
		aux = sorted(distancias_pares)
		d12 = aux[1]-aux[0]
		diferencias.append([d12])
		keys_d.append(k)

# Clustering kmeans
X = np.array(diferencias)
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)

# El centroide mas grande --> pun
centroides = kmeans.cluster_centers_.tolist()
print (centroides)
label_centroide_max = centroides.index(max(centroides))
print (label_centroide_max)

# Obtenemos las etiquetas de los datos que ha proporcionado el clustering
labels = kmeans.labels_

# Almacenamos los resultados en un fichero de salida
f = open(f_out,"w")
for i in range(0,len(keys_d)):
	label = labels[i]
	if label == label_centroide_max:
		label = 1
	else:
		label = 0
	k = keys_d[i]
	f.write(str(k) + "\t" + str(label) + "\n")
f.close()
