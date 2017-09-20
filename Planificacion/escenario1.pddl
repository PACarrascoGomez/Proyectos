

; ----------------------------------------------
; AUTOR: Pascual Andres Carrasco Gomez
; ASIGNATURA: TIA
; PRACTICA: 4 - Planificacion
; ----------------------------------------------


; Nombre del problema
(define (problem escenario1)

; Dominio al que corresponde
(:domain robots-cajas)

; Objetos definidos en el problema
(:objects
	robot1 - robot
	caja1 - caja
	habitacion1 - habitacion
	habitacion2 - habitacion
	habitacion3 - habitacion
	habitacion4 - habitacion)

; Parametros iniciales
(:init
	(esta robot1 habitacion1)
	(esta caja1 habitacion4)
	(libre robot1)
	(puerta habitacion1 habitacion2)
	(puerta habitacion2 habitacion1)
	(puerta habitacion2 habitacion3)
	(puerta habitacion3 habitacion2)
	(puerta habitacion3 habitacion4)
	(puerta habitacion4 habitacion3)
	(= (velocidad robot1) 1)
	(= (hab-visitadas) 0)
	(= (tiempo-cargar-caja) 3)
	(= (tiempo-descargar-caja) 2)
	(= (mover-robot-caja) 2)
	(= (mover-robot-sin-caja) 1))

; Objetivo
(:goal (and (esta robot1 habitacion1)
			(esta caja1 habitacion3)))

; Funcion a minimizar
(:metric minimize (+ (* 2 (total-time)) (* 0.02 (hab-visitadas))))

)
