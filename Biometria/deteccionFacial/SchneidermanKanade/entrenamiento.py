import sys, os
import numpy as np
import cv2
from sklearn.decomposition import IncrementalPCA
from sklearn.cluster import MiniBatchKMeans
import cPickle as pickle

############################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion: Deteccion facial
#	Algoritmo Schneiderman and Kanade
# Nota: El programa requiere:
#	apt-get install python-pip
#	pip install -U scikit-learn
#	pip install -U scipy
#	apt-get install python-opencv
############################################

#-------------------------------------------
# Parametros
#-------------------------------------------
if len(sys.argv) != 3:
	print("Uso: python2.7 entrenamiento.py <f_caras> <f_no_caras>")
	sys.exit(1)


print "################################################"
print "Algoritmo Schneiderman and Kanade"
print "################################################"
print "Cargando datos..."

# Cargamos las imagenes correspondientes a caras y no caras
f = file(sys.argv[1],"rb")
l_imagenes_caras = pickle.load(f)
f.close()
f = file(sys.argv[2],"rb")
l_imagenes_no_caras = pickle.load(f)
f.close()

# Size de dev (20%) y de test (20%)
s_dev = len(l_imagenes_caras)*10/100
s_test = len(l_imagenes_caras)*10/100

# Obtenemos una parte del dev del train (sin eliminarlo del train)
dev_caras = l_imagenes_caras[len(l_imagenes_caras)-s_dev:len(l_imagenes_caras)]
dev_no_caras = l_imagenes_no_caras[len(l_imagenes_no_caras)-s_dev:len(l_imagenes_no_caras)]
datos_dev = []
for i in range(0,len(dev_caras)):
	datos_dev.append((dev_caras[i],1))
	datos_dev.append((dev_no_caras[i],0))

# Almacenamos el dev para obtener lambda
f = file("datos_dev.dat","wb")
pickle.dump(datos_dev,f,2)
f.close()

# Separamos el train del test
test_caras = l_imagenes_caras[0:s_test]
l_imagenes_caras = l_imagenes_caras[s_test:len(l_imagenes_caras)]
test_no_caras = l_imagenes_no_caras[0:s_test]
l_imagenes_no_caras = l_imagenes_no_caras[s_test:len(l_imagenes_no_caras)]
datos_test = []
for i in range(0,len(test_caras)):
	datos_test.append((test_caras[i],1))
	datos_test.append((test_no_caras[i],0))

# Almacenamos el test para obtener lambda
f = file("datos_test.dat","wb")
pickle.dump(datos_test,f,2)
f.close()

print "Proyeccion PCA y Clustering (K-means)..."
# Nota: Imagenes de entrada son cuadradas
# Ventana subregion (cuadrada)
l_sr = len(l_imagenes_caras[0])/16
# Clusters para k means
clusters = 60
# PCA
ipca = IncrementalPCA(n_components=8)
# k means
kmeans = MiniBatchKMeans(n_clusters=clusters,random_state=1)

# Listas auxiliares
l_aux = []
l_pos = []
# Obtenemos el modelo de PCA (caras)
for img_cara in l_imagenes_caras:

	# Prepoceso PCA
	pos = 0
	for i in range(0,len(img_cara),l_sr):
		if i+l_sr <= len(img_cara):
			subregion = img_cara[i:i+l_sr]
			l_aux.append(subregion)
			l_pos.append(pos)
			pos += 1

	# Actualizamos la matriz de proyeccion
	if len(l_aux) >= 500:
		# Incremental PCA (Principal component analysis)
		X = np.array(l_aux)
		ipca.partial_fit(X)
		# Inicializamos
		l_aux = []

# Actualizamos datos restantes (PCA)
if len(l_aux) != 0:
	# Incremental PCA (Principal component analysis)
	X = np.array(l_aux)
	ipca.partial_fit(X)

# Inicializamos
l_aux = []
# Actualizamos el modelo de PCA (no caras)
for img_no_cara in l_imagenes_no_caras:

	# Prepoceso PCA
	for i in range(0,len(img_no_cara),l_sr):
		if i+l_sr <= len(img_no_cara):
			subregion = img_no_cara[i:i+l_sr]
			l_aux.append(subregion)

	# Actualizamos la matriz de proyeccion
	if len(l_aux) >= 500:
		# Incremental PCA (Principal component analysis)
		X = np.array(l_aux)
		ipca.partial_fit(X)
		# Inicializamos
		l_aux = []

