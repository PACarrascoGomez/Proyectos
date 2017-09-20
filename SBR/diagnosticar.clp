/*
	AUTOR: Pascual Andres Carrasco Gomez
	Practica: Jess (Parte 2)
	Descripción: Programa que genera un diagnostico a un ordenador domestico
	Encadenamiento inferencial: forward
*/

(clear)

; TEMPLATES
(deftemplate pc
	"Template que define las caracteristicas del PC a diagnosticar"
    (declare (slot-specific TRUE))
    (slot estado); (nuevo | viejo)
    (slot disco_duro); (lento | rapido)
    (slot cpu); (calienta | normal)
    (slot ram); (saturada | normal)
    (slot ruido_ventiladores); (si | no)
    (slot fuente_cortes); (si | no)
    (slot disipador); (falla | normal)
    (slot disco_fragmentado); (si | no)
    (slot obstruccion_suciedad); (si | no)
    (slot mas_2_anos); edad (si | no)
)

(deftemplate sistema_operativo
    "Template que define las caracteristicas de los sistemas operativos"
    (declare (slot-specific TRUE))
	(slot id); (linux | windows)
    (slot antivirus); (si | no)
    (slot virus); (si | no)
    (slot arranque); (lento | normal)
    (slot ficheros); (defectuosos | correctos)
    (slot aplicaciones); (lentas | rapidas)
    (slot errores_busqueda); (si | no)
    (slot programas_2plano); (si | no) 
    (slot reinicio_constante); (si | no)
)

(deftemplate usuario
	"Template que define la configuracion del programa"
    (declare (slot-specific TRUE))    
    (slot nombre)
)


; INSTANCIAS (VACIAS)
(assert (pc))
(assert (sistema_operativo))
(assert (usuario))


; REGLAS
(defrule entran_virus
	?s <- (sistema_operativo (id ?id) (antivirus ?a)) 
    (test (eq ?id windows))
    (test (eq ?a no))
=>
    (modify ?s (virus si))  
)

(defrule errores_busqueda
	?s <- (sistema_operativo (arranque ?a)) 
    (test (eq ?a lento))
=>
    (modify ?s (errores_busqueda si))  
)

(defrule ficheros_defectuosos_virus
	?s <- (sistema_operativo (virus ?v)) 
    (test (eq ?v si))
=>
    (modify ?s (ficheros defectuosos))  
)

(defrule disco_duro_lento
    ?p <- (pc)
	?s <- (sistema_operativo (errores_busqueda ?e) (ficheros ?f)) 
    (test (eq ?e si))
    (test (eq ?f defectuosos))
=>
    (modify ?p (disco_duro lento))  
)

(defrule pc_viejo
    ?p <- (pc (mas_2_anos ?e))
    (test (eq ?e si))
=>
    (modify ?p (estado viejo)) 
)

(defrule pc_nuevo
    ?p <- (pc (mas_2_anos ?e))
    (test (eq ?e no))
=>
    (modify ?p (estado nuevo))
)

(defrule disco_duro_fragmentado
	?p <- (pc (disco_duro ?hd))
    ?s <- (sistema_operativo (id ?id) (aplicaciones ?ap))
    (test (eq ?hd lento))
    (test (eq ?id windows))
    (test (eq ?ap lentas))
=>
    (modify ?p (disco_fragmentado si))
)

(defrule obstruccion_suciedad
	?p <- (pc (estado ?e) (ruido_ventiladores ?rv))
    (test (eq ?e viejo))
    (test (eq ?rv si))
=>
    (modify ?p (obstruccion_suciedad si))
)

(defrule ficheros_defectuosos_cortes
	?p <- (pc (fuente_cortes ?f))
    ?s <- (sistema_operativo (programas_2plano ?pp))
    (test (eq ?f si))
    (test (eq ?pp si))
=>
    (modify ?s (ficheros defectuosos))
)

(defrule programas_2_plano
    ?s <- (sistema_operativo (aplicaciones ?a))
    (test (eq ?a lentas))
=>
    (modify ?s (programas_2plano si))
)

(defrule calienta_cpu
	?s <- (sistema_operativo (programas_2plano ?pp) (reinicio_constante ?rc))
    ?p <- (pc)
    (test (eq ?pp si))
    (test (eq ?rc si))
=>
    (modify ?p (cpu calienta))
)

(defrule fallo_disipador
	?p <- (pc (obstruccion_suciedad ?o) (cpu ?c))
    (test (eq ?o si))
    (test (eq ?c calienta))
=>
    (modify ?p (disipador falla))
)

(defrule ram_saturada
	?p <- (pc (estado ?e))
    ?s <- (sistema_operativo (programas_2plano ?pp))
    (test (eq ?e viejo))
    (test (eq ?pp si))
=>
    (modify ?p (ram saturada))
)

(defrule q_nombre
	(declare (salience 100))
    ?u <- (usuario (nombre ?n))
    (test (eq ?n nil))
=>
    (printout t "¿Me dice su nombre para poder dirigirme a usted?" crlf)
    (modify ?u (nombre (read)))
)

