#!/bin/bash

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Preparamos el lenguaje para la Centralita
###########################################################

# Creamos el directorio donde vamos a trabajar
if [ -d data/local/dict ]; then
	rm -R data/local/dict
fi
mkdir data/local/dict

# Ejecutamos los scripts python necesarios
cd local
python2.7 lexicon.py
python2.7 nonsilence_phones.py
echo "sil
spn" > ../data/local/dict/silence_phones.txt
echo "sil" > ../data/local/dict/optional_silence.txt
