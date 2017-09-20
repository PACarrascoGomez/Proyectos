# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: lista de ids con su locutor
# Entorno: python2.7
###########################################################

#---------------------------------------------------------
# TRAIN
#---------------------------------------------------------
comando = "ls ../data/train/*.wav | sort -u"
lista_ids = os.popen(comando).read().split("\n")
lista_ids = lista_ids[0:len(lista_ids)-1]
f_train = open("../data/train/utt2spk","w")
for i in range(0,len(lista_ids)):
	aux_id = lista_ids[i].split(".wav")[0].split("/")
	id_actual = aux_id[len(aux_id)-1]
	f_train.write(id_actual + " FER \n")
f_train.close()

#---------------------------------------------------------
# TEST
#---------------------------------------------------------
comando = "ls ../data/test/*.wav | sort -u"
lista_ids = os.popen(comando).read().split("\n")
lista_ids = lista_ids[0:len(lista_ids)-1]
f_test = open("../data/test/utt2spk","w")
for i in range(0,len(lista_ids)):
	aux_id = lista_ids[i].split(".wav")[0].split("/")
	id_actual = aux_id[len(aux_id)-1]
	f_test.write(id_actual + " FER \n")
f_test.close()