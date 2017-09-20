#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Trabajo: Extra (Test con Ngramas) -> Ejercicio1
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
# Nota: Los corpus en este ejercicio ya han sido limpiados 
# ,tokenizados y divididos en Ngramas -> limpiar_corpus.sh 
# y se han generado los corpus con 2gramas.py
# Traducimos
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f mert-work/moses.europarl.ini < test_2gramas.en > test.hyp

############################################################
# 9. EVALUACION
############################################################
$MOSES/scripts/generic/multi-bleu.perl -lc test_2gramas.es < test.hyp > res_bleu.txt