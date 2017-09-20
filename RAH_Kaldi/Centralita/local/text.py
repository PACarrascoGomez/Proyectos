# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: lista de ids con su transcripcion
# Entorno: python2.7
###########################################################

#---------------------------------------------------------
# TRAIN
#---------------------------------------------------------
comando = "ls ../data/train/*.wav | sort -u"
lista_ids = os.popen(comando).read().split("\n")
lista_ids = lista_ids[0:len(lista_ids)-1]
comando = "cat ../transcripciones/train/*"
lista_transcripciones = os.popen(comando).read().split("\n")
lista_transcripciones = lista_transcripciones[0:len(lista_transcripciones)-1]
f_train = open("../data/train/text","w")
for i in range(0,len(lista_ids)):
	aux_id = lista_ids[i].split(".wav")[0].split("/")
	id_actual = aux_id[len(aux_id)-1]
	aux_transcripcion = lista_transcripciones[i].split("\n")[0].split(" ")
	aux_transcripcion = aux_transcripcion[1:len(aux_transcripcion)]
	transcripcion_actual = ""
	for t in aux_transcripcion:
		transcripcion_actual += t + " "
	f_train.write(id_actual + " " + transcripcion_actual + "\n")
f_train.close()

#---------------------------------------------------------
# TEST
#---------------------------------------------------------
comando = "ls ../data/test/*.wav | sort -u"
lista_ids = os.popen(comando).read().split("\n")
lista_ids = lista_ids[0:len(lista_ids)-1]
comando = "cat ../transcripciones/test/*"
lista_transcripciones = os.popen(comando).read().split("\n")
lista_transcripciones = lista_transcripciones[0:len(lista_transcripciones)-1]
f_test = open("../data/test/text","w")
for i in range(0,len(lista_ids)):
	aux_id = lista_ids[i].split(".wav")[0].split("/")
	id_actual = aux_id[len(aux_id)-1]
	aux_transcripcion = lista_transcripciones[i].split("\n")[0].split(" ")
	aux_transcripcion = aux_transcripcion[1:len(aux_transcripcion)]
	transcripcion_actual = ""
	for t in aux_transcripcion:
		transcripcion_actual += t + " "
	f_test.write(id_actual + " " + transcripcion_actual + "\n")
f_test.close()