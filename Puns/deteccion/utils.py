import xml.etree.ElementTree as ET
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
import stopwords_544 as mas_stopwords
from scipy.spatial import distance
from gensim.models import KeyedVectors
from gensim.models import Word2Vec as w2v
import math
import os
import pickle
import random
from pywsd import disambiguate

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Funciones auxiliares
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

# Obtener stopwords
# Frases = Frases origniales
def obtener_stopwords(frases):
	# stopwords del ingles
	set_aux1 = set(stopwords.words('english'))
	set_aux2 = set(mas_stopwords.lista_stopwords())
	set_stopwords = set_aux1 | set_aux2
	for k in frases: # Insertamos las palabras de len == 1 como stopwords
		for p in frases[k].split(" "):
			if len(p) == 1:
				set_stopwords.add(p.lower())
	return set_stopwords

# Elimina stopwords, numeros, minusculas...
def tokenizar(frase,stopwords):
	res = []
	palabras = frase.split(" ")
	for palabra in palabras:
		p = palabra.lower()
		if p not in stopwords and not(p.isnumeric()):
			res.append(p)
	return res

# Cargar frases desde el xml
# Eda -> Diccionario: key --> id_frase; value --> frase
def cargar_frases(f_xml):
	frases = {}
	tree = ET.parse(f_xml)
	root = tree.getroot()
	for texto in root:
		id_text = texto.attrib['id']
		f = ""
		for palabra in texto:
			f += palabra.text + " "
		f = f[:-1] # Quitar el ultimo espacio
		frases[id_text] = f
	return frases

# Cargar frases desde un txt
# Eda -> Diccionario: key --> id_frase; value --> frase
def cargar_frases_txt(f_txt):
	frases = {}
	f = open(f_txt,"r")
	lineas = f.read().split("\n")[:-1]
	f.close()
	for l in lineas:
		data = l.split("\t")
		frases[data[0]] = data[1]
	return frases

# Cargar puns desde el xml
# Eda -> Diccionario: key --> id_frase; value --> pun
def cargar_puns(f_xml):
	puns = {}
	tree = ET.parse(f_xml)
	root = tree.getroot()
	for texto in root:
		id_texto = texto.attrib['id']
		f_or = ""
		for palabra in texto:
			if palabra.attrib['senses'] == "2":
				id_pun = palabra.attrib['id']
				pun = palabra.text
				puns[id_texto] = pun
	return puns

# Carga los puns de la subtarea 2 (localizacion)
def cargar_puns_subtask2(f_xml,f_gold):
	# EDA fichero gold
	f = open(f_gold,"r")
	data = f.read().split("\n")[:-1]
	f.close()
	dic_gold = {}
	for l in data:
		aux_data = l.split("\t")
		dic_gold[aux_data[0]] = aux_data[1]
	# EDA resultante
	puns = {}
	tree = ET.parse(f_xml)
	root = tree.getroot()
	for texto in root:
		id_text = texto.attrib['id']
		id_pun = dic_gold[id_text]
		for palabra in texto:
			if palabra.attrib['id'] == id_pun:
				puns[id_text] = palabra.text.lower()
	return puns

# Cargar los puns de la subtarea 3 (interpretacion)
def cargar_puns_subtask3(f_xml):
	# EDA resultante
	puns = {}
	tree = ET.parse(f_xml)
	root = tree.getroot()
	for texto in root:
		id_text = texto.attrib['id']
		for palabra in texto:
			if palabra.attrib['senses'] == "2":
				puns[id_text] = palabra.text.lower()
	return puns

# Cargar el codigo de los puns de la subtarea 3 (interpretacion)
def cargar_codigo_puns_subtask3(f_xml):
	# EDA resultante
	puns = {}
	tree = ET.parse(f_xml)
	root = tree.getroot()
	for texto in root:
		id_text = texto.attrib['id']
		for palabra in texto:
			if palabra.attrib['senses'] == "2":
				puns[id_text] = palabra.attrib['id']
	return puns

# Cargamos la informacion del xml --> Frases tokenizadas
# Eda -> Diccionario: key --> id_frase ; value --> frase tokenizada
def tokenizar_frases(frases,stopwords):
	frases_t = {}
	for k in frases:
		id_f = k
		f_t = tokenizar(frases[k],stopwords)
		frases_t[id_f] = f_t
	return frases_t

# Cargar el modelo word2vec
def cargar_modelo_w2v(w2vFile):
	#model_w2v = w2v.load(w2vFile)
	#model_w2v = w2v.load_word2vec_format(w2vFile, binary=True)
	model_w2v = KeyedVectors.load_word2vec_format(w2vFile, binary=True)
	return model_w2v

# Calcula el rango intercuartilico (IQR)
def IQR(scores):
	scores_ord = sorted(scores)
	n = len(scores)
	cuartil_1 = scores_ord[round((n+1)/4)-1]
	cuartil_3 = scores_ord[round((3*(n+1))/4)-1]
	iqr = cuartil_3 - cuartil_1
	return iqr

