#!/bin/bash

###############################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Limpiar y tokenizar los corpus de train+test
###############################################################

# Nota: Realizar los EXPORT para crear el entorno
export PATH=$PATH:/home/pascu/Moses/tools/moses/bin/
export PATH=$PATH:/home/pascu/Moses/tools/moses/scripts/training/
export PATH=$PATH:/home/pascu/Moses/tools/srilm-1.7.1/bin/i686-m64/
export SCRIPTS_ROOTDIR=/home/pascu/Moses/tools/moses/scripts/
export GIZA=/home/pascu/Moses/tools/giza-pp-master/GIZA++-v2/
export MOSES=/home/pascu/Moses/tools/moses

# LIMPIAMOS EL CORPUS TRAIN
# Accedemos al corpus de train
cd Corpus/train/
# Limpiar el corpus
clean-corpus-n.perl training es en training.clean 1 60
# Tokenizamos los corpus
$MOSES/scripts/tokenizer/tokenizer.perl -l en < training.clean.en > training.clean.tok.en
$MOSES/scripts/tokenizer/tokenizer.perl -l es < training.clean.es > training.clean.tok.es

# LIMPIAMOS EL CORPUS TEST
# Accedemos al corpus de test
cd ../test/
# Limpiar el corpus
clean-corpus-n.perl test es en test.clean 1 60
# Tokenizamos los corpus
$MOSES/scripts/tokenizer/tokenizer.perl -l en < test.clean.en > test.clean.tok.en
$MOSES/scripts/tokenizer/tokenizer.perl -l es < test.clean.es > test.clean.tok.es

