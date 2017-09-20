import numpy as np
import cv2
import sys
import cPickle as pickle

# Ejemplo de ejecucion: python2 rotar_caras_corpus.py DETECCION/dfFaces_24x24_norm

# Comprobamos parametros
if len(sys.argv) != 3:
	print "Uso: python2.7 operaciones_caras.py <f_caras> <f_salida>"
	sys.exit(1)

def rotar_imagen(img, angle):
	centro = tuple(np.array(img.shape)/2)
	rot_mat = cv2.getRotationMatrix2D(centro,angle,1.0)
	result = cv2.warpAffine(img,rot_mat,img.shape,flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_TRANSPARENT)
	return result

grados = [5,8,-5,-8]

# Cargamos las caras a las cuales les aplicamos las operaciones
f = file(sys.argv[1],"rb")
l_imagenes_caras = pickle.load(f)
f.close()
l_imagenes_caras = l_imagenes_caras.tolist()

# Estructura de datos para almacenar las imagenes
lista_img = []

# Transformaciones sobre imagenes 
for img_cara in l_imagenes_caras:
	lista_img.append(img_cara)
	a = np.array(img_cara)
	img = np.reshape(a,(24,24))
	for g in grados:
		img_rot = rotar_imagen(img,g)
		img_crop = img_rot[2:len(img_rot)-2,2:len(img_rot[0])-2] # Eliminamos relleno negro que se anade al rotar la imagen
		img_rot = cv2.resize(img_crop,(24,24))
		#cv2.imshow('image',img_rot)
		#cv2.waitKey(0)
		img_aux = np.reshape(img_rot,(1,24*24))
		l_aux_img = img_aux.tolist()[0]
		lista_img.append(l_aux_img)
	img_flip = cv2.flip(img,1)
	#cv2.imshow('image',img_flip)
	#cv2.waitKey(0)
	img_aux = np.reshape(img_flip,(1,24*24))
	l_aux_img = img_aux.tolist()[0]
	lista_img.append(l_aux_img)
	for g in grados:
		img_rot = rotar_imagen(img_flip,g)
		img_crop = img_rot[2:len(img_rot)-2,2:len(img_rot[0])-2] # Eliminamos relleno negro que se anade al rotar la imagen
		img_rot = cv2.resize(img_crop,(24,24))
		#cv2.imshow('image',img_rot)
		#cv2.waitKey(0)
		img_aux = np.reshape(img_rot,(1,24*24))
		l_aux_img = img_aux.tolist()[0]
		lista_img.append(l_aux_img)

matriz = np.array(lista_img)

# Almacenamos las nuevas imagenes
f = file(sys.argv[2],"wb")
pickle.dump(matriz,f,2)
f.close()