# Devuelve el nombre de los lemmas de los sentidos especificados como parametro
def obtener_lemmas(sentidos):
	lemmas = set()
	for s in sentidos:
		for l in s.lemmas():
			lemmas.add(l.name())
	return lemmas

# Devuelve el codigo de los lemmas de los sentidos especificados como parametro
def obtener_codigo_lemmas(sentidos):
	lemmas = set()
	for s in sentidos:
		for l in s.lemmas():
			lemmas.add(l)
	return lemmas

# Obtiene la key del sentido especificado
def obtener_key_sentido(sentido):
	return sentido.lemmas()[0].key()

# Devuelve la distancia coseno entre dos palabras utilizando embeddings
def distancia_coseno(p1,p2,m_w2v):
	d_cos = None
	if p1 in m_w2v and p2 in m_w2v:
		d_cos = distance.cosine(m_w2v[p1],m_w2v[p2])
	return d_cos

# Nos devuelve si las dos palabras son contiguas en la frase
def contiguas(p1,p2,frase):
	frase_m = frase.lower().split(" ")
	i1 = frase_m.index(p1)
	i2 = frase_m.index(p2)
	if math.fabs(i1-i2) == 1:
		return True
	else:
		return False

# Metrica basandonos en los lemas de los sentidos del par de palabras
def metrica_sentidos(p1,p2,m_w2v):
	s1 = wn.synsets(p1)
	s2 = wn.synsets(p2)
	l1 = list(obtener_lemmas(s1))
	l2 = list(obtener_lemmas(s2))
	min_d_cos = float("Inf")
	for l1_i in l1:
		for l2_i in l2:
			d_cos = distancia_coseno(l1_i,l2_i,m_w2v)
			if d_cos != None:
				if d_cos < min_d_cos:
					min_d_cos = d_cos
	return min_d_cos

# Pondera una palabra respecto a su posicion en la frase
def posicion_palabra_frase(p,palabras_frase):
	return palabras_frase.index(p)

# Ponderar distancias segun la posicion de la palabra en la frase
# Nota: La palabra es la de la posicion derecha del par de palabras
def ponderar_distancia(p,distancia,palabras_frase):
	wd = 0.3 # Ponderacion distancia
	wp = 0.7 # Ponderacion posicion palabra
	pos = palabras_frase.index(p)
	n_palabras = len(palabras_frase)
	w = ((n_palabras-pos)+1)/n_palabras
	d_ponderada = (wp*w)+(wd*distancia)
	return d_ponderada

# Devuelve el conjunto de hiperonimos de los sentidos especeficiados
def hiperonimos(sentidos):
	res_h = set()
	for s in sentidos:
		h = s.hypernyms()
		h = obtener_lemmas(h)
		res_h = res_h | h
	return res_h

# Devuelve el conjunto de hiponimos de los sentidos especeficiados
def hiponimos(sentidos):
	res_h = set()
	for s in sentidos:
		h = s.hyponyms()
		h = obtener_lemmas(h)
		res_h = res_h | h
	return res_h

# Obtener sinonimos a partir de la categoria gramatical
def son_sinonimos(p1,categoria1,p2,categoria2):
	if categoria1 != categoria2:
		return False
	else:
	 s1 = wn.synsets(p1,pos=categoria1)
	 lemas1 = obtener_lemmas(s1)
	 s2 = wn.synsets(p2,pos=categoria2)
	 lemas2 = obtener_lemmas(s2)
	 intersec = lemas1 & lemas2
	 if len(intersec) != 0:
	 	return True
	 else:
	 	return False

# pos_tagger stanford
def pos_tagger(frase):
	f = open("input_tagger.txt","w")
	f.write(frase)
	f.close()
	ruta = os.popen("pwd").read().split("\n")[0]
	ruta = ruta + "/"
	aux = os.popen("../ejecutar_pos_stanford.sh " + ruta + "input_tagger.txt " + ruta + "output_tagger.txt").read()
	tag = os.popen("cat output_tagger.txt").read().split("\n")[:-1]
	os.system("rm input_tagger.txt output_tagger.txt")
	return tag

# Convierte el formato Penn Treebank al formato utilizado en Wordnet
def pennTreebank_to_wordnet(categoria):
	cat_wn = None
	if categoria[:2] == "NN": #nombre
		cat_wn = 'n'
	elif categoria[:2] == "JJ": #adjetivo
		cat_wn = 'a'
	elif categoria[:2] == "VB": #verbo
		cat_wn = 'v'
	elif categoria[:2] == "RB": #adverbio
		cat_wn = 'r'
	else: # Otra categoria
		cat_wn = 'o'
	return cat_wn

# Devuelve una EDA (diccionario) con el resultado del tagger estructurado
# Frase_tagger: Puede ser mas de una sentencia separada por un punto
def estructurar_tag(frase_tagger):
	dic_palabra_categoria = {}
	for f in frase_tagger:
		tokens = f.split(" ")
		for t in tokens:
			data = t.split("/")
			palabra = data[0].lower()
			categoria = pennTreebank_to_wordnet(data[1])
			dic_palabra_categoria[palabra] = categoria
	return dic_palabra_categoria
	
