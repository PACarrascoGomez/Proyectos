import sys
import cv2
import numpy as np

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Sauvola
# Tecnica: Binarizacion (Local)
# Asignatura: Reconocimiento de escritura
##############################################

# Ej: python3 Sauvola.py prueba.jpg 3 0.05 128

# Parametros de ejecucion
if len(sys.argv) != 5:
	print ("Uso: python3 Niblack.py <image> <size_window> <k> <R>")
	exit()

# Cargamos la imagen en escala de grises
img = cv2.imread(sys.argv[1],0)
rows,cols = img.shape

# Ventana de analisis
size_w = int(sys.argv[2])

# Parametros
k = float(sys.argv[3])
R = float(sys.argv[4])

# Imagen binarizada
img_out = np.zeros((rows,cols),dtype=int)

# Binarizacion
i = int(size_w/2)
for r in range(i,rows-i):
	for c in range(i,cols-i):
		crop_img = img[r-i:r+i,c-i:c+i]
		u = np.mean(crop_img)
		o = np.std(crop_img)
		thr = u*(1+(k*(1-(o/R))))
		if img[r][c] >= thr:
			img_out[r][c] = 0
		else:
			img_out[r][c] = 255

# Almacenamos la imagen binarizada
cv2.imwrite("binarizacion_sauvola.jpg",img_out)
