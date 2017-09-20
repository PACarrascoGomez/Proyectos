# -------------------------------------------------------- 
# Autor: Pascual A. Carrasco Gomez
# --------------------------------------------------------
# Descripcion:
# - Muestra la solucion de forma grafica y comprueba la solucion
# --------------------------------------------------------
import sys

def comprobarSolucion(m):
	correcto = True
	v = 45 # (1+2+3+4+5+6+7+8+9 = 45)
	# Comprobamos filas
	for i in range(len(m)):
		if sum(m[i]) != v:
			print "Error en la fila: ",i+1
			correcto = False
	# Comprobamos columnas
	for i in range(len(m)):
		aux = 0
		for j in range(len(m)):
			aux = aux + m[j][i]
		if aux != v:
			print "Error en la columna: ",i+1
			correcto = False
	# Comprobamos los bloques
	for i in range(0,7,3):
		for j in range(0,7,3):
			aux = 0
			for z in range(3):
				aux = aux + sum(m[j+z][i:i+3])
			if aux != v:
				print "Error en el bloque: ",(i/3)+j+1
				correcto = False
	if correcto:
		print "Solucion correcta!!!"

# Comprobamos parametros pasados por teclado
if len(sys.argv) != 2:
	print "Ejecucion: python2.7 sudoku.py fichero";
	sys.exit(0)
# Abrimos el fichero con el conjunto de soluciones
fichero = open(sys.argv[1], 'r')
# Obtenemos el contenido del fichero
texto = fichero.read()
# Trabajamos sobre el contenido
solucion = texto.split("SOLUTION")
# Quitamos el primer elemento de la lista
solucion = solucion[1:len(solucion)]
# Separamos y formateamos la solucion
aux = solucion[0].split("sat")
aux = aux[0].split("   ")
aux = aux[1:len(aux)]
u_valor = aux[len(aux)-1]
u_valor = u_valor.strip("   ")
aux.pop()
aux.append(u_valor)
solucion = aux
# Creamos una matriz de 9x9 para la solucion
matriz = []
for j in range(9):
	matriz.append([0,0,0,0,0,0,0,0,0])
# Rellenamos la matriz con la solucion obtenida
for j in range(len(solucion)):
	fila = int(solucion[j][1])
	col = int(solucion[j][2])
	valor = int(solucion[j][6])
	matriz[fila-1][col-1] = valor
# Imprimimos las matrices con formato 
for j in range(len(matriz)):
	print matriz[j]
print "\n"
print"-------------------------------------------------------------------"
# Comprobamos que la solucion es correcta
comprobarSolucion(matriz)
print"-------------------------------------------------------------------"

