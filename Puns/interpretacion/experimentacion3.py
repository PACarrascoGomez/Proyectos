import sys
from utils import *
import numpy as np
import nltk

##########################################################
# Autor: Pascual Andres Carrasco Gomez
# Descripcion: Interpretacion de puns (tarea 7.3 Semeval)
# Metodo: Experimentacion3
# Asignatura: Trabajo de final de Master (TFM)
# Entorno: python3
##########################################################

class GetSynsets():
    
    stopwords = nltk.corpus.stopwords.words('english')
    wn = nltk.corpus.wordnet
    wnL = nltk.WordNetLemmatizer
    def tokenize (self, word):
        return nltk.word_tokenize(word)
    def lemmatize(self, word, pos='n'):
        return self.wnL().lemmatize(word, pos)

    def wn_word_definitions(self, word, pos=('v', 'n', 'a', 's', 'r'), verbose=0):
        d = {}
        for synset in self.wn.synsets(word):
            if verbose > 0:
                print (synset)
            lem = []
            de = [word] + self.tokenize(synset.definition())
            for ex in synset.examples():
                de += self.tokenize(ex)
            for lemma in synset.lemma_names():
                de += self.tokenize(' '.join(lemma.split('_')))
            clean_de = [w.lower() for w in de if w.lower() not in self.stopwords]
            if pos is None:
                lem += [wn.morphy(w) for w in clean_de if wn.morphy(w) is not None]
            else:
                for pos in pos: 
                    lem += [self.lemmatize(w, pos=pos) for w in clean_de]
            lem = ' '.join(lem)
            d[synset.name()] = lem
        return d

    def word_intersection(self, sentence1, sentence2, verbose=0):
        d = len(set(sentence1.split()).intersection(sentence2.split()))
        if verbose > 0:
            print (sentence1)
            print (sentence2)
            print (d)
            print ('\n'*3)    
        return d

    def allvsall(self, wnwd1, wnwd2, verbose=1):    
        "wnwd = wordnet word definitions"
        sim = {}
        for syn1 in wnwd1:
            for syn2 in wnwd2:
                d = self.word_intersection(wnwd1[syn1], wnwd2[syn2])
                sim[(syn1, syn2)] = d
        return sim

    def do_all(self, word1, word2, verbose=0):
        if verbose > 1:
            print ("do_all")
            print ("======")
            print ("word1", word1)
            print ("word2", word2)
        wnwd1 = self.wn_word_definitions(word1, verbose=verbose)
        wnwd2 = self.wn_word_definitions(word2, verbose=verbose)
        sim = self.allvsall(wnwd1, wnwd2, verbose=verbose)
        if verbose > 1:
            print (wnwd1)
            print (wnwd2)
        sorted_sim = sorted([(y,x) for x,y in sim.items()], reverse=True)
        if verbose > 0:
            for s, k in sorted_sim[:10]:        
                s1, s2 = k
                print (k, s)
                print (wnwd1[s1])
                print (wnwd2[s2])
                #print ('------')
        return sorted_sim

    def select_best_different(self, word1, word2, word3, verbose=0):
        
        def mec(word, syn):
            return word.startswith(syn.split('%')[0])
        
        s1 = g.do_all(word1, word2, verbose=0)
        s2 = g.do_all(word1, word3, verbose=0)
        if len(s1) == 0 or len(s2) == 0:
            if len(s1) > 0:
                return len(s1), None
            elif len(s2) > 0:
                return None, len(s2)
            else:
                return None, None
        #print ('----')
        all_syn1 = []
        for sn in s1:
            #print (sn[1][0])
            #a = self.wn.synset(sn[1][0])
            #print (dir(self.wn))
            #print (a)
            all_syn1 += [l.key() for l in self.wn.synset(sn[1][0]).lemmas()]
        all_syn2 = []
        for sn in s2:
            #print (sn[1][0])
            #a = self.wn.synset(sn[1][0])
            #print (dir(self.wn))
            #print (a)
            all_syn2 += [l.key() for l in self.wn.synset(sn[1][0]).lemmas()]
        pure_synset1 = [s for s in all_syn1 if mec(word1, s)]
        pure_synset2 = [s for s in all_syn2 if mec(word1, s)]
        
        #print (all_syn1)
        if verbose > 0:
            print ([(sn[1][0], sn[0]) for sn in s1])
            print (pure_synset1)
            print ('\n'*2)
            print (pure_synset2)
        if len(pure_synset1) == 0:
            pure_synset1 = all_syn1
        if len(pure_synset2) == 0:
            if verbose > 1:
                print ('problem')
                for s in all_syn2:
                    print (word1, s)
                    print (s.split('%')[0])
                    print (word1.startswith(s.split('%')[0]))

                print (pure_synset2)
                print (all_syn2)
            pure_synset2 = all_syn2        
        first_synset = pure_synset1[0]
        for second_synset in pure_synset2:
            if first_synset != second_synset:
                break       
        #print (first_synset, second_synset)
        #for while
        return first_synset, second_synset


