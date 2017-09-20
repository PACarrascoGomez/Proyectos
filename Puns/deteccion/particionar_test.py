import sys
from utils import *
import pickle

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Deteccion de puns (tarea 7.1 Semeval)
# Metodo: Particiona el test en 3 partes (2*643+321)
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Parametros
if len(sys.argv) != 3:
	print ("Uso: python3 particionar_test.py <fichero_xml> <fichero_gold_xml>")
	sys.exit(1)

# Parametros
f_xml = sys.argv[1]
f_gold_xml = sys.argv[2]

# Cargamos las frases del corpus de test
frases_test = cargar_frases(f_xml)

# Cargamos las salidas de las frases de test
frases_y_test = y_tarea_deteccion(f_gold_xml)

# Creamos un indice invertido de las frases de test
inv_frases_test = {}
for k in frases_test:
	inv_frases_test[frases_test[k]] = k

# Separamos las frases que tengan pun con las que no
l_frases_pun = []
l_frases_no_pun = []
for k in frases_test:
	id_num = int(k.split("_")[1])
	if frases_y_test[k] == 1:
		l_frases_pun.append((id_num,frases_test[k]))
	else:
		l_frases_no_pun.append((id_num,frases_test[k]))

# Ordenamos las frases por su id de menor a mayor para poder trabajar con la semilla (seed)
l_frases_pun_ord = sorted(l_frases_pun)
l_frases_pun = []
for data in l_frases_pun_ord:
	l_frases_pun.append(data[1])
l_frases_no_pun_ord = sorted(l_frases_no_pun)
l_frases_no_pun = []
for data in l_frases_no_pun_ord:
	l_frases_no_pun.append(data[1])

# Barajamos las frases con pun y las frases sin pun con una semilla (seed)
random.seed(5)
random.shuffle(l_frases_pun)
random.shuffle(l_frases_no_pun)

# Separamos las frases que contiene pun en tres particiones (2 para test y 1 para dev)
particion1_test_pun = l_frases_pun[:643] # 643
particion2_test_pun = l_frases_pun[643:(643*2)] # 643
particion_dev_pun = l_frases_pun[(643*2):] # 321
particion_dev_pun = particion_dev_pun[:277] # 277 frases en total

# Particion de frases que no contienen pun
particion_test_no_pun = l_frases_no_pun

# Escribimos las particiones en ficheros
f = open("particion1_test_pun","w")
for frase in particion1_test_pun:
	k = inv_frases_test[frase]
	f.write(str(k) + "\t" + frase + "\n")
f.close()
f = open("particion2_test_pun","w")
for frase in particion2_test_pun:
	k = inv_frases_test[frase]
	f.write(str(k) + "\t" + frase + "\n")
f.close()
f = open("particion_dev_pun","w")
for frase in particion_dev_pun:
	k = inv_frases_test[frase]
	f.write(str(k) + "\t" + frase + "\n")
f.close()
f = open("particion_test_no_pun","w")
for frase in particion_test_no_pun:
	k = inv_frases_test[frase]
	f.write(str(k) + "\t" + frase + "\n")
f.close()
