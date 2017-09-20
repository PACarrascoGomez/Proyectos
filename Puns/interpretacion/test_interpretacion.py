import sys
from utils import *


##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Interpretacion de puns (tarea 7.3 Semeval)
# Metodo: Test de la tarea
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 test_interpretacion.py <f_gold> <f_resultados>")
	exit()

# Parametros
f_gold = sys.argv[1]
f_res = sys.argv[2]

# Diccionario con los resultados f_gold
f = open(f_gold,"r")
datos_gold = f.read().split("\n")[:-1]
f.close()
dic_gold = {}
for d in datos_gold:
	datos = d.split("\t")
	dic_gold[datos[0]] = (datos[1].split(";"),datos[2].split(";"))

# Diccionario con los resultados obtenidos
f = open(f_res,"r")
datos_res = f.read().split("\n")[:-1]
f.close()
dic_res = {}
for d in datos_res:
	datos = d.split("\t")
	dic_res[datos[0]] = (datos[1],datos[2])


# cont = 0

# Resultados
aciertos = 0
errores = 0
for k in dic_res:
	datos_gold = dic_gold[k]
	l_s1 = datos_gold[0]
	l_s2 = datos_gold[1]
	s1 = dic_res[k][0]
	s2 = dic_res[k][1]
	if s1 in l_s1 and s2 in l_s2:
		aciertos += 1
	elif s2 in l_s1 and s1 in l_s2:
		aciertos += 1
	else:
		errores += 1

# Estadisticas
total = 389 # Dev
#total = 909 # Test
#total = len(dic_gold) # Corpus completo
analizadas = len(dic_res)
c = round(analizadas/total,4)
p = round(aciertos/analizadas,4)
r = round(aciertos/total,4)
print (aciertos,errores)
f1 = round((2*p*r)/(p+r),4)
print ("----------------------------------")
print ("RESULTADOS:")
print ("----------------------------------")
print ("Coverage:",c)
print ("Precision:",p)
print ("Recall:",r)
print ("F1:",f1)
print ("----------------------------------")
print ("Sentencias analizadas:",analizadas)
print ("Sentencias tarea:",total)

