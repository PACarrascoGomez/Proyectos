#!/bin/bash

###############################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Limpiar los corpus de train+dev+test
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
clean-corpus-n.perl training en ja training.clean.tok 1 60
clean-corpus-n.perl dev en ja dev.clean.tok 1 60

# LIMPIAMOS EL CORPUS TEST
# Accedemos al corpus de test
cd ../test/
# Limpiar el corpus
clean-corpus-n.perl test en ja test.clean.tok 1 60