# Actualizamos datos restantes (PCA)
if len(l_aux) != 0:
	# Incremental PCA (Principal component analysis)
	X = np.array(l_aux)
	ipca.partial_fit(X)

# Almacenamos el objeto ipca en un fichero .dat para deteccion
fichero = file("pca.dat", "w")  
pickle.dump(ipca, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  

# Reducimos la dimensionalidad (CARAS)
n_X_caras = []
for img_cara in l_imagenes_caras:

	pos = 0
	for i in range(0,len(img_cara),l_sr):
		if i+l_sr <= len(img_cara):
			subregion = img_cara[i:i+l_sr]
			X = np.array([subregion])
			n_X_caras.append(ipca.transform(X)[0])

# Clustering K means
kmeans.partial_fit(n_X_caras)

# Reducimos la dimensionalidad (NO_CARAS)
n_X_no_caras = []
for img_no_cara in l_imagenes_no_caras:

	pos = 0
	for i in range(0,len(img_no_cara),l_sr):
		if i+l_sr <= len(img_no_cara):
			subregion = img_no_cara[i:i+l_sr]
			X = np.array([subregion])
			n_X_no_caras.append(ipca.transform(X)[0])

# Clustering K means
kmeans.partial_fit(n_X_no_caras)

# Almacenamos el objeto kmeans en un fichero .dat para testing
fichero = file("kmeans.dat", "w")  
pickle.dump(kmeans, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  

############################################################

print "---------------------------------------"
print "EDAs --> CARAS"
print "---------------------------------------"
# Cuantificacion mediante k-means
labels = kmeans.predict(n_X_caras)

# Vector q de caras
q = [0]*clusters

print "- Obteniendo el vector q_i..."
# Actualizamos el vector q
for i in range(0,len(labels)):
	q[labels[i]] += 1

print "- Normalizando el vector q_i..."
# Normalizamos (para trabajar con probabilidades)
suma = sum(q)
for i in range(0,len(q)):
	q[i] = q[i]/float(suma)

# Almacenamos el objeto q en un fichero .dat para testing
fichero = file("q_caras.dat", "w")  
pickle.dump(q, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  

# Matriz pos/q de caras
m_pos_q = []
for i in range(0,16):
	m_pos_q.append([0]*clusters)

print "- Obteniendo la matriz pos_i/q_i..."
# Actualizamos la matriz pos_i/qi
for i in range(0,len(labels)):
	pos = l_pos[i]
	q = labels[i]
	m_pos_q[pos][q] += 1

print "- Normalizando la matriz pos_i/q_i..."
# Suavizamos y normalizamos la matriz
for r in range(0,len(m_pos_q)):
	for c in range(0,len(m_pos_q[0])):
		m_pos_q[r][c] += 0.001
v_suma = []
for r in range(0,len(m_pos_q)):
	v_suma.append(sum(m_pos_q[r]))
for r in range(0,len(m_pos_q)):
	for c in range(0,len(m_pos_q[0])):
		m_pos_q[r][c] = m_pos_q[r][c]/float(v_suma[r])

# Almacenamos el objeto m_pos_q en un fichero .dat para testing
fichero = file("m_pos_q_caras.dat", "w")  
pickle.dump(m_pos_q, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  

############################################################

print "---------------------------------------"
print "EDAs --> NO CARAS"
print "---------------------------------------"
# Cuantificacion mediante k-means
labels = kmeans.predict(n_X_no_caras)

# Vector q de no caras
q = [0]*clusters

print "- Obteniendo el vector q_i..."
# Actualizamos el vector q
for i in range(0,len(labels)):
	q[labels[i]] += 1

print "- Normalizando el vector q_i..."
# Normalizamos (para trabajar con probabilidades)
suma = sum(q)
for i in range(0,clusters):
	q[i] = q[i]/float(suma)

# Almacenamos el objeto q en un fichero .dat para testing
fichero = file("q_no_caras.dat", "w")  
pickle.dump(q, fichero, 2) # 2 = Almacenamiento binario
fichero.close()  

