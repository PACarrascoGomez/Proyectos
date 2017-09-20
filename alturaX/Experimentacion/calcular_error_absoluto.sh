#!/bin/bash

# Ficheros y directorios con los que trabaja el script
fichero='generacion_datos.txt'
salida='error_absoluto_obtenido.txt'

# Obtenemos el numero de lineas del fichero
n_lineas=$(wc -l $fichero | awk '1 { print $1 }')

# Creamos un fichero vacio independientemente de que exista o no
echo '---------------------------' > $salida
echo 'Numero de datos: ' $n_lineas >> $salida
echo '---------------------------' >> $salida

# Calculamos el error con diferencias en valor absoluto de:
# 1,2,3,4 y 5 pixeles
for i in {1..5}; do

	# Cantidad de errores
	n_errores=0

	for j in `seq 1 $n_lineas`; do
		
		# Obtenemos la linea $i del fichero
		linea=$(head -$j $fichero | tail -1)

		# Obtenemos la diferencia en valor absoluto de la altura real
		# y la altura que ha devuelto nuestro sistema respecto al escalado
		altura_real=$(echo $linea | awk '1 { print $9 }') 
		altura_sistema=$(echo $linea | awk '1 { print $10 }') 
		diferencia=`expr $altura_real - $altura_sistema`
		diferencia=${diferencia#-} # valor absoluto
		
		# Convertimos las cadenas a numeros enteros
		let dif_num=$diferencia
		let i_num=$i

		if [ $dif_num -gt $i_num ]; then
			n_errores=`expr $n_errores + 1`
		fi

	done

	error_obtenido=$(echo "scale=6;($n_errores/$n_lineas)*100" | bc)
	echo 'Diferencia: ' $i ' pixeles, numero de errores: ' $n_errores ', error obtenido: ' $error_obtenido ' %' >> $salida

done