#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Practica: 2
# Trabajo: Extra
###################################################################

# Nota: Realizar los EXPORT para crear el entorno
export PATH=$PATH:/home/pascu/Moses/tools/moses/bin/
export PATH=$PATH:/home/pascu/Moses/tools/moses/scripts/training/
export PATH=$PATH:/home/pascu/Moses/tools/srilm-1.7.1/bin/i686-m64/
export SCRIPTS_ROOTDIR=/home/pascu/Moses/tools/moses/scripts/
export GIZA=/home/pascu/Moses/tools/giza-pp-master/GIZA++-v2/
export MOSES=/home/pascu/Moses/tools/moses

############################################################
# 8. PROCESO DE TRADUCCION
############################################################
cd Corpus/test
# Nota: Los corpus ya estan limpios y tokenizados -> limpiar_corpus.sh
$MOSES/bin/moses_chart \
-f ../train/work/model/moses.ini < test.clean.tok.en > test.hyp

############################################################
# 9. EVALUACION
############################################################
$MOSES/scripts/generic/multi-bleu.perl -lc test.clean.tok.ja < test.hyp