# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: generar el lexicon del lenguaje
# Entorno: python2.7
###########################################################

lista_fonemas = []

#---------------------------------------------------------
# TRAIN
#---------------------------------------------------------
comando = "ls ../data/train/*.txt"
lista_txt = os.popen(comando).read()
lista_txt = lista_txt[0:len(lista_txt)-1].split("\n")

for f in lista_txt:
	comando = "cat " + f
	aux = os.popen(comando).read().split("\n")
	aux = aux[0:len(aux)-1]
	for par in aux:
		aux_lista = par.split("\t")
		fonemas = aux_lista[1].split(" ")
		fonemas = fonemas[0:len(fonemas)-1]
		for fo in fonemas:
			if fo not in lista_fonemas and fo != "":
				lista_fonemas.append(fo)
		
#---------------------------------------------------------
# TEST
#---------------------------------------------------------
comando = "ls ../data/test/*.txt"
lista_txt = os.popen(comando).read()
lista_txt = lista_txt[0:len(lista_txt)-1].split("\n")

for f in lista_txt:
	comando = "cat " + f
	aux = os.popen(comando).read().split("\n")
	aux = aux[0:len(aux)-1]
	for par in aux:
		aux_lista = par.split("\t")
		fonemas = aux_lista[1].split(" ")
		for fo in fonemas:
			if fo not in lista_fonemas and fo != "":
				lista_fonemas.append(fo)

# Escribimos el lexicon en el fichero
f_no_s = open("../data/local/dict/nonsilence_phones.txt","w")
for fo in lista_fonemas:
	f_no_s.write(fo + "\n")
	#print fo
f_no_s.close()