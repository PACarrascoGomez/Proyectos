# -*- coding: utf-8 -*-

import os

################################################################
# Autor: Pascual Andres Carrasco Gomez
# Obtiene los txt del directorio especificado
# Entorno: python2.7
################################################################

# Formato de las transcripciones:
#	id_wav transcripcion_wav

#---------------------------------------------------------------
# TRAIN
#---------------------------------------------------------------
ruta = "transcripciones/train/"

# Recorremos todos los ficheros de train
for f in os.listdir(ruta):
	f_i = open(ruta + f,"r")
	for line in f_i:
		palabras = line.split("\n")[0].split(" ")
		id_wav = palabras[0]
		if len(id_wav) == 1:
			id_wav = "00" + id_wav
		elif len(id_wav) == 2:
			 id_wav = "0" + id_wav
		palabras = palabras[1:len(palabras)-1]
		f_aux_palabras = []
		for p in palabras:
			# Obtenemos la fonetica de cada palabra
			comando = "echo " + p + " | local/Syllables.perl -sp -sil -longsil +SIMPLE -t +c"
			trans_p = os.popen(comando).read().split("\n")[0]
			f_aux_palabras.append(trans_p)
		# Concatenamos cada palabra con su transcripcion fonetica
		f_o = open("data/train/training" + id_wav + ".txt","w")
		for i in range(0,len(palabras)):
			f_o.write(palabras[i] + "\t" + f_aux_palabras[i] + "\n")
		f_o.close()


#---------------------------------------------------------------
# TEST
#---------------------------------------------------------------
ruta = "transcripciones/test/"

# Recorremos todos los ficheros de train
for f in os.listdir(ruta):
	f_i = open(ruta + f,"r")
	for line in f_i:
		palabras = line.split("\n")[0].split(" ")
		id_wav = palabras[0]
		if len(id_wav) == 1:
			id_wav = "00" + id_wav
		elif len(id_wav) == 2:
			 id_wav = "0" + id_wav
		palabras = palabras[1:len(palabras)-1]
		f_aux_palabras = []
		for p in palabras:
			# Obtenemos la fonetica de cada palabra
			comando = "echo " + p + " | local/Syllables.perl -sp -sil -longsil +SIMPLE -t +c"
			trans_p = os.popen(comando).read().split("\n")[0]
			f_aux_palabras.append(trans_p)
		# Concatenamos cada palabra con su transcripcion fonetica
		f_o = open("data/test/test" + id_wav + ".txt","w")
		for i in range(0,len(palabras)):
			f_o.write(palabras[i] + "\t" + f_aux_palabras[i] + "\n")
		f_o.close()




