from keras.models import Sequential
from keras.layers import Dense, noise, Activation
from keras.utils.np_utils import to_categorical
import sys, os
import numpy as np
from random import shuffle
import h5py
import cPickle as pickle

######################################################
# Autor: Pascual Andres Carrasco Gomez
# 
# Requerimientos:
#	pip install h5py
#	apt-get install python-numpy python-scipy python-dev python-pip python-nose g++ libopenblas-dev git
#	pip install Theano
#	pip install keras
#	pip install tensorflow
######################################################

# Parametros
if len(sys.argv) != 3:
	print "Uso: python2 caras_neuronal.py <f_caras> <f_no_caras>"
	sys.exit(1)

# Cargamos las imagenes correspondientes a caras y no caras
f = file(sys.argv[1],"rb")
l_imagenes_caras = pickle.load(f)
f.close()
f = file(sys.argv[2],"rb")
l_imagenes_no_caras = pickle.load(f)
f.close()

# Convertimos a listas
aux_l_caras = l_imagenes_caras.tolist()
aux_l_no_caras = l_imagenes_no_caras.tolist()

# Asignamos la clase
l_caras = []
l_no_caras = []
for i in range(0,len(aux_l_caras)):
	l_caras.append((aux_l_caras[i],1))
for i in range(0,len(aux_l_no_caras)):
	l_no_caras.append((aux_l_no_caras[i],0))

# Separamos el test del train (caras)
# test = 20% de train
s_test = len(l_caras)*20/100
datos_test = l_caras[0:s_test/2]
l_caras = l_caras[s_test/2:len(l_caras)]
datos_test = datos_test + l_no_caras[0:s_test/2]
l_no_caras = l_no_caras[s_test/2:len(l_no_caras)]

# Barajamos los datos
datos_train = l_caras + l_no_caras
shuffle(datos_train)
shuffle(datos_test)

# Obtenemos el vector de train y sus respectivas clases
x_train = []
y_train = []
for i in range(0,len(datos_train)):
	x_train.append(datos_train[i][0])
	y_train.append(datos_train[i][1])

# Obtenemos el vector de test y sus respectivas clases
x_test = []
y_test = []
for i in range(0,len(datos_test)):
	x_test.append(datos_test[i][0])
	y_test.append(datos_test[i][1])

# Convierte los vectores en matrices binarias (para clasificacion)
y_test2 = y_test
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#----------------------------------------------------
# Estructura de la red
#----------------------------------------------------
model = Sequential()
model.add(Dense(64, init='uniform', input_shape=(len(x_train[0]),)))
model.add(noise.GaussianNoise(0.5))
model.add(Activation('relu'))
model.add(Dense(32, init='uniform'))
model.add(Activation('relu'))
model.add(Dense(2, init='uniform'))
model.add(Activation('softmax'))

#----------------------------------------------------
# Parametros
#----------------------------------------------------
model.compile(loss='categorical_crossentropy',
              optimizer='adadelta',
              metrics=['accuracy'])


print "----------------------------------------------------"
print "Training"
print "----------------------------------------------------"
model.fit(np.array(x_train), np.array(y_train),
          nb_epoch=2,
          batch_size=500)

print "----------------------------------------------------"
print "Evaluation"
print "----------------------------------------------------"
score = model.evaluate(np.array(x_test), np.array(y_test), batch_size=500)
print "\n"
print "loss: ",score[0]
print "accuracy: ",score[1]

# Almacenamos el modelo entrenado
model.save("modelo.h5")

# Evaluacion
vp = 0
vn = 0
fp = 0
fn = 0
total_caras = 0
total_no_caras = 0
for i in range(0,len(x_test)):
	clase = model.predict_classes(np.array([x_test[i]]),batch_size=100)
	if y_test2[i] == 1:
		total_caras += 1
		if clase == 1:
			vp += 1
		else:
			fp += 1
	else:
		total_no_caras += 1
		if clase == 0:
			vn += 1
		else:
			fn += 1

# Resultados
print "-----------------------------------"
print "\t\tRESULTADOS"
print "-----------------------------------"
print "Verdaderos positivos (VP): ",vp
print "Falsos positivos (FP): ",fp
print "Verdaderos negativos (VN)",vn
print "Falsos negativos (FN)",fn
print "Caras analizadas: ", total_caras
print "No caras analizadas: ", total_no_caras
print "-----------------------------------"


