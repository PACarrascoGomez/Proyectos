# -------------------------------------------------------- 
# Autor: Pascual A. Carrasco Gomez
# --------------------------------------------------------
# Descripcion:
# - Muestra las correccion del CSP de reuniones
# --------------------------------------------------------
import sys

# ---------------------------------------------------------------------------
# MA = 0
# MD = 1
# ML = 2
# MP = 3
# ME = 4
# MR = 5
# EA = 6
# ED = 7
# EL = 8
# EP = 9
# EE = 10
# ER = 11
def comprobar_sol(s):
	# R1
	if(s[0][-1] == s[6][-1] and s[1][-1] == s[7][-1] and s[2][-1] == s[9][-1]):
		if(s[4][-1] != s[11][-1]):
			return "R1"
	# R2
	if(s[0][-1] == s[6][-1] and s[3][-1] == s[9][-1] and s[1][-1] == s[10][-1]):
		if(s[5][-1] == s[8][-1]):
			return "R2"
	# R3
	if(s[4][-1] == s[5][-1] and s[5][-1] == s[10][-1] and s[10][-1] == s[11][-1] and s[0][-1] != s[7][-1]):
		if(s[2][-1] == s[9][-1]):
			return "R3"
	# R4
	if(s[0][-1] == s[6][-1] and s[5][-1] == s[11][-1] and s[1][-1] != s[10][-1]):
		if(s[2][-1] != s[9][-1]):
			return "R4"
	# R5
	if(s[2][-1] == s[8][-1] and s[3][-1] == s[9][-1] and s[4][-1] == s[11][-1]):
		if(s[0][-1] == s[7][-1]):
			return "R5"
	# R6
	if(s[1][-1] == s[4][-1] and s[4][-1] == s[7][-1] and s[7][-1] == s[10][-1] and s[2][-1] != s[9][-1]):
		if(s[5][-1] != s[8][-1]):
			return "R6"
	# R7
	if(s[3][-1] == s[6][-1]):
		if(s[0][-1] != s[6][-1]):
			return "R7"
	# R8
	if(s[9][-1] == s[8][-1]):
		if(s[2][-1] == s[3][-1]):
			return "R8"
	# R9
	if(s[0][-1] == s[6][-1] and s[1][-1] == s[7][-1] and s[2][-1] == s[8][-1] and s[3][-1] == s[9][-1] and s[4][-1] == s[10][-1] and s[5][-1] == s[11][-1]):
		return "R9"
	# R10
	aux = 0
	for i in range(len(s)):
		aux += int(s[i][-1])
	if(aux < 4):
		return "R10"
	if(aux > 8):
		return "R10"

	# La solucion satisface las soluciones
	return "correcto"

# ---------------------------------------------------------------------------



# Comprobamos parametros pasados por teclado
if len(sys.argv) != 2:
	print "Ejecucion: python2.7 sudoku_todas.py fichero";
	sys.exit(0)
# Abrimos el fichero con el conjunto de soluciones
fichero = open(sys.argv[1], 'r')
# Obtenemos el contenido del fichero
texto = fichero.read()
# Trabajamos sobre el contenido
soluciones = texto.split("SOLUTION")
# Quitamos el primer elemento de la lista
soluciones = soluciones[1:len(soluciones)]
# Separamos y formateamos cada solucion
lista_soluciones = []
for i in range(len(soluciones)):
	aux = soluciones[i].split("sat")
	aux = aux[0].split("   ")
	aux = aux[1:len(aux)]
	u_valor = aux[len(aux)-1]
	u_valor = u_valor.strip("   ")
	aux.pop()
	aux.append(u_valor)
	lista_soluciones.append(aux)
# Comprobamos cada solucion
error = False
for i in range(len(lista_soluciones)):
	res = comprobar_sol(lista_soluciones[i]);
	if(res != "correcto"):
		print "\nError en la solucion: ",i+1, ", en la restriccion: ",res
		error = True
if(error == False):
	print "Todas las soluciones analizadas son correctas"
