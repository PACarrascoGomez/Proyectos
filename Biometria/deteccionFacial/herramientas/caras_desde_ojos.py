import sys, os
import cv2
import numpy as np
import cPickle as pickle

# Corpus: BioID-FaceDatabase-V1.2

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Entorno: python2.7
# Descripcion: Obtener caras a partir de posicion de ojos
###########################################################

# Parametros
if len(sys.argv) != 3:
	print "Uso: python2 caras_desde_ojos.py <corpus_BioID-FaceDatabase-V1.2> <f_salida>"
	sys.exit(1)

# Lista de imagenes de caras
lista_img = os.popen("ls " + sys.argv[1] + "*.pgm").read().split("\n")
lista_img = lista_img[0:len(lista_img)-1]

lista_crops = []
# Crop de imagenes segun la posicion de los ojos
for r_img in lista_img:
	img = cv2.imread(r_img,0) # Escala de grises
	# Obtenemos las posiciones de los ojos de la imagen
	n_f = r_img.split(".pgm")[0]+".eye"
	f = open(n_f,"r")
	texto = f.read()
	f.close()
	lineas = texto.split("\n")
	posiciones = lineas[1].split("\t") # LX,LY,RX,RY
	for p in range(0,len(posiciones)):
		posiciones[p] = int(posiciones[p])
	distancia_ojos = posiciones[0]-posiciones[2]
	r_o = posiciones[1]-20
	r_d = posiciones[1]+distancia_ojos+20
	c_o = posiciones[2]-20
	c_d = posiciones[2]+distancia_ojos+20
	# Comprobamos margenes de la imagen (hay imagenes mal posicionadas en el corpus ej: BioID_0146)
	rows,cols = img.shape
	if r_o > 0 and r_d < rows and c_o > 0 and c_d < cols:
		crop = img[r_o:r_d,c_o:c_d]
		size = 24
		crop = cv2.resize(crop, (size, size)) # Resize 24x24
		x = np.mean(crop)
		o = np.std(crop)
		aux_crop = np.zeros((len(crop),len(crop[0])),dtype=float)
		for i in range(0,len(aux_crop)):
			for j in range(0,len(aux_crop[0])):
				aux_crop[i][j] = (crop[i][j]-x)/o
		crop = np.reshape(aux_crop,(1,size*size))
		crop = crop.tolist()[0]
		lista_crops.append(crop)
		
# Almacenamos la lista
f = file(sys.argv[2],"wb")
pickle.dump(lista_crops,f,2)
f.close()