def propiedades_similares(p1,categoria1,p2,categoria2):
	s1 = wn.synsets(p1)
	s2 = wn.synsets(p2)
	inter1 = hiperonimos(s1) & hiponimos(s2)
	inter2 = hiperonimos(s2) & hiponimos(s1)
	if len(inter1) != 0 or len(inter2) != 0 or son_sinonimos(p1,categoria1,p2,categoria2):
		return True
	else:
		return False

# Genera una estructura de datos para almacenar los resultados de aplicar el tagger sobre las frases
# Para evitar cada vez el coste computacional que ello conlleva (unos 40 min)
# EDA: diccionario --> key:id_frase; value:(diccionario --> key:palabra; value:categoria)
def generar_EDA_frases_tagged(frases):
	frases_tag = {}
	for k in frases:
		f = frases[k]
		f_tag = pos_tagger(f)
		frases_tag[k] = f_tag
	f = open("dic_frases_tag","wb")
	pickle.dump(frases_tag,f,2)
	f.close()

# Carga la EDA generada por "generar_EDA_frases_tagged(frases)"
def cargar_EDA_frases_tagged(f_pickle):
	f = open(f_pickle,"rb")
	dic = pickle.load(f)
	f.close()
	return dic

# A partir de un fichero .txt carga el modelo glove
def cargar_modelo_glove(gloveFile):
    f = open(gloveFile,'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    return model

# Devuelve un diccionario con la probabilidad de categoria
def prob_categoria():
	dic_cat = {}
	dic_cat["n"] = 0.5009
	dic_cat["a"] = 0.1301
	dic_cat["v"] = 0.3454
	dic_cat["r"] = 0.0174
	dic_cat["o"] = 0.0062
	return dic_cat

# Metrica basada en la distancia del par de palabras y posicion de la palabra derecha del par
def metrica_sentidos_posicion(p,d,palabras_frase_tok):
	# Ponderacion segun la posicion
	pos = palabras_frase_tok.index(p)
	n_palabras = len(palabras_frase_tok)
	w = ((n_palabras-pos)+1)/n_palabras
	# Nueva distancia
	d_res = d*w
	return d_res

# Metrica basada en la posicion y la categoria de la palabra
def metrica_posicion_categoria(p,categoria,palabras_frase_tok):
	# Ponderacion segun la posicion
	pos = palabras_frase_tok.index(p)
	n_palabras = len(palabras_frase_tok)
	w = ((n_palabras-pos)+1)/n_palabras
	# Ponderacion segun la categoria
	dic_cat = prob_categoria()
	prob_cat = dic_cat[categoria]
	return w*(1-prob_cat)

# Diccionario con key id_frase y con value (1) si es pun o (0) si no
def y_tarea_deteccion(f_gold):
	f = open(f_gold,"r")
	lineas = f.read().split("\n")[:-1]
	f.close()
	dic = {}
	for l in lineas:
		data = l.split("\t")
		dic[data[0]] = int(data[1])
	return dic

# Particiona el corpus en las tareas: localizacion e interpretacion
# Baraja los frases del corpus
# Utiliza una semilla para que el resultado sea determinista
# 30% train 70% test
def particionar_corpus(frases):
	# Lista de frases ordenadas por el id_texto
	lista_frases = []
	l_aux_keys = []
	for k in frases:
		n_key = int(k.split("_")[1])
		l_aux_keys.append(n_key)
	l_aux_keys_ord = sorted(l_aux_keys)
	for k_ord in l_aux_keys_ord:
		key = "hom_"+str(k_ord)
		lista_frases.append(frases[key])
	# Diccionario invertido de frases
	dic_inv_frases = {}
	for k in frases:
		dic_inv_frases[frases[k]] = k
	# Establecemos la semilla para siempre obtener los mismos resultados
	random.seed(5)
	# Mezclamos la lista de frases
	random.shuffle(lista_frases)
	# Separamos el dev y test
	n_dev = round(len(frases)*30/100) # 30% dev
	l_dev = lista_frases[:n_dev]
	l_test = lista_frases[n_dev:]
	# Convertimos la lista a diccionario para mantener las estructuras con las que trabajamos
	frases_dev = {}
	for f in l_dev:
		frases_dev[dic_inv_frases[f]] = f
	frases_test = {}
	for f in l_test:
		frases_test[dic_inv_frases[f]] = f
	# Retornamos la particion
	return (frases_dev,frases_test)

# Aplica la herramienta PYWSD sobre una frase y devuelve el sentido de la palabra especifada por parametro
def sentido_PYWSD(palabra,frase):
	frase_wsd = disambiguate(frase)
	for r in frase_wsd:
		if r[0] == palabra:
			if not(r[1] is None):
				sentido = r[1]
				return (sentido,True)
	return (None,False)

