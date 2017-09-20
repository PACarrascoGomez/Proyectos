import sys

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Codifica el corpus de puns y no puns
# Metodo: Enumeracion simple
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Ejemplo: python3 codificar_corpus.py frases_no_pun.txt

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 codificar_corpus.py <f_puns> <f_no_puns>")
	exit()

# Parametros
f_puns = sys.argv[1]
f_no_puns = sys.argv[2]

# Id numerico incrementativo
id_num = 0

# Fichero .gold
fo_gold = open("frases_gold.txt","w")

# Fichero con las frases (puns y no_puns) enumeradas
fo_frases = open("frases.txt","w")

# Codificamos puns
f = open(f_puns,"r")
frases = f.read().split("\n")[:-1]
f.close()
for frase in frases:
	#frase = frase.split("\t")[1] # Para el dev
	fo_frases.write(str(id_num) + "\t" + frase + "\n")
	fo_gold.write(str(id_num) + "\t" + "1\n")
	id_num += 1

# Codificamos no_puns
f = open(f_no_puns,"r")
frases = f.read().split("\n")[:-1]
f.close()
for frase in frases:
	#frase = frase.split("\t")[1] # Para el dev
	fo_frases.write(str(id_num) + "\t" + frase + "\n")
	fo_gold.write(str(id_num) + "\t" + "0\n")
	id_num += 1

# Cerramos los ficheros de salida
fo_gold.close()
fo_frases.close()