#!/bin/bash

# Comprobacion de parametros
if [ $# -ne 1 ]; then 
	echo 'No has introducido un corpus de imagenes'
	echo './generacion_random.sh path_corpus'
	exit
fi

# Ruta del corpus de imagen con el que trabajamos
ruta_corpus=$1

# Creamos un fichero vacio independientemente de que exista o no
> alturas_corpus.txt

# Generamos un fichero que contiene:
# filas columnas imagen altura
for i in $( ls $ruta_corpus ); do
	imagen=$i
	columnas=$(identify $ruta_corpus$imagen | awk '{ print $3 }' | cut -d 'x' -f 1)
	filas=$(identify $ruta_corpus$imagen | awk '{ print $3 }' | cut -d 'x' -f 2)
	altura=$(../alturaX -i $ruta_corpus/$imagen)
	echo $filas $columnas $imagen $altura >> alturas_corpus.txt
done