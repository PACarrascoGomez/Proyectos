import sys
from utils import *
from sklearn.svm import LinearSVC
import pickle

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: SVM
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 train_svm.py ../../DataSet_Propio/train/X/ ../../DataSet_Propio/train/Y/ 3

# Comprobacion de parametros
if len(sys.argv) != 4:
	print ("Uso: python3 train_mlp.py <dir_x_train> <dir_y_train> <size_windows>")
	exit()

# Parametros de entrada
dir_x = sys.argv[1]
dir_y = sys.argv[2]

# Dimension de la ventana de analisis
s_w = int(sys.argv[3])

# Obtenemos x_train e y_train
x_train,y_train = load_data(dir_x,dir_y,s_w)

#------------------------------------------
# MODELO
#------------------------------------------
clf = LinearSVC()

#------------------------------------------
# ENTRENAMIENTO
#------------------------------------------
clf.fit(x_train, y_train)

#------------------------------------------
# Almacenamos el modelo obtenido
#------------------------------------------
f_out = open("model_svm","wb")
pickle.dump(clf,f_out)
f_out.close()
