import sys

###################################################################################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Genera la tabla con los resultados obtenidos en los ficheros generados por generar_resultados.sh
# utilizando la mediana de cada ejecucion
###################################################################################################################

# Comprobacion de parametros de entrada
if len(sys.argv) != 2:
	print "-------------------------------------------------------------------------------------"
	print "Uso: python2.7 obtener_tablas.py <fichero_resultados>"
	print "-------------------------------------------------------------------------------------"
	print "<fichero_resultados>: Fichero con los resultados obtenidos de generar_resultados.sh"
	sys.exit(0)

# Alacenamos el parametro de entrada
fichero = sys.argv[1]

f_entrada = open(fichero,'r')
texto = f_entrada.read()
texto_parseado = texto.split("Puntuacion : ")

# Obtenemos una lista de todas las puntuaciones obtenidas
puntuaciones = []
for i in range(1,len(texto_parseado)):
	puntuacion = texto_parseado[i].split("\n")[0]
	puntuaciones.append(puntuacion)

# Obtenemos la mediana de cada bloque_agrupacion que corresponde a una celda de la tabla
bloque_agrupacion = 5
tabla = []
indice_mediana = bloque_agrupacion/2
for i in range(0,len(puntuaciones),bloque_agrupacion):
	bloque = puntuaciones[i:i+bloque_agrupacion]
	bloque_ord = sorted(bloque)
	mediana = bloque_ord[indice_mediana]
	tabla.append(mediana)

columnas = 4 # Generaciones = 100 1000 10000 30000
tabla_lista = []
# Dividimos la tabla en filas y columnas
for i in range(0,len(tabla),columnas):
	tabla_lista.append(tabla[i:i+columnas])

aux_fila = ""
# Mostramos la tabla
for fila in tabla_lista:
	for valor in fila:
		aux_fila += valor.split("\n")[0] + "\t"
	print aux_fila
	aux_fila = ""
