

; ----------------------------------------------
; AUTOR: Pascual Andres Carrasco Gomez
; ASIGNATURA: TIA
; PRACTICA: 4 - Planificacion
; ----------------------------------------------


; Nombre del dominio
(define (domain robots-cajas)

; Se requieren:
;	Acciones durativas
;	Predicados con tipo
;	Funciones numericas
(:requirements :durative-actions :typing :fluents)

; Tipos de objetos
(:types robot caja habitacion - object)

; Predicados
(:predicates (esta ?x - (either robot caja) ?h - habitacion)
             (ocupado ?r - robot ?c - caja)
             (libre ?r - robot)
             (puerta ?h1 - habitacion ?h2 - habitacion))

; Funciones numericas
(:functions 
            (velocidad ?r - robot)
            (hab-visitadas)
            (tiempo-cargar-caja)
            (tiempo-descargar-caja)
			(mover-robot-caja)
            (mover-robot-sin-caja))

; Acciones (Operadores)
(:durative-action coger-caja
 :parameters (?r - robot ?c - caja ?h - habitacion)
 :duration (= ?duration (tiempo-cargar-caja))
 :condition (and (at start (esta ?c ?h))
                 (at start (libre ?r))
                 (over all (esta ?r ?h)))
 :effect (and (at start (not (esta ?c ?h)))
              (at start (not (libre ?r)))
              (at end (ocupado ?r ?c))))

(:durative-action dejar-caja
 :parameters (?r - robot ?c - caja ?h - habitacion)
 :duration (= ?duration (tiempo-descargar-caja))
 :condition (and (at start (ocupado ?r ?c))
                 (over all (esta ?r ?h)))
 :effect (and (at start (not (ocupado ?r ?c)))
              (at end (libre ?r))
              (at end (esta ?c ?h))))

(:durative-action mover-robot-vacio
 :parameters (?r - robot ?ho - habitacion ?hd - habitacion)
 :duration (= ?duration (/ (mover-robot-sin-caja) (velocidad ?r)))
 :condition (and (at start (puerta ?ho ?hd))
                 (at start (esta ?r ?ho))
                 (over all (libre ?r)))
 :effect (and (at start (not (esta ?r ?ho)))
              (at end (esta ?r ?hd))
              (at end (increase (hab-visitadas) 1))))

(:durative-action mover-robot-caja
 :parameters (?r - robot ?c - caja ?ho - habitacion ?hd - habitacion)
 :duration (= ?duration (/ (mover-robot-caja) (velocidad ?r)))
 :condition (and (at start (puerta ?ho ?hd))
                 (at start (esta ?r ?ho))
                 (over all (ocupado ?r ?c)))
 :effect (and (at start (not (esta ?r ?ho)))
              (at end (esta ?r ?hd))
              (at end (increase (hab-visitadas) 1))))

)
