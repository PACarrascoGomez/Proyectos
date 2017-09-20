import sys
import cv2
import numpy as np

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Bernsen
# Tecnica: Binarizacion (Local)
# Asignatura: Reconocimiento de escritura
##############################################

# Ej: python3 Niblack.py prueba.jpg 3 -0.2

# Parametros de ejecucion
if len(sys.argv) != 4:
	print ("Uso: python3 Bernsen.py <image> <size_window> <L>")
	exit()

# Metodo de binarizacion propuesto por Otsu
def binarizacion_otsu(img):
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
	return thr

# Cargamos la imagen en escala de grises
img = cv2.imread(sys.argv[1],0)
rows,cols = img.shape

# Ventana de analisis
size_w = int(sys.argv[2])

# Parametro
L = float(sys.argv[3])

# Imagen binarizada
img_out = np.zeros((rows,cols),dtype=int)

# thr Otsu
thr_otsu = binarizacion_otsu(img)

# Binarizacion
i = int(size_w/2)
for r in range(i,rows-i):
	for c in range(i,cols-i):
		crop_img = img[r-i:r+i,c-i:c+i]
		Imax = float(np.max(crop_img))
		Imin = float(np.min(crop_img))
		thr = -1
		if Imax - Imin >= L:
			thr = (Imax+Imin)/2
		else:
			thr = thr_otsu
		if img[r][c] >= thr:
			img_out[r][c] = 255
		else:
			img_out[r][c] = 0

# Almacenamos la imagen binarizada
cv2.imwrite("binarizacion_Bernsen.jpg",img_out)
