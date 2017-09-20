#!/bin/bash

# Ficheros y directorios con los que trabaja el script
fichero='generacion_datos.txt'
salida='error_relativo_obtenido.txt'

# Obtenemos el numero de lineas del fichero
n_lineas=$(wc -l $fichero | awk '1 { print $1 }')

# Creamos un fichero vacio independientemente de que exista o no
echo '---------------------------' > $salida
echo 'Numero de datos: ' $n_lineas >> $salida
echo '---------------------------' >> $salida

error_medio=0

for j in `seq 1 $n_lineas`; do
	
	# Obtenemos la linea $i del fichero
	linea=$(head -$j $fichero | tail -1)

	# Obtenemos la diferencia en valor absoluto de la altura real
	# y la altura que ha devuelto nuestro sistema respecto al escalado
	altura_real=$(echo $linea | awk '1 { print $9 }') 
	altura_sistema=$(echo $linea | awk '1 { print $10 }') 
	diferencia=`expr $altura_real - $altura_sistema`
	diferencia=${diferencia#-} # valor absoluto

	# Calculamos el error absoluto
	error_obtenido=$(echo "scale=6;$diferencia/$altura_real" | bc)
	error_medio=$(echo "scale=6;$error_medio+$error_obtenido" | bc)

done

# Calculamos la media del error absoluto
error_medio=$(echo "scale=6;$error_medio/$n_lineas" | bc)

echo 'Error relativo: ' $error_medio >> $salida
