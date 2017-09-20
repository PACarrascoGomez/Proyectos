import sys
from utils import *
from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical

##############################################
# Autor: Pascual Andres Carrasco Gomez
# Metodo: MLP
# Tecnica: Binarizacion (ML)
# Asignatura: Reconocimiento de escritura
##############################################

# Uso: python3 train_mlp.py ../../DataSet_Propio/train/X/ ../../DataSet_Propio/train/Y/ 3

# Comprobacion de parametros
if len(sys.argv) != 4:
	print ("Uso: python3 train_mlp.py <dir_x_train> <dir_y_train> <size_windows>")
	exit()

# Parametros de entrada
dir_x = sys.argv[1]
dir_y = sys.argv[2]

# Dimension de la ventana de analisis
s_w = int(sys.argv[3])

# Tamanyo del batch
s_b = 1024

# Numero de muestras totales
samples = data_size(dir_x,s_w)
spe = round(samples/s_b)

# Dimension de cada muestra
dim = dimension_sample()

#------------------------------------------
# MODELO
#------------------------------------------
model = Sequential()
model.add(Dense(5, activation='relu', input_shape=(dim,)))
model.add(Dense(2, activation='softmax'))

#------------------------------------------
# CONFIGURACION
#------------------------------------------
model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])

#------------------------------------------
# ENTRENAMIENTO
#------------------------------------------
#model.fit(x_train, y_train,
#          epochs=2,
#          batch_size=128)
model.fit_generator(generator_data(dir_x,dir_y,s_w,s_b),
        steps_per_epoch=spe, epochs=1)
#------------------------------------------
# Almacenamos el modelo obtenido
#------------------------------------------
model.save('model_mlp.h5')