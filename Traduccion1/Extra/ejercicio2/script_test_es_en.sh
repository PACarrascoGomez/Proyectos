#!/bin/bash

###################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA (Traduccion automatica)
# Trabajo: Ejercicio 2 (degradacion)
###################################################################

# Nota: Realizar los EXPORT para crear el entorno
export PATH=$PATH:/home/pascu/Moses/tools/moses/bin/
export PATH=$PATH:/home/pascu/Moses/tools/moses/scripts/training/
export PATH=$PATH:/home/pascu/Moses/tools/srilm-1.7.1/bin/i686-m64/
export SCRIPTS_ROOTDIR=/home/pascu/Moses/tools/moses/scripts/
export GIZA=/home/pascu/Moses/tools/giza-pp-master/GIZA++-v2/
export MOSES=/home/pascu/Moses/tools/moses

# Fichero de salida
out="res_degradacion_bleu_es_en.txt"

############################################################
# 8. PROCESO DE TRADUCCION + EVALUACION EN AMBOS SENTIDOS
############################################################
# Los corpus de test en este ejercicio ya estan limpios y tokenizados

echo "-------------------------------
sentido español ingles
-------------------------------"  > $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/es_en_moses.europarl.ini < test/test.clean.tok.es > test_en.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.en < test_en.hyp >> $out

echo "-------------------------------
sentido ingles español
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/en_es_moses.europarl.ini < test_en.hyp > test_es.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.es < test_es.hyp >> $out

echo "-------------------------------
sentido español ingles
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/es_en_moses.europarl.ini < test_es.hyp > test_en.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.en < test_en.hyp >> $out

echo "-------------------------------
sentido ingles español
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/en_es_moses.europarl.ini < test_en.hyp > test_es.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.es < test_es.hyp >> $out

echo "-------------------------------
sentido español ingles
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/es_en_moses.europarl.ini < test_es.hyp > test_en.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.en < test_en.hyp >> $out

echo "-------------------------------
sentido ingles español
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/en_es_moses.europarl.ini < test_en.hyp > test_es.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.es < test_es.hyp >> $out

echo "-------------------------------
sentido español ingles
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/es_en_moses.europarl.ini < test_es.hyp > test_en.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.en < test_en.hyp >> $out

echo "-------------------------------
sentido ingles español
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/en_es_moses.europarl.ini < test_en.hyp > test_es.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.es < test_es.hyp >> $out

echo "-------------------------------
sentido español ingles
-------------------------------"  >> $out
$MOSES/bin/moses -feature-name-overwrite "SRILM KENLM" \
-f modelos/es_en_moses.europarl.ini < test_es.hyp > test_en.hyp
$MOSES/scripts/generic/multi-bleu.perl -lc test/test.clean.tok.en < test_en.hyp >> $out
