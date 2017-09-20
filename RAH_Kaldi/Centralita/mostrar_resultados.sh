#!/bin/bash

# Muestra los mejores WERT obtenidos (mono,tri)
for x in exp/*/decode*; do 
	[ -d $x ] && grep WER $x/wer_* | utils/best_wer.sh; 
done
exit 0

