/*
	AUTOR: Pascual Andres Carrasco Gomez
	Practica: Jess (Parte 1)
	Descripción: Programa para adivinar que animal estamos pensando
	Encadenamiento inferencial: backward
*/

(clear)

(do-backward-chaining cubre)
(do-backward-chaining reproduce)
(do-backward-chaining pico)
(do-backward-chaining vuela)
(do-backward-chaining nada)
(do-backward-chaining color)
(do-backward-chaining rayas)
(do-backward-chaining piel)
(do-backward-chaining come)
(do-backward-chaining garras)
(do-backward-chaining da_leche)

; REGLA INICIAL
(defrule inicio
	(nombre ?nombre)
=>
    (printout t "El nombre del animal es: " ?nombre crlf) 
    (halt) ; cuando encuentra el primer objetivo finaliza
)


; REGLAS CONOCIMIENTO
(defrule es_tipo_mamifero_1
	(cubre ?cubre)
    (test (eq ?cubre pelo))
=>
    (assert (tipo mamifero))
)

(defrule es_tipo_ave_1
	(cubre ?cubre)
    (test (eq ?cubre plumas))
    (reproduce ?reproduce)
    (test (eq ?reproduce oviparo))
=>
    (assert (tipo ave))    
)

(defrule alimenta_carnivoro
	(tipo mamifero)
    (come ?come)
    (test (eq ?come carne))
    (garras ?garras)
    (test (eq ?garras si))
=>
    (assert (alimenta carnivoro))    
)

(defrule es_un_guepardo
	(alimenta carnivoro)
    (color ?color)
    (test (eq ?color pardo))
    (piel ?piel)
    (test (eq ?piel manchas))
=>
    (assert (nombre guepardo))    
)

(defrule es_un_tigre
	(alimenta carnivoro)
    (color ?color)
    (test (eq ?color pardo))
    (rayas ?rayas)
    (test (eq ?rayas negras))
=>
    (assert (nombre tigre))    
)

(defrule es_un_pinguino
	(tipo ave)
    (vuela ?vuela)
    (test (eq ?vuela mal))
    (nada ?nada)
    (test (eq ?nada bien))
=>
    (assert (nombre pinguino))    
)

(defrule es_una_gaviota
	(tipo ave)
    (vuela ?vuela)
    (test (eq ?vuela muy_bien))
=>
    (assert (nombre gaviota))    
)

(defrule es_tipo_mamifero_2
	(da_leche ?da_leche)
    (test (eq ?da_leche si))
=>
    (assert (tipo mamifero))    
)

(defrule es_tipo_ave_2
	(pico ?pico)
    (test (eq ?pico si))
    (reproduce ?reproduce)
    (test (eq ?reproduce oviparo))
=>
    (assert (tipo ave))
)

; PREGUNTAS AL USUARIO
(defrule preguntar-cubre
	(need-cubre ?)    
=>
    (printout t "Cubre: (plumas|pelo|vacio)" crlf)
    (assert (cubre (read)))
)

(defrule preguntar-reproduce
	(need-reproduce ?)    
=>
    (printout t "Reproduce: (oviparo|vacio)" crlf)
    (assert (reproduce (read)))
)

(defrule preguntar-pico
	(need-pico ?)    
=>
    (printout t "Pico: (si|no)" crlf)
    (assert (pico (read)))
)

(defrule preguntar-vuela
	(need-vuela ?)    
=>
    (printout t "Vuela: (mal|muy_bien|vacio)" crlf)
    (assert (vuela (read)))
)

(defrule preguntar-nada
	(need-nada ?)    
=>
    (printout t "Nada: (bien|vacio)" crlf)
    (assert (nada (read)))
)

(defrule preguntar-color
	(need-color ?)    
=>
    (printout t "Color: (pardo|vacio)" crlf)
    (assert (color (read)))
)

(defrule preguntar-rayas
	(need-rayas ?)    
=>
    (printout t "Rayas: (negras|vacio)" crlf)
    (assert (rayas (read)))
)

(defrule preguntar-piel
	(need-piel ?)    
=>
    (printout t "Piel: (manchas|vacio)" crlf)
    (assert (piel (read)))
)

(defrule preguntar-come
	(need-come ?)    
=>
    (printout t "Come: (carne|vacio)" crlf)
    (assert (come (read)))
)

(defrule preguntar-garras
	(need-garras ?)    
=>
    (printout t "Garras: (si|no)" crlf)
    (assert (garras (read)))
)

(defrule preguntar-da_leche
	(need-da_leche ?)    
=>
    (printout t "Da leche: (si|no)" crlf)
    (assert (da_leche (read)))
)

;(watch all)
(reset)
(run)