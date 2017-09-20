import sys
import cv2
import numpy as np

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Niblack
# Tecnica: Binarizacion (Local)
# Asignatura: Reconocimiento de escritura
##############################################

# Ej: python3 Niblack.py prueba.jpg 3 -0.2

# Parametros de ejecucion
if len(sys.argv) != 4:
	print ("Uso: python3 Niblack.py <image> <size_window> <k>")
	exit()

# Cargamos la imagen en escala de grises
img = cv2.imread(sys.argv[1],0)
rows,cols = img.shape

# Ventana de analisis
size_w = int(sys.argv[2])

# Parametro
k = float(sys.argv[3])

# Imagen binarizada
img_out = np.zeros((rows,cols),dtype=int)

# Binarizacion
i = int(size_w/2)
for r in range(i,rows-i):
	for c in range(i,cols-i):
		crop_img = img[r-i:r+i,c-i:c+i]
		u = np.mean(crop_img)
		o = np.std(crop_img)
		thr = u+(k*o)
		if img[r][c] >= thr:
			img_out[r][c] = 255
		else:
			img_out[r][c] = 0

# Almacenamos la imagen binarizada
cv2.imwrite("binarizacion_niblack.jpg",img_out)
