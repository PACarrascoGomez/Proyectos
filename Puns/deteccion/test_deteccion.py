import sys

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Evaluacion Deteccion de puns (tarea 7.1 Semeval)
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Parametros
if len(sys.argv) != 3:
	print ("Uso: python3 test_deteccion.py <f_gold> <f_resultados>")
	sys.exit(1)

# Cargamos los resultados de referencia (gold)
f = open(sys.argv[1],"r")
texto = f.read()
f.close()
l_gold = texto.split("\n")
l_gold = l_gold[0:len(l_gold)-1]
dic_gold = {}
for aux in l_gold:
	id_gold = aux.split("\t")[0]
	y  = aux.split("\t")[1]
	dic_gold[id_gold] = y

# Cargamos los resultados propios obtenidos
f = open(sys.argv[2],"r")
texto = f.read()
f.close()
l_res = texto.split("\n")
l_res = l_res[0:len(l_res)-1]
dic_res = {}
for aux in l_res:
	id_res = aux.split("\t")[0]
	y = aux.split("\t")[1]
	dic_res[id_res] = y

# Realizamos la evaluacion
# Suponemos coverage = 1.0
vp = 0
fp = 0
vn = 0
fn = 0
total = 0
for k in dic_res:
	gold = dic_gold[k]
	res = dic_res[k]
	if gold == "1":
		if res == "1":
			vp += 1
		else:
			fn += 1
	else:
		if res == "0":
			vn += 1
		else:
			fp += 1
	total += 1

print ("VP:",vp)
print ("FN:",fn)
print ("VN:",vn)
print ("FP:",fp)
p = float(vp)/(vp+fp)
r = float(vp)/(vp+fn)
a = float(vp+vn)/(vp+vn+fp+fn)
f1 = (2*p*r)/(p+r)
print ("--------------------------------")
print ("Precision:",p)
print ("Recall:",r)
print ("Accuracy:",a)
print ("F1-score:",f1)
print ("--------------------------------")
print ("Total:",total)