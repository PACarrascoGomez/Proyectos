import sys, os
import cv2
import numpy as np
from numpy import linalg as LA
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

######################################################
# Autor: Pascual Andres Carrasco Gomez
# Problema: eigenFaces
# Entorno: python2.7
######################################################

# Uso: python2 eigenfaces.py ORL/

# Parametros
if len(sys.argv) != 2:
	print "Uso: python2 eigenfaces.py <dir_ORL>"
	sys.exit(1)

#--------------------------------------------------------
# DATOS TRAIN Y TEST
#--------------------------------------------------------
l_dir = os.popen("ls " + sys.argv[1]).read().split("\n")
# Eliminamos el README y el espacio vacio del final de la lista
l_dir = l_dir[1:len(l_dir)-1]
# Obtenemos las filas y las columnas de las imagenes
img = cv2.imread(sys.argv[1] + l_dir[0] + "/1.pgm",0)
rows,cols = img.shape
# EDAs
m_train = None
m_test = None
y_ref = []

l_aux_train = []
l_aux_test = []
for d in l_dir:
	for i in range(1,6):
		img = cv2.imread(sys.argv[1] + d + "/" + str(i) + ".pgm",0)
		img_fila = np.reshape(img,(1,rows*cols))
		l_aux_train.append(img_fila.tolist()[0])
	for i in range(6,11):
		img = cv2.imread(sys.argv[1] + d + "/" + str(i) + ".pgm",0)
		img_fila = np.reshape(img,(1,rows*cols))
		l_aux_test.append(img_fila.tolist()[0])
	y_ref.append(d)
m_train = np.array(l_aux_train)
m_test = np.array(l_aux_test)

# Obtenemos el vector promedio (cara promedio)
n,d = m_train.shape
x = np.sum(m_train,axis=0,dtype=float)
v_p = x/n # vector promedio

# Obtenemos la matriz A
A_p = m_train - v_p
A = A_p.transpose()

# Obtenemos la matriz C'
C_p = np.dot(A_p,A)
C_p = C_p/d

# Obtenemos los eigenvectores (B') y eigenvalores (D') de C'
D_p,B_p = LA.eig(C_p)

# Obtenemos B y D
B = np.dot(A,B_p)
D = (d/n)*D_p

# Hacemos ortonormales los eigenvectores
modulo_B = LA.norm(B,axis=0) # Vectores columna
B = B/modulo_B
B_t = B.transpose()

# Ordenamos de mayor a menor eigenvalor
D_sort = np.copy(D)
D_sort[::-1].sort()

# Datos grafica
data_x = []
data_y = []
for d_p in range(1,n+1):

	# Obtenemos los d' primeros eigenvectores (de mayor a menor eigenvalor)
	l_aux = []
	for i in range(0,d_p):
		indice = np.where(D==D_sort[i])
		l_aux.append(B_t[indice][0])
	B_d = np.array(l_aux)

	# Proyeccion de la x (train)
	pca_train = np.dot(B_d,m_train.transpose())

	# Entrenamos el modelo (clasificador) de vecino mas cercano
	X = pca_train.transpose()
	y = []
	for i in range(0,len(y_ref)):
		for j in range(0,5):
			y.append(i)
	y = np.array(y)
	nbrs = KNeighborsClassifier(n_neighbors=1, metric='euclidean', algorithm='kd_tree').fit(X,y)

	# Realizamos la evaluacion
	pca_test = np.dot(B_d,m_test.transpose())
	Y = pca_test.transpose()
	res_class = nbrs.predict(Y)

	# Obtenemos el numero de errores obtenido
	n_errores = 0
	for i in range(0,len(y)):
		if y[i] != res_class[i]:
			n_errores += 1
	data_x.append(d_p)
	data_y.append(n_errores/float(len(y)))

# Mostramos la grafica
plt.xlabel('d')
plt.ylabel('error')
plt.title('Resultados eigenfaces')
plt.plot(data_x,data_y)
plt.show()










