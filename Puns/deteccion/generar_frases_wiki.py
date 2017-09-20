import sys
import wikipedia as wiki

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Generacion de fichero con frases --> no puns
# Metodo: Wikipedia
# Nota: No se obtenian buenos resultados
# 		Los no puns en el coprus deben ser proverbios y refranes
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Ejemplo: python3 generar_frases_wiki.py 100 frases_wiki.txt

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 generar_frases_wiki.py <n_frases> <f_out>")
	exit()

# Parametros
n_frases = int(sys.argv[1])
f_out = sys.argv[2]

# Numero de frases obtenidas por cada entrada (Aproximacion para mantener la variabilidad)
n_frases_entrada = 10

# Entradas ya buscadas en la wiki (evitar repeticiones)
vistos = []

# Numero de frases generadas
n_frases_gen = 0

# Lista de frases resultante
frases = []

# Generacion de frases aleatoria 
# Nota: Restriccion corpus --> El tamano de la frase ha de ser entre 10 y 20 palabras
while n_frases_gen < n_frases:
	entrada = wiki.random()
	entrada_valida = True
	try:
		wiki.page(entrada)
	except:
		entrada_valida = False
	while entrada in vistos or not(entrada_valida):
		entrada = wiki.random()
		try:
			wiki.page(entrada)
			entrada_valida = True
		except:
			entrada_valida = False
	vistos.append(entrada)
	texto = wiki.page(entrada).content
	frases_texto = texto.split("\n")
	i = 0 
	while i < n_frases_entrada and i < len(frases_texto) and n_frases_gen < n_frases:
		frase = frases_texto[i]
		palabras = frase.split(" ")
		if len(palabras) >= 10 and len(palabras) <= 20: # Restriccion corpus
			frases.append(frase)
			n_frases_gen += 1
		i += 1

# Mostramos las entradas de donde se han obtenido las frases
print ("------------------------------------------")
print ("Entradas (Paginas Wikipedia):")
print ("------------------------------------------")
for e in vistos:
	print (e)

# Mostramos las frases generadas por consola
print ("------------------------------------------")
print ("Frases Generadas:")
print ("------------------------------------------")
for f in frases:
	print (f)
print ("##########################################")
print ("Total frases generadas:",len(frases))
print ("##########################################")

# Almacenamos las frases en el fichero de salida
fo = open(f_out,"w")
for f in frases:
	fo.write(f + "\n")
fo.close()

