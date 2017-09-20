#!/bin/bash

# Fichero con el que trabajamos
# NOTA: Generado por obtener_alturas.sh
fichero='alturas_corpus.txt'

# Comprobacion de parametros
if [ $# -ne 1 ]; then 
	echo 'No has introducido un corpus de imagenes'
	echo './generacion_random.sh path_corpus'
	exit
fi

# Ruta del corpus de imagen con el que trabajamos
ruta=$1

# Directorio donde almacenamos las imagenes segmentadas por la altura obtenida
dir_salida='corpus_segmentado'
if [ -d $dir_salida ];
	then rm -R ./$dir_salida
fi

# Creamos el directorio de salida
mkdir $dir_salida

# Generamos las imagenes segmentadas
while read linea
do
   imagen=$(echo $linea | awk '1 { print $3 }')
   altura=$(echo $linea | awk '1 { print $4 }')
   ../segmentar -i $ruta/$imagen -p $altura -o ./corpus_segmentado/$imagen
done < $fichero