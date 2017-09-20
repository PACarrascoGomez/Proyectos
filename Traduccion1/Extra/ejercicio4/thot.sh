#!/bin/bash

##########################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TA
# Toolkit: thot
# Ejercicio: Avanzado -> Crear el traductor basico con el toolkit thot
##########################################################################

# # Nota: ./configure --enable-ibm2-alig
# # Nota: Con HMM salta un error, hemos de trabajar con el modelo 2 de IBM
# # Instalar
# #	1) cd thoth-master
# #	2) ./reconf
# #	3) ./configure --enable-ibm2-alig
# #	4) make
# #	5) sudo make install
# # Nota: Corregir Makefile para que thot escoja python2 como entorno de trabajo, 
# # con python3 da error.

# NOTA: Para solucionar el problema
# /usr/local/bin//thot_gen_sw_model: error while loading shared 
# libraries: libthot.so.0: cannot open shared object file: No such file or directory
# Instalar: sudo apt-get install libgconf2-dev 

# Tokenizamos el corpus
thot_tokenize -f Corpus/train/training.es > Corpus/train/training_tok.es
thot_tokenize -f Corpus/train/training.en > Corpus/train/training_tok.en
thot_tokenize -f Corpus/test/test.es > Corpus/test/test_tok.es
thot_tokenize -f Corpus/test/test.en > Corpus/test/test_tok.en

# Lowercasing (minusculas) el corpus
thot_lowercase -f Corpus/train/training_tok.es > Corpus/train/training_tok_lc.es
thot_lowercase -f Corpus/train/training_tok.en > Corpus/train/training_tok_lc.en
thot_lowercase -f Corpus/test/test_tok.es > Corpus/test/test_tok_lc.es
thot_lowercase -f Corpus/test/test_tok.en > Corpus/test/test_tok_lc.en

# Limpiamos el corpus
thot_clean_corpus_ln -s Corpus/train/training_tok_lc.en -t Corpus/train/training_tok_lc.es > line_numbers
thot_extract_sents_by_ln -f Corpus/train/training_tok_lc.en \
-n line_numbers > Corpus/train/training_tok_lc_clean.en
thot_extract_sents_by_ln -f Corpus/train/training_tok_lc.es \
-n line_numbers > Corpus/train/training_tok_lc_clean.es
thot_clean_corpus_ln -s Corpus/test/test_tok_lc.en -t Corpus/test/test_tok_lc.es > line_numbers
thot_extract_sents_by_ln -f Corpus/test/test_tok_lc.en \
-n line_numbers > Corpus/test/test_tok_lc_clean.en
thot_extract_sents_by_ln -f Corpus/test/test_tok_lc.es \
-n line_numbers > Corpus/test/test_tok_lc_clean.es

# Separamos el train en train + dev
# 85% -> train; 15% -> dev
n_frases_train=$(cat Corpus/train/training_tok_lc.en | wc -l)
n_frases_dev=$(echo "("$n_frases_train*"15)/100" | bc)
n_frases_train=$(echo $n_frases_train"-"$n_frases_dev | bc)
cat Corpus/train/training_tok_lc_clean.en | head -$n_frases_train > Corpus/train/en_tok_lc_clean.train
cat Corpus/train/training_tok_lc_clean.es | head -$n_frases_train > Corpus/train/sp_tok_lc_clean.train
cat Corpus/train/training_tok_lc_clean.en | tail -$n_frases_dev > Corpus/train/en_tok_lc_clean.dev
cat Corpus/train/training_tok_lc_clean.es | tail -$n_frases_dev > Corpus/train/sp_tok_lc_clean.dev

# Renombramos el test
mv Corpus/test/test_tok_lc_clean.en Corpus/test/en_tok_lc_clean.test
mv Corpus/test/test_tok_lc_clean.es Corpus/test/sp_tok_lc_clean.test

# define variables (optional)
src_train_corpus=Corpus/train/en_tok_lc_clean.train
trg_train_corpus=Corpus/train/sp_tok_lc_clean.train
src_dev_corpus=Corpus/train/en_tok_lc_clean.dev
trg_dev_corpus=Corpus/train/sp_tok_lc_clean.dev
src_test_corpus=Corpus/test/en_tok_lc_clean.test
trg_test_corpus=Corpus/test/sp_tok_lc_clean.test

# train system
thot_lm_train -c ${trg_train_corpus} -o lm_outdir -n 3 -unk
thot_tm_train -s ${src_train_corpus} -t ${trg_train_corpus} -o tm_outdir

# generate cfg file
thot_gen_cfg_file lm_outdir/lm_desc tm_outdir/tm_desc > before_tuning.cfg

# tune system
thot_smt_tune -c before_tuning.cfg -s ${src_dev_corpus} -t ${trg_dev_corpus} \
-o tune

# filter phrase model
thot_prepare_sys_for_test -c tune/tuned_for_dev.cfg -t ${src_test_corpus} \
-o systest

# translate test corpus
thot_decoder -c systest/test_specific.cfg -t ${src_test_corpus} -o output

# evaluate translation quality
thot_calc_bleu -r ${trg_test_corpus} -t output