# -*- coding: utf-8 -*-

import os

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: lista de ids con wavs
# Entorno: python2.7
###########################################################

#---------------------------------------------------------
# TRAIN
#---------------------------------------------------------
ruta_wavs_train = os.popen("cd ../data/train/;pwd").read()
ruta_wavs_train = ruta_wavs_train.split("\n")[0]
comando = "ls ../data/train/*.wav | sort -u"
lista = os.popen(comando).read().split("\n")
lista = lista[0:len(lista)-1]
f_train = open("../data/train/wav.scp","w")
for l in lista:
	wav = l.split(".wav")[0].split("/")
	wav = wav[len(wav)-1]
	f_train.write(wav + " " + ruta_wavs_train + "/" + wav + ".wav" + "\n")
f_train.close()

#---------------------------------------------------------
# TEST
#---------------------------------------------------------
ruta_wavs_test = os.popen("cd ../data/test/;pwd").read()
ruta_wavs_test = ruta_wavs_test.split("\n")[0]
comando = "ls ../data/test/*.wav | sort -u"
lista = os.popen(comando).read().split("\n")
lista = lista[0:len(lista)-1]
f_test = open("../data/test/wav.scp","w")
for l in lista:
	wav = l.split(".wav")[0].split("/")
	wav = wav[len(wav)-1]
	f_test.write(wav + " " + ruta_wavs_test + "/" + wav + ".wav" + "\n")
f_test.close()