# Comprobacion de parametros
if len(sys.argv) != 3:
	print ("Uso: python3 experimentacion3.py <fichero_xml> <fichero_out>")
	sys.exit(1)

# Parametros
f_xml = sys.argv[1]
f_out = sys.argv[2]

# Cargamos las frases del corpus
frases = cargar_frases(f_xml)

# Cargamos stopwords
stopwords = obtener_stopwords(frases)

# Particionamos el corpus
(frases_dev,frases_test) = particionar_corpus(frases)
frases = frases_dev

# Tokenizamos las frases
frases_tok = tokenizar_frases(frases,stopwords)

# Cargamos el modelo word2vec
f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/GoogleNews-vectors-negative300.bin'
#f_w2v = '/home/pascu/Escritorio/Experimentacion/modelos_w2v/wikipedia_w2v.bin'
model = cargar_modelo_w2v(f_w2v)

# Cargar puns
puns = cargar_puns_subtask3(f_xml)
puns_codigo = cargar_codigo_puns_subtask3(f_xml)

# Obtenemos las distancia (metrica_sentidos) de las palabras de la sentencia respecto al pun
distancias_metrica_sentidos_frases = {}
for k in frases_tok:
    pun = puns[k]
    palabras = frases_tok[k]
    palabras_frase = []
    for p in frases[k].split(" "):
        palabras_frase.append(p.lower())
    distancias_pares = []
    for p in palabras:
        if p != pun and not(contiguas(p,pun,frases[k])):
            d_min = metrica_sentidos(p,pun,model)
            d_min = ponderar_distancia(pun,d_min,palabras_frase)
            if d_min != float("Inf"):
                distancias_pares.append((d_min,p))
    if len(distancias_pares) > 0:
        distancias_metrica_sentidos_frases[k] = distancias_pares

# Obtenemos las distancia (coseno) de las palabras de la sentencia respecto al pun
distancias_coseno_frases = {}
for k in frases_tok:
    pun = puns[k]
    palabras = frases_tok[k]
    palabras_frase = []
    for p in frases[k].split(" "):
        palabras_frase.append(p.lower())
    distancias_pares = []
    for p in palabras:
        if p != pun and not(contiguas(p,pun,frases[k])):
            d_min = distancia_coseno(p,pun,model)
            if d_min != None:
                distancias_pares.append((d_min,p))
    if len(distancias_pares) > 1:
        distancias_coseno_frases[k] = distancias_pares

# Obtenemos los sentidos
g = GetSynsets()
resultados = {}
for k in distancias_metrica_sentidos_frases:
    if k in distancias_coseno_frases:
        pun = puns[k]
        distancias_metrica_sentidos = distancias_metrica_sentidos_frases[k]
        distancias_metrica_sentidos_ord = sorted(distancias_metrica_sentidos)
        distancias_coseno = distancias_coseno_frases[k]
        distancias_coseno_ord = sorted(distancias_coseno)
        p1 = distancias_metrica_sentidos_ord[0][1]
        p2 = distancias_coseno_ord[0][1]
        if p1 == p2:
            p2 = distancias_coseno_ord[1][1]
        s1, s2 = g.select_best_different(pun, p1, p2)
        if s1 != None and s2 != None:
            resultados[k] = (s1,s2)

# Estadisticas
print ("Frases analizadas:",len(resultados))
print ("Frases totales:",len(frases))

# Escribimos los resultados en el fichero de salida
f = open(f_out,"w")
for k in resultados:
	#print (puns_codigo[k],resultados[k][0],resultados[k][1])
	f.write(puns_codigo[k] + "\t" + resultados[k][0] + "\t" + resultados[k][1] + "\n")
f.close()

