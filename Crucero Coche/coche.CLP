
;	Autor: Pascual Andres Carrasco Gomez
;	Practica: 2 (Fuzzy-clips)
;	Sistema: Control de crucero de un vehiculo
;	Aplicacion: Logica difusa




; VARIABLES DIFUSAS
(deftemplate distancia
	0 50 metros
	((cerca (0 1) (15 0))
	(medio (10 0) (25 1) (35 1) (40 0))
	(lejos (35 0) (50 1)))
)

(deftemplate velocidad-relativa
	-30 30 kmh
	((alejando (-30 1) (0 0))
	(constante (-10 0) (0 1) (10 0))
	(acercando (0 0) (30 1)))
)

(deftemplate presion_freno
	0 100 %
	((nula (z 10 25))
	(media (pi 25 65))
	(alta (s 65 90)))
)

; HECHOS INICIALES
(deffacts datos
	(pregunta1 si)
	(pregunta2 si)
)

; REGLAS
(defrule R1
	(declare (salience 100))
	(distancia cerca)
	(velocidad-relativa alejando) 
=>
	(assert (presion_freno nula))
)

(defrule R2
	(declare (salience 100))
	(distancia cerca)
	(velocidad-relativa constante)
=>
	(assert (presion_freno media))
)

(defrule R3
	(declare (salience 100))
	(distancia cerca)
	(velocidad-relativa acercando)
=>
	(assert (presion_freno alta))
)

(defrule R4
	(declare (salience 100))
	(distancia medio)
	(velocidad-relativa alejando)
=>
	(assert (presion_freno nula))
)

(defrule R5
	(declare (salience 100))
	(distancia medio)
	(velocidad-relativa constante)
=>
	(assert (presion_freno nula))
)

(defrule R6
	(declare (salience 100))
	(distancia medio)
	(velocidad-relativa acercando)
=>
	(assert (presion_freno media))
)

(defrule R7
	(declare (salience 100))
	(distancia lejos)
	(velocidad-relativa alejando)
=>
	(assert (presion_freno nula))
)

(defrule R8
	(declare (salience 100))
	(distancia lejos)
	(velocidad-relativa constante)
=>
	(assert (presion_freno nula))	
)

(defrule R9
	(declare (salience 100))
	(distancia lejos)
	(velocidad-relativa acercando)
=>
	(assert (presion_freno media))	
)
	
; DEFUSIFICACION
(defrule obtener_presion
	(declare (salience 50))
	(presion_freno ?pf)
=>
	(bind ?aux1 (maximum-defuzzify ?pf))
	(printout t "Criterio-Maximo: La presion a aplicar es :" ?aux1 (get-u-units ?pf) crlf)
	(bind ?aux2 (moment-defuzzify ?pf))
	(printout t "Criterio-Momento: La presion a aplicar es :" ?aux2 (get-u-units ?pf) crlf)
	(bind ?media (/ (+ ?aux1 ?aux2) 2))
	(printout t "Media: La media de los criterios obtenidos es: " ?media (get-u-units ?pf) crlf)
)

; FUNCION FUZZIFY
(deffunction fuzzify (?fztemplate ?value ?delta)
    (bind ?low (get-u-from ?fztemplate))
    (bind ?hi  (get-u-to   ?fztemplate))

    (if (<= ?value ?low)
      then
        (assert-string
          (format nil "(%s (%g 1.0) (%g 0.0))" ?fztemplate ?low ?delta))
      else
        (if (>= ?value ?hi)
          then
            (assert-string
               (format nil "(%s (%g 0.0) (%g 1.0))"
                           ?fztemplate (- ?hi ?delta) ?hi))
          else
            (assert-string
               (format nil "(%s (%g 0.0) (%g 1.0) (%g 0.0))"
                           ?fztemplate (max ?low (- ?value ?delta))
                           ?value (min ?hi (+ ?value ?delta)) ))
        )
    )
)

; INTERACCION USUARIO
(defrule preguntar_distancia
	(declare (salience 1000))
	?p1 <- (pregunta1 si)
=>
	(printout t "Introduzca la distancia en metros ([0 - 50])" crlf)
	(bind ?aux (read))
	(fuzzify distancia ?aux 0)
	(retract ?p1)
)

(defrule preguntar_velocidad
	(declare (salience 1000))
	?p2 <- (pregunta2 si)
=>
	(printout t "Introduzca la velocidad en km/h ([-30 - 30])" crlf)
	(bind ?aux (read))
	(fuzzify velocidad-relativa ?aux 0)
	(retract ?p2)
)

