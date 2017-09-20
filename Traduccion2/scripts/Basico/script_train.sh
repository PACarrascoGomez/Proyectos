#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Practica: 2
# Ejercicio: Basico
###################################################################

# Nota: Realizar los EXPORT para crear el entorno
export PATH=$PATH:/home/pascu/Moses/tools/moses/bin/
export PATH=$PATH:/home/pascu/Moses/tools/moses/scripts/training/
export PATH=$PATH:/home/pascu/Moses/tools/srilm-1.7.1/bin/i686-m64/
export SCRIPTS_ROOTDIR=/home/pascu/Moses/tools/moses/scripts/
export GIZA=/home/pascu/Moses/tools/giza-pp-master/GIZA++-v2/
export MOSES=/home/pascu/Moses/tools/moses

# Variables
corpus="Corpus"
train="training_train"
dev="training_dev"

############################################################
# 4. CORPUS TRAIN
############################################################
# Accedemos al directorio del corpus
cd $corpus/train
# Nota: Los corpus ya estan limpios y tokenizados -> limpiar_corpus.sh
# Separamos el corpus de train en dos partes (train+dev)
# 85% -> train; 15% -> dev
n_frases_train=$(cat training.clean.tok.en | wc -l)
n_frases_dev=$(echo "("$n_frases_train*"15)/100" | bc)
n_frases_train=$(echo $n_frases_train"-"$n_frases_dev | bc)
cat training.clean.tok.en | head -$n_frases_train > $train.en
cat training.clean.tok.es | head -$n_frases_train > $train.es
cat training.clean.tok.en | tail -$n_frases_dev > $dev.en
cat training.clean.tok.es | tail -$n_frases_dev > $dev.es

############################################################
# 5. ENTRENAMIENTO MODELOS DE LENGUAJE (PARA EL ESPANOL)
############################################################
# Creamos el directorio donde almacenamos los modelos de lenguaje
mkdir lm
# Obtenemos el modelo de lenguaje (LM)
ngram-count -order 5 -unk \
-kndiscount -text $train.es -lm lm/turista.lm
# Nos guardamos la ruta del modelo de lenguaje
export LM=$PWD/lm/turista.lm

############################################################
# 6. ENTRENAMIENTO MODELO DE TRADUCCIÓN
############################################################
# Construimos la tabla de segmentos
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work \
-corpus $train -f en -e es -alignment grow-diag-final-and \
-lm 0:5:$LM -external-bin-dir $GIZA -hierarchical -glue-grammar -max-phrase-length 5

############################################################
# 7. ENTRENAMIENTO DE LOS PESOS DEL MODELO LOG_LINEAL
############################################################
# Obtenemos los pesos del modelo log-lineal mediante MERT
cd ..
$MOSES/scripts/training/mert-moses.pl \
train/$dev.en train/$dev.es \
$MOSES/bin/moses train/work/model/moses.ini \
--maximum-iterations=5 \
--mertdir $MOSES/bin/ \
--decoder-flags "-feature-name-overwrite \"SRILM KENLM\""
# Corregimos un error que provoca que MOSES tenga un fallo
mv train/work/model/moses.ini train/work/model/moses.ini.old
sed 's/SRILM/KENLM/g' train/work/model/moses.ini.old > train/work/model/moses.ini