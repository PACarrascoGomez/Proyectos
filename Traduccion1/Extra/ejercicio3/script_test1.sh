#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Trabajo: Ejercicio extra -> post-edicion
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
cd Corpus
# Limpiar el corpus
clean-corpus-n.perl europarl-v7.es-en-train-red-PE es en test.clean 1 60
# Tokenizamos los corpus
$MOSES/scripts/tokenizer/tokenizer.perl -l en < test.clean.en > test.clean.tok.en
$MOSES/scripts/tokenizer/tokenizer.perl -l es < test.clean.es > test.clean.tok.es
# Traducimos
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f ../traductor-en-es/moses.europarl.ini < test.clean.tok.en > trad_es.hyp

############################################################
# 9. EVALUACION
############################################################
$MOSES/scripts/generic/multi-bleu.perl -lc test.clean.tok.es < trad_es.hyp > res_bleu_trad_es_hyp.txt