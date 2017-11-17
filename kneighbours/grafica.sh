#!/bin/bash

####################################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Resultados (Grafica): k vecinos mas cercanos
# Entorno: bash
# Sistema operativo: Linux Mint 18.2
####################################################################

# Ejemplo de ejecucion: ./grafica.sh iris.dat 30

# Dependencias para que funcione el script
# sudo apt-get install gnuplot

# Comprobacion de parametros
if [ $# -ne 2 ]; then
	echo "Uso: ./grafica.sh <data.dat> <n_k>"
	exit
fi

# Obtenemos los datos de la grafica
k=()
a=()
for i in $(seq 1 $2); do
	aciertos=$(python3 kneighbours.py $1 $i | grep "Precision" | cut -d ":" -f 2)
	k[$i]=$i
	a[$i]=$aciertos
done

# Mostrar los datos de la grafica por consola
#echo ${k[*]}
#echo ${a[*]}

# Volcamos los datos de la grafica a un fichero
cat /dev/null > grafica.dat
for i in $(seq 1 $2); do
	echo "${k[$i]} ${a[$i]}" >> grafica.dat
done

# Mostramos la grafica con gnuplot
gnuplot -persist <<-EOFMarker
    set title "Estudio parametro K del algoritmo K-Neighbours" font ",14" textcolor rgbcolor "royalblue"
    set yrange [0:1]
    set xrange [0:$k]
    set ylabel "Precision"
    set xlabel "k"
    unset key
    plot "grafica.dat" using 1:2 with linespoints
EOFMarker

# Eliminamos los archivos auxiliares creados para la grafica
rm grafica.dat