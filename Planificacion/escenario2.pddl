

; ----------------------------------------------
; AUTOR: Pascual Andres Carrasco Gomez
; ASIGNATURA: TIA
; PRACTICA: 4 - Planificacion
; ----------------------------------------------


; Nombre del problema
(define (problem escenario2)

; Dominio al que corresponde
(:domain robots-cajas)

; Objetos definidos en el problema
(:objects
	robot1 - robot
	robot2 - robot
	caja1 - caja
	caja2 - caja
	caja3 - caja
	habitacion1 - habitacion
	habitacion2 - habitacion
	habitacion3 - habitacion
	habitacion4 - habitacion
	habitacion5 - habitacion
	habitacion6 - habitacion
	habitacion7 - habitacion
	habitacion8 - habitacion
	habitacion9 - habitacion
	habitacion10 - habitacion
	habitacion11 - habitacion
	habitacion12 - habitacion
	habitacion13 - habitacion)

; Parametros iniciales
(:init
	(esta robot1 habitacion1)
	(esta robot2 habitacion1)
	(esta caja1 habitacion8)
	(esta caja2 habitacion13)
	(esta caja3 habitacion6)
	(libre robot1)
	(libre robot2)
	(puerta habitacion1 habitacion2)
	(puerta habitacion2 habitacion1)
	(puerta habitacion2 habitacion4)
	(puerta habitacion3 habitacion5)
	(puerta habitacion3 habitacion9)
	(puerta habitacion4 habitacion2)
	(puerta habitacion4 habitacion5)
	(puerta habitacion4 habitacion7)
	(puerta habitacion5 habitacion3)
	(puerta habitacion5 habitacion4)
	(puerta habitacion5 habitacion6)
	(puerta habitacion6 habitacion5)
	(puerta habitacion7 habitacion4)
	(puerta habitacion8 habitacion11)
	(puerta habitacion9 habitacion3)
	(puerta habitacion9 habitacion10)
	(puerta habitacion9 habitacion12)
	(puerta habitacion10 habitacion9)
	(puerta habitacion10 habitacion13)
	(puerta habitacion11 habitacion8)
	(puerta habitacion11 habitacion12)
	(puerta habitacion12 habitacion9)
	(puerta habitacion12 habitacion11)
	(puerta habitacion13 habitacion10)
	(= (velocidad robot1) 1)
	(= (velocidad robot2) 2)
	(= (hab-visitadas) 0)
	(= (tiempo-cargar-caja) 3)
	(= (tiempo-descargar-caja) 2)
	(= (mover-robot-caja) 3)
	(= (mover-robot-sin-caja) 2))

; Objetivo
(:goal (and (esta robot1 habitacion1)
			(esta robot2 habitacion1)
			(esta caja1 habitacion7)
			(esta caja2 habitacion8)
			(esta caja3 habitacion10)
			))

; Funcion a minimizar
(:metric minimize (+ (* 2 (total-time)) (* 0.02 (hab-visitadas))))

)
