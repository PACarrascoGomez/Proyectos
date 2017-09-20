#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Trabajo: Evaluacion traductor post edicion 
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
# Traducimos del ingles al espanol
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f traductor-en-es/moses.europarl.ini < test_eb.clean.tok.en > trad_es_eb.hyp

# Traducimos del espanol al espanol
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f Corpus/mert-work/moses.europarl.ini < trad_es_eb.hyp > trad_es_pos_ed.hyp

############################################################
# 9. EVALUACION
############################################################
$MOSES/scripts/generic/multi-bleu.perl -lc test_eb.clean.tok.es < trad_es_pos_ed.hyp > res_bleu_trad_es_hyp_final.txt