(defrule q_sistema_operativo
    ?s <- (sistema_operativo (id ?id))
    ?u <- (usuario (nombre ?n))
    (test (eq ?id nil))
=>
    (printout t ?n ": ¿Que sistema operativo tiene instalado? (windows | linux)" crlf)
    (modify ?s (id (read)))
)

(defrule q_arranque
    ?s <- (sistema_operativo (arranque ?a))
    ?u <- (usuario (nombre ?n))
    (test (eq ?a nil))
=>
    (printout t ?n ": ¿Cómo es el arranque del ordenador? (lento | normal)" crlf)
    (modify ?s (arranque (read)))
)

(defrule q_edad_pc
    ?p <- (pc (mas_2_anos ?m))
    ?u <- (usuario (nombre ?n))
    (test (eq ?m nil))
=>
    (printout t ?n ": ¿Tu PC tiene mas de 2 años? (si | no)" crlf)
    (modify ?p (mas_2_anos (read)))
)

(defrule q_antivirus
    ?s <- (sistema_operativo (id ?id) (antivirus ?a))
    ?u <- (usuario (nombre ?n))
    (test (eq ?id windows))
    (test (eq ?a nil))
=>
    (printout t ?n ": ¿Tienes algun antivirus instalado en el sistema operativo? (si | no)" crlf)
    (modify ?s (antivirus (read)))
)

(defrule q_cortes_luz
    ?p <- (pc (fuente_cortes ?f))
    ?u <- (usuario (nombre ?n))
    (test (eq ?f nil))
=>
    (printout t ?n ": ¿Se va la luz con frecuencia en su domicilio? (si |no)" crlf)
    (modify ?p (fuente_cortes (read)))
)

(defrule q_aplicaciones_lentas
    ?s <- (sistema_operativo (aplicaciones ?a))
    ?u <- (usuario (nombre ?n))
    (test (eq ?a nil))
=>
    (printout t ?n ": ¿Como son las aplicaciones al ejecutarse? (lentas | rapidas)" crlf)
    (modify ?s (aplicaciones (read)))
)

(defrule q_ruido_ventiladores
    ?p <- (pc (ruido_ventiladores ?rv))
    ?u <- (usuario (nombre ?n))
    (test (eq ?rv nil))
=>
    (printout t ?n ": ¿Los ventiladores hacen mas ruido de lo normal? (si | no)" crlf)
    (modify ?p (ruido_ventiladores (read)))
)

(defrule q_reinicio_constante
    ?s <- (sistema_operativo (reinicio_constante ?rc))
    ?u <- (usuario (nombre ?n))
    (test (eq ?rc nil))
=>
    (printout t ?n ": Una vez iniciada la sesion, ¿el ordenador se reinicia constantemente? (si | no)" crlf)
    (modify ?s (reinicio_constante (read)))
)

(defrule sol_antivirus
    ?s <- (sistema_operativo (aplicaciones ?a))
    ?p <- (pc (disco_duro ?hd))
    ?u <- (usuario (nombre ?n))
    (test (eq ?a rapidas))
    (test (eq ?hd lento))
=>
    (printout t ?n ": El sistema operativo tiene virus, es recomedable que instales un antivirus." crlf)
    (halt) 
)

(defrule sol_desfragmentar
	?p <- (pc (disco_fragmentado ?hf))
    ?u <- (usuario (nombre ?n))
    (test (eq ?hf si))
=>
    (printout t ?n ": El disco duro esta fragmentado, se recomienda que utilices una aplicacion para desfragmentarlo." crlf)
    (halt)
)

(defrule sol_formateo_windows
	?p <- (pc (cpu ?c) (ram ?r))
    ?s <- (sistema_operativo (id ?id))
    ?u <- (usuario (nombre ?n))
    (test (eq ?c calienta))
    (test (eq ?r saturada))
    (test (eq ?id windows))
=>
    (printout t ?n ": Se recomienda que el S.O Windows sea formateado." crlf)
    (halt)
)

(defrule sol_formatear_linux
    ?p <- (pc (disco_duro ?hd))
    ?s <- (sistema_operativo (id ?id))
    ?u <- (usuario (nombre ?n))
    (test (eq ?id linux))
    (test (eq ?hd lento))
=>
    (printout t ?n ": Se recomienda que el S.O Linux sea formateado." crlf)
    (halt)
)

(defrule sol_cambiar_pasta_termica
	?p <- (pc (disipador ?d))
    ?u <- (usuario (nombre ?n))
    (test (eq ?d falla))
=>
    (printout t ?n ": Se recomienda que se cambie la pasta termica del disipador del procesador y que se limpie la suciedad interna del PC" crlf)
    (halt)    
)

(deffunction inicio ()
	(printout t "¿Indica el control inferencial? (depth | breadth)" crlf)
	(set-strategy (read))
    (printout t "¿Quieres activar el modo verbose? (si | no)" crlf)
    (bind ?aux (read))
    (if (eq ?aux si) then (watch all))
)

(inicio)
(run)