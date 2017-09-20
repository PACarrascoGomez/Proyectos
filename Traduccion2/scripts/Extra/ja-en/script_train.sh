#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Practica: 2
# Ejercicio: Extra
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
train="training.clean.tok"
dev="dev.clean.tok"

# Configuracion max-phrase-length
#mpl=3
mpl=5

# Accedemos al directorio del corpus
cd $corpus/train

############################################################
# 5. ENTRENAMIENTO MODELOS DE LENGUAJE (PARA EL INGLES)
############################################################
# Creamos el directorio donde almacenamos los modelos de lenguaje
mkdir lm
# Obtenemos el modelo de lenguaje (LM)
ngram-count -order 5 -unk \
-kndiscount -text $train.en -lm lm/modelo.lm
# Nos guardamos la ruta del modelo de lenguaje
export LM=$PWD/lm/modelo.lm

############################################################
# 6. ENTRENAMIENTO MODELO DE TRADUCCIÓN
############################################################
# Construimos la tabla de segmentos
$SCRIPTS_ROOTDIR/training/train-model.perl -root-dir work \
-corpus $train -f ja -e en -alignment grow-diag-final-and \
-lm 0:5:$LM -external-bin-dir $GIZA -hierarchical -glue-grammar -max-phrase-length $mpl

############################################################
# 7. ENTRENAMIENTO DE LOS PESOS DEL MODELO LOG_LINEAL
############################################################
# Obtenemos los pesos del modelo log-lineal mediante MERT
cd ..
$MOSES/scripts/training/mert-moses.pl \
train/$dev.ja train/$dev.en \
$MOSES/bin/moses train/work/model/moses.ini \
--maximum-iterations=5 \
--mertdir $MOSES/bin/ \
--decoder-flags "-feature-name-overwrite \"SRILM KENLM\""
# Corregimos un error que provoca que MOSES tenga un fallo
mv train/work/model/moses.ini train/work/model/moses.ini.old
sed 's/SRILM/KENLM/g' train/work/model/moses.ini.old > train/work/model/moses.ini