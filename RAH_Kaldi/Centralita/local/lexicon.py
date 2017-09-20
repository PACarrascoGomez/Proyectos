# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: generar el lexicon del lenguaje
# Entorno: python2.7
###########################################################

dic_palabra_fonema = {}

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
		palabra = aux_lista[0]
		fonemas = aux_lista[1]
		dic_palabra_fonema[palabra] = fonemas
		
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
		palabra = aux_lista[0]
		fonemas = aux_lista[1]
		dic_palabra_fonema[palabra] = fonemas

# Escribimos el lexicon en el fichero
f_lexicon = open("../data/local/dict/lexicon.txt","w")
f_lexicon.write("!SIL sil\n<UNK> spn\n")
for palabra in dic_palabra_fonema:
	f_lexicon.write(palabra + " " + dic_palabra_fonema[palabra] + "\n")
f_lexicon.close()