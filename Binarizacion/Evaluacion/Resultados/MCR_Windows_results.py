import sys, os

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Obtener resultados Metrica competicion
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 MCR_Windows_results.py <f_lista_salida_gt> <f_out>")
	exit()

# Parametros
f_in = sys.argv[1]
f_out = sys.argv[2]

# Obtenemos el nombre de las imagenes
data = os.popen("type " + f_in).read().split("\n")[:-1]
l_img_res = []
l_img_gt = []
for d in data:
	aux = d.split("\t")
	l_img_res.append(aux[1])
	l_img_gt.append(aux[0])

# Fichero de salida
file_out = open(f_out,"w")

# Obtenemos los resultados
a = 0.0
b = 0.0
c = 0.0
d = 0.0
e = 0.0
f = 0.0
g = 0.0
h = 0.0
cont = 0
for i in range(0,len(l_img_res)):
	# Obtenemos la imagen correspondiente GT
	f_res = l_img_res[i].replace("/","\\")
	f_gt = l_img_gt[i].replace("/","\\")
	print (f_res,f_gt)
	# Obtenemos los ficheros de pesos
	# aux = os.popen("BinEvalWeights\BinEvalWeights.exe " + f_gt).read()
	# Ruta de los ficheros de pesos
	ruta = "Dataset\GT\\"
	r_weights = ruta + f_gt.split("\\")[-1].split(".bmp")[0] + "_RWeights.dat"
	p_weights = ruta + f_gt.split("\\")[-1].split(".bmp")[0] + "_PWeights.dat"
	results = os.popen("HDIBCO14-metrics_incl-TIPmetrics\DIBCO13_metrics.exe " + f_gt + " " + f_res + " " + r_weights + " " + p_weights).read()
	file_out.write(f_res.split("\\")[-1] + "\t" + results)
	data = results.split("\t")
	a += float(data[0])
	b += float(data[1])
	c += float(data[2])
	d += float(data[3])
	e += float(data[4])
	f += float(data[5])
	g += float(data[6])
	h += float(data[7])
	cont += 1

file_out.write("-------------------------------------------------------------------------------------------------------------------\n")
file_out.write("RESULTADO\n")
file_out.write("-------------------------------------------------------------------------------------------------------------------\n")
file_out.write("MEDIA:\t" + str(a/cont) + "\t" + str(b/cont) + "\t" + str(c/cont) + "\t" + str(d/cont) + "\t" + str(e/cont) + "\t" + str(f/cont) + "\t" + str(g/cont) + "\t" + str(h/cont) + "\n")

# Cerramos el fichero de salida
file_out.close()