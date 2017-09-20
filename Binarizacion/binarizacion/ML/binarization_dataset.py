import sys, os

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: Binarizar el corpus (competicion)
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# python3 binarization_dataset.py ../../Evaluacion/Dataset/Originals/ model_svm ../../Evaluacion/Salida/

# Comprobacion de parametros
if len(sys.argv) != 4:
	print ("Uso: python3 binarization_dataset.py <dir_img_originales> <modelo> <dir_out>")
	exit()

# Parametros
dir_in = sys.argv[1]
modelo = sys.argv[2]
dir_out = sys.argv[3]

# Lista de nombre de imagenes a binarizar
l_img = os.popen("ls " + dir_in).read().split("\n")[:-1]

# Realizamos la binarizacion
for n_f in l_img:
	n_f_out = n_f.split(".")[0]+".out."+n_f.split(".")[1]
	print (n_f_out)
	# aux = os.popen("python3 binarization_mlp.py " + dir_in + n_f + " " + modelo + " " + dir_out + n_f_out + " 3").read()
	aux = os.popen("python3 binarization.py " + dir_in + n_f + " " + modelo + " " + dir_out + n_f_out + " 3").read()