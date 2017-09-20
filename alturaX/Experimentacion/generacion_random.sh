#!/bin/bash

# Comprobacion de parametros
if [ $# -ne 1 ]; then 
	echo 'No has introducido un corpus de imagenes'
	echo './generacion_random.sh path_corpus'
	exit
fi

# Ruta del corpus de imagen con el que trabajamos
ruta_corpus=$1

# Ficheros y directorios con los que trabaja el script
fichero='alturas_corpus.txt'
salida='generacion_datos.txt'
dir_img_escaladas='imagenes_corpus_escaladas'

# Creamos un fichero vacio independientemente de que exista o no
> $salida

# Comprobamos que no exista el directorio de salida
if [ -d $dir_img_escaladas ];
	then rm -R ./$dir_img_escaladas
fi

# Creamos el directorio
mkdir $dir_img_escaladas

# Generamos un fichero que contiene:
# filas columnas imagen altura porcentaje operacion filas_escala columnas_escala altura_real altura_escala
for i in {1..200}; do

	# Obtenemos una imagen aleatoria del corpus
	# Guardamos su informacion
	muestras=150
	numero=`expr $RANDOM % $muestras`
	numero=`expr $numero + 1`
	datos=$(head -$numero $fichero | tail -1 | awk '1 { print $1,$2,$3,$4 }')
	filas=$(echo $datos | cut -d ' ' -f 1)
	columnas=$(echo $datos | cut -d ' ' -f 2)
	imagen=$(echo $datos | cut -d ' ' -f 3)
	altura=$(echo $datos | cut -d ' ' -f 4)

	# Generamos un porcentaje aleatorio para escalar la imagen
	porcentaje=`expr $RANDOM % 60`
	porcentaje=`expr $porcentaje + 10`

	# Generamos una operacion aleatoria
	# Operacion 1: aumentar la imagen
	# Operacion 2: disminuir la imagen
	operacion=`expr $RANDOM % 2`
	operacion=`expr $operacion + 1`

	# Calculamos la nueva dimension de la imagen respecto al numero de columnas
	columnas_s=`expr $columnas \* $porcentaje` 
	columnas_s=`expr $columnas_s / 100`
	if [ $operacion = '1' ];
		then columnas_s=`expr $columnas + $columnas_s`
	else
		 columnas_s=`expr $columnas - $columnas_s`
	fi

	# Escalamos la imagen 
	convert -scale $columnas_s $ruta_corpus$imagen $dir_img_escaladas/$imagen

	# Obtenemos la altura de la imagen escalada
	altura_s=$(../alturaX -i $dir_img_escaladas/$imagen)

	# Altura que correspondiente a la escala realizada
	altura_real=`expr $altura \* $porcentaje` 
	altura_real=`expr $altura_real / 100`
	if [ $operacion = '1' ];
		then altura_real=`expr $altura + $altura_real`
	else
		 altura_real=`expr $altura - $altura_real`
	fi

	columnas_s=$(identify $dir_img_escaladas/$imagen | awk '{ print $3 }' | cut -d 'x' -f 1)
	filas_s=$(identify $dir_img_escaladas/$imagen | awk '{ print $3 }' | cut -d 'x' -f 2)

	# Almacenamos la informacion obtenida
	echo $filas $columnas $imagen $altura $porcentaje $operacion $filas_s $columnas_s $altura_real $altura_s >> $salida

done

# Borra
rm -R $dir_img_escaladas