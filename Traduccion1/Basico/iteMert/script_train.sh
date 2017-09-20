#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Trabajo: Basico -> experimentacion iteraciones MERT
###################################################################

# Nota: Realizar los EXPORT para crear el entorno
export PATH=$PATH:/home/pascu/Moses/tools/moses/bin/
export PATH=$PATH:/home/pascu/Moses/tools/moses/scripts/training/
export PATH=$PATH:/home/pascu/Moses/tools/srilm-1.7.1/bin/i686-m64/
export SCRIPTS_ROOTDIR=/home/pascu/Moses/tools/moses/scripts/
export GIZA=/home/pascu/Moses/tools/giza-pp-master/GIZA++-v2/
export MOSES=/home/pascu/Moses/tools/moses

# Definicion de Ngramas
Ngramas=3

# Suavizado
suavizado="-interpolate"

# Metodo descuento
descuento="-kndiscount"

# Iteraciones MERT
iteMert=5
#iteMert=10
#iteMert=15

# Variables
corpus="Corpus"
train="training_train"
dev="training_dev"

############################################################
# 4. CORPUS TRAIN
############################################################
# Accedemos al directorio del corpus
cd $corpus/train
# Los corpus ya estan limpios y tokenizados
# Separamos el corpus de train en dos partes (train+dev)
# 85% -> train; 15% -> dev
n_frases_train=$(cat training.en | wc -l)
n_frases_dev=$(echo "("$n_frases_train*"15)/100" | bc)
n_frases_train=$(echo $n_frases_train"-"$n_frases_dev | bc)
cat training.en | head -$n_frases_train > $train.en
cat training.es | head -$n_frases_train > $train.es
cat training.en | tail -$n_frases_dev > $dev.en
cat training.es | tail -$n_frases_dev > $dev.es

############################################################
# 5. ENTRENAMIENTO MODELOS DE LENGUAJE (PARA EL ESPANOL)
############################################################
# Creamos el directorio donde almacenamos los modelos de lenguaje
mkdir lm
# Obtenemos el modelo de lenguaje (LM)
ngram-count -order $Ngramas -unk $suavizado $descuento -text $train.es -lm lm/europarl.lm
# Nos guardamos la ruta del modelo de lenguaje
export LM=$PWD/lm/europarl.lm

############################################################
# 6. ENTRENAMIENTO MODELO DE TRADUCCIÓN
############################################################
# Construimos la tabla de segmentos
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work \
-corpus $train -f en -e es \
-alignment grow-diag-final-and -reordering msd-bidirectional-fe \
-lm 0:$Ngramas:$LM -external-bin-dir $GIZA>& training.out

############################################################
# 7. ENTRENAMIENTO DE LOS PESOS DEL MODELO LOG_LINEAL
############################################################
cd ..
# Obtenemos los pesos del modelo log-lineal mediante MERT
$MOSES/scripts/training/mert-moses.pl \
train/$dev.en train/$dev.es \
$MOSES/bin/moses train/work/model/moses.ini \
--maximum-iterations=$iteMert \
--mertdir $MOSES/bin/ \
--decoder-flags "-feature-name-overwrite \"SRILM KENLM\""
# Corregimos un error que provoca que MOSES tenga un fallo
sed ":a;N;$bash;s/\"SRILM\nKENLM/\"SRILM KENLM\"/" \
mert-work/moses.ini > mert-work/moses.europarl.ini

# Borramos los ficheros auxiliares generados
rm train/$train.*
rm train/$dev.*
