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

# Variables
corpus="Corpus"

############################################################
# 8. PROCESO DE TRADUCCION
############################################################
cd $corpus/test
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f ../mert-work/moses.europarl.ini < test.en > test.hyp

############################################################
# 9. EVALUACION
############################################################
$MOSES/scripts/generic/multi-bleu.perl -lc test.es < test.hyp
