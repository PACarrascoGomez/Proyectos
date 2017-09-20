#!/bin/bash

###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Preparamos el lenguaje para la Centralita
###########################################################

# Creamos el directorio donde vamos a trabajar
if [ -d conf ]; then
	rm -R conf
fi
mkdir conf

# Creamos los ficheros de conf necesario
echo "--use-energy=false" > conf/mfcc.conf
echo "first_beam=10.0
beam=13.0
lattice_beam=6.0" > conf/decode.config
