#! /bin/bash

# Ejemplo: ./generar_resultados.sh ../data/qa194.data.txt 1000 resultados_viajante_qa194.txt

##################################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TIA
# Script: Obtener resultados con algoritmo enfriamiento simulado
##################################################################


# Comprobacion de parametros
if [ $# -ne 3 ]; then 
	echo 'USO: ./generar_resultados.sh <data.txt> <Temperatura> <fichero_salida>'
	exit
fi

# Directorio donde se encuentran los datos
data=$1

# Temperatura inicial del algoritmo por enfriamiento simulado
T=$2

# Valores de los bucles
iteraciones=(100 1000 10000 30000) # Iteraciones del bucle
n_vecinos=(5 10 20 30) # Numero de vecinos

# Creamos el fichero de salida (fichero de resultados)
salida=$3
echo > $salida

# Ejecucion
for nv in ${n_vecinos[*]}; do
	echo "Temperatura = $T, n_vecinos = $nv, $data" >> $salida
	echo >> $salida
	for i in ${iteraciones[*]}; do
		echo "------------------------------------------------------" >> $salida
		echo "n_iteraciones = $i" >> $salida
		echo "------------------------------------------------------" >> $salida
		for r in $( seq 1 1 5); do
			python2.7 viajante_vecinos.py $data $i $T 0.8 $nv False >> $salida
			echo >> $salida
		done
	done
	echo >> $salida "##############################################################################################################################################################"
done

