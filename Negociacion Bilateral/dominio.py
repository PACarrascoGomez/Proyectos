
###########################################################
# Autor: Pascual Andres Carrasco Gomez
# Asignatura: Sistemas multiagente (SMA)
# Trabajo: Entorno de negociacion automatica bilateral
# Descripcion: Definicion del dominio del problema
# Dominio: Compra/Venta de portatil
# Lenguaje: python2.7
###########################################################

# Definicion del dominio
def dominio():

	# Definimos los tipos de atributos
	tipos = ["list","list","list","int","float","list"]

	# Definimos los valores que pueden tomar los atributos dentro del dominio
	RAM = [2,4,8,16,32,64]
	HDD = [120,240,500,750,1000,2000]
	pulgadas = [10.1,11.6,13.3,14.0,15.6,17.3]
	peso = 5 # Cota superior
	precio = (RAM[len(RAM)-1]*HDD[len(HDD)-1])/100.0 # Cota superior
	color = ["negro","azul","blanco","rojo","plata"]

	# Devolvemos el dominio
	return [tipos,[RAM,HDD,pulgadas,peso,precio,color]]