#!/bin/bash

# Comprobacion de paramaetros
if [ $# -ne 1 ]; then
	echo "Uso: ./preparar_corpus_kftt.sh <dir_data_kftt>"
	exit
fi

# Directorio de datos kftt como parametro
data=$1

# ruta de ejecucion
ruta_actual=$(pwd)

# Eliminamos el Corpus si existe
if [ -d Corpus ]; then
	rm -R Corpus
fi

# Creamos la estructura Corpus
mkdir -p Corpus/train
mkdir Corpus/test
cd $data
cp kyoto-test.en $ruta_actual/Corpus/test/test.en
cp kyoto-test.ja $ruta_actual/Corpus/test/test.ja
# Unimos el train y el tune (para tener mas datos de train)
cp kyoto-train.cln.en $ruta_actual/Corpus/train/training.en
cat kyoto-tune.en >> $ruta_actual/Corpus/train/training.en
cp kyoto-train.cln.ja $ruta_actual/Corpus/train/training.ja
cat kyoto-tune.ja >> $ruta_actual/Corpus/train/training.ja
# dev
cp kyoto-dev.en $ruta_actual/Corpus/train/dev.en
cp kyoto-dev.ja $ruta_actual/Corpus/train/dev.ja