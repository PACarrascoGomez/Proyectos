import sys
import cv2
import numpy as np

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Otsu
# Tecnica: Binarizacion (Global)
# Asignatura: Reconocimiento de escritura
##############################################

# Ej: python3 Otsu.py prueba.jpg

# Parametros de ejecucion
if len(sys.argv) != 2:
	print ("Uso: python3 Otsu.py <image>")
	exit()

# Cargamos la imagen en escala de grises
img = cv2.imread(sys.argv[1],0)
rows,cols = img.shape


# Obtenemos histograma de la imagen a nivel de escala de gris
h = np.zeros((1,256),dtype=int)
for r in range(0,rows):
	for c in range(0,cols):
		h[0][img[r][c]] += 1

# Normalizamos el histograma (Para trabajar con Probabilidades)
h_norm = np.zeros((1,256),dtype=float)
N = np.sum(h)
for c in range(0,256):
	h_norm[0][c] = h[0][c]/N

# Obtenemos el valor de thr (umbral)
thr_max = float("-Inf")
v_thr = -1
for k in range(0,256):
	w0 = 0.0
	w1 = 0.0
	for i in range(0,k):
		w0 += float(h_norm[0][i])
	for i in range(k,256):
		w1 += float(h_norm[0][i])
	u0 = 0.0
	u1 = 0.0
	if w0 > 0.0:
		for i in range(0,k):
			u0 += i*float(h_norm[0][i])
		u0 = u0/w0
	if w1 > 0.0:
		for i in range(k,256):
			u1 += i*float(h_norm[0][i])
		u1 = u1/w1
	aux = u0 - u1
	o2b = w0*w1*(aux*aux)
	if o2b > thr_max:
		thr_max = o2b
		v_thr = k
thr = v_thr

# Imagen binarizada
img_out = np.zeros((rows,cols),dtype=int)

# Binarizacion
for r in range(0,rows):
	for c in range(0,cols):
		if img[r][c] >= thr:
			img_out[r][c] = 255
		else:
			img_out[r][c] = 0

# Almacenamos la imagen binarizada
cv2.imwrite("binarizacion_Otsu.jpg",img_out)

img_out = np.reshape(img_out,(1,rows*cols))
print (set(img_out[0].tolist()))