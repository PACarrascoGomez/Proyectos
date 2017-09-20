#!/bin/bash

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Preparamos los datos para la Centralita
###########################################################

# Creamos los directorios para los ficheros de train y test
mkdir -p data/train data/test

# Separamos y estructuramos los wavs de train y test
cp wav/test* data/test/
cp wav/train* data/train/

# Generamos los txt para cada wav de train y de test
python2.7 local/txt_corpus.py

# Creamos el directorio local dentro de data
mkdir data/local

# Generamos los datos acusticos del corpus
cd local
python2.7 wav.scp.py
python2.7 text.py
python2.7 utt2spk.py
python2.7 corpus.py 
cd ..

# Generamos el fichero spk2gender
echo "FER m" > data/train/spk2gender
echo "FER m" > data/test/spk2gender

# Juntamos todos los datos
if [ -d Centralita ]; then
	rm -R Centralita
fi
mkdir Centralita
cp data/train/*.wav Centralita/
cp data/train/*.txt Centralita/
cp data/test/*.wav Centralita/
cp data/test/*.txt Centralita/