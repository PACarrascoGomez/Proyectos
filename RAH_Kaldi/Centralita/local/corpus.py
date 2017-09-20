# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: genera la lista de frases del corpus entero
# Entorno: python2.7
###########################################################

f_corpus = open("../data/local/corpus.txt","w")

#---------------------------------------------------------
# TRAIN
#---------------------------------------------------------
comando = "cat ../transcripciones/train/*"
transcripciones = os.popen(comando).read().split("\n")
transcripciones = transcripciones[0:len(transcripciones)-1]
for t in transcripciones:
	l_palabras_transcripcion = t.split("\n")[0].split(" ")
	l_palabras_transcripcion = l_palabras_transcripcion[1:len(l_palabras_transcripcion)-1]
	transcripcion = ""
	for palabra in l_palabras_transcripcion:
		transcripcion += palabra + " "
	f_corpus.write(transcripcion + "\n")

#---------------------------------------------------------
# TEST
#---------------------------------------------------------
comando = "cat ../transcripciones/test/*"
transcripciones = os.popen(comando).read().split("\n")
transcripciones = transcripciones[0:len(transcripciones)-1]
for t in transcripciones:
	l_palabras_transcripcion = t.split("\n")[0].split(" ")
	l_palabras_transcripcion = l_palabras_transcripcion[1:len(l_palabras_transcripcion)-1]
	transcripcion = ""
	for palabra in l_palabras_transcripcion:
		transcripcion += palabra + " "
	f_corpus.write(transcripcion + "\n")

f_corpus.close()