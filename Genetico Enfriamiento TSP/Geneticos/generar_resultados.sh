#! /bin/bash

# Ejemplo: ./generar_resultados.sh ../data/qa194.data.txt resultados_viajante_qa194.txt

###################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: TIA
# Script: Obtener resultados con algoritmo genetico
###################################################


# Comprobacion de parametros
if [ $# -ne 2 ]; then 
	echo 'USO: ./generar_resultados.sh <data.txt> <fichero_salida>'
	exit
fi

# Directorio donde se encuentran los datos
data=$1

# Valores de los bucles
generaciones=(100 1000 10000 30000) # Iteraciones del bucle
nindp=(5 10 20 30) # Numero de individuos en la poblacion

# Creamos el fichero de salida (fichero de resultados)
salida=$2
echo > $2

# Ejecucion
for ip in ${nindp[*]}; do
	sp=$(echo "$ip / 2" | bc) # Los padres seleccionados son la mitad del numero de individuos
	echo "n_individuos_pob = $ip, n_padres = $sp, $data" >> $salida
	echo >> $salida
	for g in ${generaciones[*]}; do
		echo "------------------------------------------------------" >> $salida
		echo "n_generaciones = $g" >> $salida
		echo "------------------------------------------------------" >> $salida
		for r in $( seq 1 1 5); do
			python2.7 viajante.py $data $g $ip $sp False >> $salida
			echo >> $salida
		done
	done
	echo >> $salida "##############################################################################################################################################################"
done

