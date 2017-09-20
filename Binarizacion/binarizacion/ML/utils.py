import sys, os
import cv2
import numpy as np
from keras.utils.np_utils import to_categorical

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Fichero con funciones compartidas
# Asignatura: Reconocimiento de escritura
##############################################

# Metodo de binarizacion propuesto por Otsu
def binarization_otsu(img):
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

# Devuelve el numero de componentes que tiene cada muestra
def dimension_sample():
	return 3

# X: Vector de caractisticas de cada pixel de la imagen
def load_x(f_img_in,size_w):
	x = []
	img = cv2.imread(f_img_in, 0)
	rows,cols = img.shape
	u_g = np.mean(img)
	o_g = np.std(img)
	thr_otsu = binarization_otsu(img)
	inc = int((size_w)/2)
	dim = dimension_sample()
	for r in range(rows):
		for c in range(cols):
			img_crop = img[r-inc:r+inc,c-inc:c+inc]
			if np.sum(img_crop) == 0.0:
				aux_x = [0.0]*dim
			else:
				u_l = np.mean(img_crop)
				o_l = np.std(img_crop)
				du = thr_otsu-img[r][c]
				aux_x = [u_g-u_l,o_g-o_l,du]
			x.append(aux_x)
	x = np.array(x)
	return x

# Carga los datos de entrada para los modelos
# X: Vector de caractisticas de cada pixel de cada imagen
# Y: Clase (0,1) a la que pertenece cada pixel de cada imagen
def load_data(dir_x,dir_y,size_w):
	l_f_x = os.popen("ls " + dir_x).read().split("\n")[:-1]
	l_f_y = os.popen("ls " + dir_y).read().split("\n")[:-1]
	x_train = []
	y_train = []
	inc = int((size_w)/2)
	for n_f in l_f_x:
		img_original = cv2.imread(dir_x + n_f, 0)
		f_y = os.popen("ls " + dir_y + "*" + n_f.split(".")[0] + "*").read().split("\n")[0]
		img_mascara = cv2.imread(f_y, 0)
		rows,cols = img_original.shape
		u_g = np.mean(img_original)
		o_g = np.std(img_original)
		thr_otsu = binarization_otsu(img_original)
		for r in range(inc,rows-inc):
			for c in range(inc,cols-inc):
				img_crop = img_original[r-inc:r+inc,c-inc:c+inc]
				u_l = np.mean(img_crop)
				o_l = np.std(img_crop)
				du = thr_otsu-img_original[r][c]
				x = [u_g-u_l,o_g-o_l,du]
				x_train.append(x)
				# Al cargar la imagen en grises mediante opencv, 
				# varia valores entre 0 y 255 la propia libreria
				y = 0
				if img_mascara[r][c] > 150: y = 1
				y_train.append(y)
	x_train = np.array(x_train)
	y_train = np.array(y_train)
	return (x_train,y_train)

# Realiza la binarizacion de la imagen
def binarize_image(f_img_in,f_img_out,y):
	rows,cols = cv2.imread(f_img_in,0).shape
	img_out = []
	for i in range(0,len(y),cols):
		img_out.append(y[i:i+cols])
	for r in range(rows):
		for c in range(cols):
			if img_out[r][c] == 1:
				img_out[r][c] = 255
			else:
				img_out[r][c] = 0
	img_out = np.array(img_out)
	cv2.imwrite(f_img_out,img_out)

# Generador de datos (x,y)
def generator_data(dir_x,dir_y,size_w,size_b):
	while True:
		l_f_x = os.popen("ls " + dir_x).read().split("\n")[:-1]
		l_f_y = os.popen("ls " + dir_y).read().split("\n")[:-1]
		inc = int((size_w)/2)
		x_train = []
		y_train = []
		cont = 0
		for n_f in l_f_x:
			img_original = cv2.imread(dir_x + n_f, 0)
			f_y = os.popen("ls " + dir_y + "*" + n_f.split(".")[0] + "*").read().split("\n")[0]
			img_mascara = cv2.imread(f_y, 0)
			rows,cols = img_original.shape
			u_g = np.mean(img_original)
			o_g = np.std(img_original)
			thr_otsu = binarization_otsu(img_original)
			for r in range(inc,rows-inc):
				for c in range(inc,cols-inc):
					img_crop = img_original[r-inc:r+inc,c-inc:c+inc]
					u_l = np.mean(img_crop)
					o_l = np.std(img_crop)
					pixel = img_original[r][c]
					du = thr_otsu-pixel
					x = [u_g-u_l,o_g-o_l,du]
					x_train.append(x)
					# Al cargar la imagen en grises mediante opencv, 
					# varia valores entre 0 y 255 la propia libreria
					y = 0
					if img_mascara[r][c] > 150: y = 1
					y_train.append(y)
					cont += 1
					if cont == size_b:
						x_train = np.array(x_train)
						y_train = np.array(y_train)
						y_train = to_categorical(y_train)
						yield(x_train,y_train)
						x_train = []
						y_train = []
						cont = 0
		for i in range(cont,size_b):
			x = [0.0]*3
			y = 0
			x_train.append(x)
			y_train.append(y)
		x_train = np.array(x_train)
		y_train = np.array(y_train)
		y_train = to_categorical(y_train)
		yield(x_train,y_train)

# Devuelve el numero de muestras que obtenemos de los datos
def data_size(dir_x,size_w):
	l_f_x = os.popen("ls " + dir_x).read().split("\n")[:-1]
	inc = int((size_w)/2)
	res_size = 0
	for n_f in l_f_x:
		img = cv2.imread(dir_x+n_f,0)
		rows,cols = img.shape
		aux = rows*cols
		aux = aux-(2*inc*rows) # Pixeles de la ventana analisis (filas)
		aux = aux-(2*inc*cols) # Pixeles de la ventana analisis (columnas)
		res_size += aux
	return res_size
