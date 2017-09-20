/*
Proyecto GPC
Autor: Pascual Andres Carrasco Gomez
*/

//------------------------------------------------------------
// Variables globales
//------------------------------------------------------------

// Variables consensuadas
var renderer, scene, camera;
// Variables camara
var cameraControls;
// Variables para video
var video, videoImage, videoImageContext, videoTexture;
// Variables objetos mundo visual
var pista, tarima, guia1, guia2, guia_tope_derecha, guia_tope_izquierda, marcador;
var cuerpo_marcador, pilar1_marcador, pilar2_marcador, bola, bolo1, bolo2, bolo3, bolo4, bolo5;
var bolo6, bolo7, bolo8, bolo9, bolo10;
var cilindro_prueba;
// Variables objetos mundo fisico
var world, sphereBody, cilindro_bolo1, cilindro_bolo2, cilindro_bolo3, cilindro_bolo4;
var cilindro_bolo5, cilindro_bolo6, cilindro_bolo7, cilindro_bolo8, cilindro_bolo9, cilindro_bolo10;
var demo = new CANNON.Demo();
var postStepHandler;

// Variables flag
var flag_mover_bola = 1;

// Variable teclado
var keyboard = new THREEx.KeyboardState();

// Posiciones iniciales de la bola para calcular la trayectoria 
// Sistema de referencias -> X = -X, Y = Z, Z = Y
var bola_i_pos_x = 0;
var bola_i_pos_y = -0.5;
var bola_i_pos_z = 1.5;

inicio();
cargarMundoVisual();
cargarMundoFisico();
setupGUI();
render();

function inicio(){
	// Configurar el motor de render
	renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.setClearColor(new THREE.Color(0x0000AA));
	renderer.antialias = true;
	document.getElementById('container').appendChild(renderer.domElement);

	// Escena
	scene = new THREE.Scene();

	// Camara
	var aspectRatio = window.innerWidth / window.innerHeight;
	camera = new THREE.PerspectiveCamera(75,aspectRatio,1,500);
	camera.position.set(0,10,15);
	//camera.lookAt(new THREE.Vector3(0,0,0));
	// Controles de camara por raton
	cameraControls = new THREE.OrbitAndPanControls(camera,renderer.domElement);
	cameraControls.target.set(0,0,-10);

	// Reloj
	reloj = new THREE.Clock();
	reloj.start();

	// Estados
	stats_fps = new Stats();
	stats_fps.setMode(0);
	stats_fps.domElement.style.position = 'absolute';
	stats_fps.domElement.style.bottom = '0px';
	stats_fps.domElement.style.left = '0px';
	document.body.appendChild(stats_fps.domElement);
	stats_ms = new Stats();
	stats_ms.setMode(1);
	stats_ms.domElement.style.position = 'absolute';
	stats_ms.domElement.style.bottom = '0px';
	stats_ms.domElement.style.left = '100px';
	document.body.appendChild(stats_ms.domElement);

	// Luces
	// Luz ambiental
	var luzAmbiente = new THREE.AmbientLight (0x999999);
	scene.add(luzAmbiente);
	// Luz puntual (Bola inicial)
	var luzPuntual = new THREE.PointLight(0xFFFFFF, 1.0);
	luzPuntual.position.set(0,10,-2);
	scene.add(luzPuntual);

	// Atencion al evento de resize
	window.addEventListener('resize',updateAspectRatio);
}

function cargarMundoVisual(){


	//---------------------------------
	// Geometrias
	//---------------------------------
	var geometria_caja = new THREE.BoxGeometry(80,35,140);
	var geometria_pared1 = new THREE.PlaneGeometry(80,35); // Planos frontales y traseros
	var geometria_pared2 = new THREE.PlaneGeometry(160,35); // Planos laterales
	var geometria_pared3 = new THREE.PlaneGeometry(160,80); // Planos suelo y techo
	var geometria_tarima = new THREE.BoxGeometry(20,1,140);
	var geometria_guia = new THREE.BoxGeometry(2.5,1,140);
	var geometria_tope_guia1 = new THREE.PlaneGeometry(4,4); // Planos frontales y traseros
	var geometria_tope_guia2 = new THREE.PlaneGeometry(115,4); // Planos laterales
	var geometria_cuerpo_marcador = new THREE.BoxGeometry(40,10,25);
	var geometria_pilar_marcador = new THREE.BoxGeometry(7.5,10,25);
	var geometria_bola = new THREE.SphereGeometry(1.5,32,32);
	// Geometria bolo
	var geometria_bolo_cabeza_top = new THREE.CylinderGeometry(0.5,0.7,0.5,15,15);
	var geometria_bolo_cabeza_bottom = new THREE.CylinderGeometry(0.7,0.5,0.5,15,15);
	var geometria_bolo_tronco_top = new THREE.CylinderGeometry(0.5,1.0,2,15,15);
	var geometria_bolo_tronco_bottom = new THREE.CylinderGeometry(1.0,0.5,2,15,15);

	//---------------------------------
	// Texturas
	//---------------------------------
	// Tarima
	var texturaTarima = new THREE.ImageUtils.loadTexture("images/tarima.jpg");
	texturaTarima.wrapS = texturaTarima.wrapT = THREE.RepeatWrapping;
	texturaTarima.repeat.set(1,1);
	texturaTarima.magFilter = THREE.LinearFilter;
	texturaTarima.minFilter = THREE.LinearFilter;

	// Textura para la estructura del marcador y topes_guias
	// Textura1
	var texturaMarcador = new THREE.ImageUtils.loadTexture("./images/marcador.jpg");
	texturaMarcador.wrapS = texturaMarcador.wrapT = THREE.RepeatWrapping;
	texturaMarcador.repeat.set(2,1);
	texturaMarcador.magFilter = THREE.LinearFilter;
	texturaMarcador.minFilter = THREE.LinearFilter;
	// Textura2
	var texturaPilarMarcador = new THREE.ImageUtils.loadTexture("./images/pilar_marcador.jpg");
	texturaPilarMarcador.wrapS = texturaPilarMarcador.wrapT = THREE.RepeatWrapping;
	texturaPilarMarcador.repeat.set(1,1);
	texturaPilarMarcador.magFilter = THREE.LinearFilter;
	texturaPilarMarcador.minFilter = THREE.LinearFilter;
	// Textura3
	var texturaTopeGuia = new THREE.ImageUtils.loadTexture("./images/tope_guia.jpg");
	texturaTopeGuia.wrapS = texturaTopeGuia.wrapT = THREE.RepeatWrapping;
	texturaTopeGuia.repeat.set(1,1);
	texturaTopeGuia.magFilter = THREE.LinearFilter;
	texturaTopeGuia.minFilter = THREE.LinearFilter;
	// Textura3
	var texturaTopeGuiaR = new THREE.ImageUtils.loadTexture("./images/tope_guia.jpg");
	texturaTopeGuiaR.wrapS = texturaTopeGuiaR.wrapT = THREE.RepeatWrapping;
	texturaTopeGuiaR.repeat.set(10,1);
	texturaTopeGuiaR.magFilter = THREE.LinearFilter;
	texturaTopeGuiaR.minFilter = THREE.LinearFilter;

	// Textura paneles que cubren la escena
	// Textura para el panel frontal
	var texturaPanelFrontal = new THREE.ImageUtils.loadTexture("./images/pared_fondo.jpg");
	texturaPanelFrontal.wrapS = texturaPanelFrontal.wrapT = THREE.RepeatWrapping;
	texturaPanelFrontal.repeat.set(1,1);
	texturaPanelFrontal.magFilter = THREE.LinearFilter;
	texturaPanelFrontal.minFilter = THREE.LinearFilter;
	// Textura para el panel trasero
	var texturaPanelTrasero = new THREE.ImageUtils.loadTexture("./images/pared_lateral.jpg");
	texturaPanelTrasero.wrapS = texturaPanelTrasero.wrapT = THREE.RepeatWrapping;
	texturaPanelTrasero.repeat.set(1,1);
	texturaPanelTrasero.magFilter = THREE.LinearFilter;
	texturaPanelTrasero.minFilter = THREE.LinearFilter;
	// Textura para el panel lateral derecho
	var texturaPanelDerecho = new THREE.ImageUtils.loadTexture("./images/pared_lateral.jpg");
	texturaPanelDerecho.wrapS = texturaPanelDerecho.wrapT = THREE.RepeatWrapping;
	texturaPanelDerecho.repeat.set(1,1);
	texturaPanelDerecho.magFilter = THREE.LinearFilter;
	texturaPanelDerecho.minFilter = THREE.LinearFilter;
	// Textura para el panel lateral izquierdo
	var texturaPanelIzquierdo = new THREE.ImageUtils.loadTexture("./images/pared_lateral.jpg");
	texturaPanelIzquierdo.wrapS = texturaPanelIzquierdo.wrapT = THREE.RepeatWrapping;
	texturaPanelIzquierdo.repeat.set(1,1);
	texturaPanelIzquierdo.magFilter = THREE.LinearFilter;
	texturaPanelIzquierdo.minFilter = THREE.LinearFilter;
	// Textura para el panel del suelo
	var texturaPanelSuelo = new THREE.ImageUtils.loadTexture("./images/suelo.jpg");
	texturaPanelSuelo.wrapS = texturaPanelSuelo.wrapT = THREE.RepeatWrapping;
	texturaPanelSuelo.repeat.set(1,1);
	texturaPanelSuelo.magFilter = THREE.LinearFilter;
	texturaPanelSuelo.minFilter = THREE.LinearFilter;
	// Textura para el panel del techo
	var texturaPanelTecho = new THREE.ImageUtils.loadTexture("./images/techo.jpg");
	texturaPanelTecho.wrapS = texturaPanelTecho.wrapT = THREE.RepeatWrapping;
	texturaPanelTecho.repeat.set(1,1);
	texturaPanelTecho.magFilter = THREE.LinearFilter;
	texturaPanelTecho.minFilter = THREE.LinearFilter;

	//---------------------------------
	// Materiales
	//---------------------------------
	var material4 = new THREE.MeshLambertMaterial({color: 'orange', wireframe:false});
	var material_caja = new THREE.MeshLambertMaterial({color: 'yellow', wireframe:true});
	var material_bola = new THREE.MeshPhongMaterial({color: 'red', specular: '0x44444444', shininess:50});
	var material_tarima = new THREE.MeshLambertMaterial({map: texturaTarima, wireframe:false});
	var material_guia = new THREE.MeshLambertMaterial({color: 'green', wireframe:false});
	var material_bolo = new THREE.MeshPhongMaterial({color: 'white', specular: '0x44444444', shininess:50});
	var material_panelFrontal = new THREE.MeshLambertMaterial({map: texturaPanelFrontal, wireframe:false});
	var material_panelTrasero = new THREE.MeshLambertMaterial({map: texturaPanelTrasero, wireframe:false});
	var material_panelDerecho = new THREE.MeshLambertMaterial({map: texturaPanelDerecho, wireframe:false});
	var material_panelIzquierdo = new THREE.MeshLambertMaterial({map: texturaPanelIzquierdo, wireframe:false});
	var material_panelSuelo = new THREE.MeshLambertMaterial({map: texturaPanelSuelo, wireframe:false});
	var material_panelTecho = new THREE.MeshLambertMaterial({map: texturaPanelTecho, wireframe:false});
	
	// Contruimos objetos
	panelFrontal = new THREE.Mesh(geometria_pared1,material_panelFrontal);
	panelTrasero = new THREE.Mesh(geometria_pared1,material_panelTrasero);
	panelDerecho = new THREE.Mesh(geometria_pared2,material_panelDerecho);
	panelIzquierdo = new THREE.Mesh(geometria_pared2,material_panelIzquierdo);
	panelSuelo = new THREE.Mesh(geometria_pared3,material_panelSuelo);
	panelTecho = new THREE.Mesh(geometria_pared3,material_panelTecho);
	pista = new THREE.Object3D();
	tarima = new THREE.Mesh(geometria_tarima,material_tarima);
	guia1 = new THREE.Mesh(geometria_guia,material_guia);
	guia2 = new THREE.Mesh(geometria_guia,material_guia);
	// Guia tope izquierda
	guia_tope_izq_f = new THREE.Mesh(geometria_tope_guia1,new THREE.MeshLambertMaterial({ map: texturaTopeGuia })); // Panel frontal
	guia_tope_izq_li = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral izq
	guia_tope_izq_ld = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral der	
	guia_tope_izq_la = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral arriba
	guia_tope_izq_lb = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral abajo
	// Guia tope derecha
	guia_tope_der_f = new THREE.Mesh(geometria_tope_guia1,new THREE.MeshLambertMaterial({ map: texturaTopeGuia })); // Panel frontal
	guia_tope_der_li = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral izq
	guia_tope_der_ld = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral der
	guia_tope_der_la = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral arriba
	guia_tope_der_lb = new THREE.Mesh(geometria_tope_guia2,new THREE.MeshLambertMaterial({ map: texturaTopeGuiaR })); // Panel lateral abajo
	marcador = new THREE.Object3D();
	cuerpo_marcador = THREE.SceneUtils.createMultiMaterialObject( 
	geometria_cuerpo_marcador, [
		new THREE.MeshLambertMaterial({ map: texturaMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaMarcador })
	]);
	pilar1_marcador = THREE.SceneUtils.createMultiMaterialObject( 
	geometria_pilar_marcador, [
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador })
	]);
	pilar2_marcador = THREE.SceneUtils.createMultiMaterialObject( 
	geometria_pilar_marcador, [
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador }),
		new THREE.MeshLambertMaterial({ map: texturaPilarMarcador })
	]);
	bola = new THREE.Mesh(geometria_bola,material_bola);
	var bolo1_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo1_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo1_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo1_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo2_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo2_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo2_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo2_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo3_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo3_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo3_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo3_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo4_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo4_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo4_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo4_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo5_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo5_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo5_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo5_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo6_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo6_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo6_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo6_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo7_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo7_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo7_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo7_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo8_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo8_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo8_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo8_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo9_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo9_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo9_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo9_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	var bolo10_cabeza_top = new THREE.Mesh(geometria_bolo_cabeza_top,material_bolo);
	var bolo10_cabeza_bottom = new THREE.Mesh(geometria_bolo_cabeza_bottom,material_bolo);
	var bolo10_tronco_top = new THREE.Mesh(geometria_bolo_tronco_top,material_bolo);
	var bolo10_tronco_bottom = new THREE.Mesh(geometria_bolo_tronco_bottom,material_bolo);
	bolo1 = new THREE.Object3D();
	bolo2 = new THREE.Object3D();
	bolo3 = new THREE.Object3D();
	bolo4 = new THREE.Object3D();
	bolo5 = new THREE.Object3D();
	bolo6 = new THREE.Object3D();
	bolo7 = new THREE.Object3D();
	bolo8 = new THREE.Object3D();
	bolo9 = new THREE.Object3D();
	bolo10 = new THREE.Object3D();
	
	// Transformaciones para unir mallas de objetos
	// Bolos
	bolo1_cabeza_top.position.y = 2.2;
	bolo1_cabeza_bottom.position.y = 1.7;
	bolo1_tronco_top.position.y = 0.5;
	bolo1_tronco_bottom.position.y = -1.5;
	bolo2_cabeza_top.position.y = 2.2;
	bolo2_cabeza_bottom.position.y = 1.7;
	bolo2_tronco_top.position.y = 0.5;
	bolo2_tronco_bottom.position.y = -1.5;
	bolo3_cabeza_top.position.y = 2.2;
	bolo3_cabeza_bottom.position.y = 1.7;
	bolo3_tronco_top.position.y = 0.5;
	bolo3_tronco_bottom.position.y = -1.5;
	bolo4_cabeza_top.position.y = 2.2;
	bolo4_cabeza_bottom.position.y = 1.7;
	bolo4_tronco_top.position.y = 0.5;
	bolo4_tronco_bottom.position.y = -1.5;
	bolo5_cabeza_top.position.y = 2.2;
	bolo5_cabeza_bottom.position.y = 1.7;
	bolo5_tronco_top.position.y = 0.5;
	bolo5_tronco_bottom.position.y = -1.5;
	bolo6_cabeza_top.position.y = 2.2;
	bolo6_cabeza_bottom.position.y = 1.7;
	bolo6_tronco_top.position.y = 0.5;
	bolo6_tronco_bottom.position.y = -1.5;
	bolo7_cabeza_top.position.y = 2.2;
	bolo7_cabeza_bottom.position.y = 1.7;
	bolo7_tronco_top.position.y = 0.5;
	bolo7_tronco_bottom.position.y = -1.5;
	bolo8_cabeza_top.position.y = 2.2;
	bolo8_cabeza_bottom.position.y = 1.7;
	bolo8_tronco_top.position.y = 0.5;
	bolo8_tronco_bottom.position.y = -1.5;
	bolo9_cabeza_top.position.y = 2.2;
	bolo9_cabeza_bottom.position.y = 1.7;
	bolo9_tronco_top.position.y = 0.5;
	bolo9_tronco_bottom.position.y = -1.5;
	bolo10_cabeza_top.position.y = 2.2;
	bolo10_cabeza_bottom.position.y = 1.7;
	bolo10_tronco_top.position.y = 0.5;
	bolo10_tronco_bottom.position.y = -1.5;
	// Marcador
	cuerpo_marcador.position.set(0,0,0);
	pilar1_marcador.position.set(16.25,-10,0);
	pilar2_marcador.position.set(-16.25,-10,0);
	// Estructura_bolos
	bolo1.position.set(0,0.5,-125);
	bolo2.position.set(2.5,0.5,-127.5);
	bolo3.position.set(-2.5,0.5,-127.5);
	bolo4.position.set(5,0.5,-130);
	bolo5.position.set(0,0.5,-130);
	bolo6.position.set(-5,0.5,-130);
	bolo7.position.set(7.5,0.5,-132.5);
	bolo8.position.set(2.5,0.5,-132.5);
	bolo9.position.set(-2.5,0.5,-132.5);
	bolo10.position.set(-7.5,0.5,-132.5);
	
	// Transformaciones sobre objetos
	marcador.position.set(0,4,-57.5);
	tarima.position.set(0,-10.5,0);
	guia1.position.set(11.25,-10.5,0);
	guia2.position.set(-11.25,-10.5,0);
	pista.position.set(0,10,-70);
	// Posicion caja que cubre la escena
	panelFrontal.position.set(0,16.5,-140);
	panelTrasero.position.set(0,16.5,20);
	panelTrasero.rotation.set(0,Math.PI,0);
	panelDerecho.position.set(40,16.5,-60);
	panelDerecho.rotation.set(0,-Math.PI/2,0);
	panelIzquierdo.position.set(-40,16.5,-60);
	panelIzquierdo.rotation.set(0,Math.PI/2,0);
	panelSuelo.rotation.set(-Math.PI/2,0,Math.PI/2);
	panelSuelo.position.set(0,-1,-60);
	panelTecho.rotation.set(Math.PI/2,0,Math.PI/2);
	panelTecho.position.set(0,34,-60);
	// Posicion tope guia izquierda
	guia_tope_izq_f.position.set(-14.5,1,0);
	guia_tope_izq_ld.position.set(-12.5,1,-57.5);
	guia_tope_izq_ld.rotation.set(0,Math.PI/2,0);
	guia_tope_izq_li.position.set(-16.5,1,-57.5);
	guia_tope_izq_li.rotation.set(0,-Math.PI/2,0);
	guia_tope_izq_lb.rotation.set(Math.PI/2,0,Math.PI/2);
	guia_tope_izq_lb.position.set(-14.5,-1,-57.5);
	guia_tope_izq_la.rotation.set(-Math.PI/2,0,Math.PI/2);
	guia_tope_izq_la.position.set(-14.5,3,-57.5);
	// Posicion tope guia derecha
	guia_tope_der_f.position.set(14.5,1,0);
	guia_tope_der_ld.position.set(12.5,1,-57.5);
	guia_tope_der_ld.rotation.set(0,-Math.PI/2,0);
	guia_tope_der_li.position.set(16.5,1,-57.5);
	guia_tope_der_li.rotation.set(0,Math.PI/2,0);
	guia_tope_der_lb.rotation.set(Math.PI/2,0,Math.PI/2);
	guia_tope_der_lb.position.set(14.5,-1,-57.5);
	guia_tope_der_la.rotation.set(-Math.PI/2,0,Math.PI/2);
	guia_tope_der_la.position.set(14.5,3,-57.5);

	//---------------------------------------------------------------
	// VIDEO
	//---------------------------------------------------------------
	// 1.- Crear el elemto video en el doc
	video = document.createElement('video');
	// Acepta videos mp4 y ogv
	video.src = "../webgl/videos/10Pin.mp4";
	video.load();
	video.play();

	// 2.- Asociar una imagen de video a un canvas. Las dimensiones son las del video
	videoImage = document.createElement('canvas');
	videoImage.width = 656;
	videoImage.height = 480;

	// 3.- Obtener un contexto para ese canvas
	videoImageContext = videoImage.getContext('2d');
	videoImageContext.fillStyle = '#0000FF';
	videoImageContext.fillRect( 0, 0, videoImage.width, videoImage.height);

	// 4.- Crear la textura a partir de la imagen en canvas
	videoTexture = new THREE.Texture(videoImage);
	videoTexture.minFilter = THREE.LinearFilter;
	videoTexture.magFilter = THREE.LinearFilter;

	// 5.- Creo el material con esa textura
	var movieMaterial = new THREE.MeshBasicMaterial(
	{
		map: videoTexture,
		overdraw: true,
		side: THREE.DoubleSide
	});

	// 6.- Geometria y malla
	var movieGeometry = new THREE.PlaneGeometry( 26, 8, 8, 8 );
	var movieScreen = new THREE.Mesh( movieGeometry, movieMaterial );
	movieScreen.position.set( 0, 0, 12.6 );
	//movieScreen.rotation.y = Math.PI/2;
	marcador.add( movieScreen );
	//---------------------------------------------------------------

	// GRAFO DE ESCENA
	// Anadimos la forma a la escena
	bolo10.add(bolo10_tronco_bottom);
	bolo10.add(bolo10_tronco_top);
	bolo10.add(bolo10_cabeza_bottom);
	bolo10.add(bolo10_cabeza_top);
	scene.add(bolo10);
	bolo9.add(bolo9_tronco_bottom);
	bolo9.add(bolo9_tronco_top);
	bolo9.add(bolo9_cabeza_bottom);
	bolo9.add(bolo9_cabeza_top);
	scene.add(bolo9);
	bolo8.add(bolo8_tronco_bottom);
	bolo8.add(bolo8_tronco_top);
	bolo8.add(bolo8_cabeza_bottom);
	bolo8.add(bolo8_cabeza_top);
	scene.add(bolo8);
	bolo7.add(bolo7_tronco_bottom);
	bolo7.add(bolo7_tronco_top);
	bolo7.add(bolo7_cabeza_bottom);
	bolo7.add(bolo7_cabeza_top);
	scene.add(bolo7);
	bolo6.add(bolo6_tronco_bottom);
	bolo6.add(bolo6_tronco_top);
	bolo6.add(bolo6_cabeza_bottom);
	bolo6.add(bolo6_cabeza_top);
	scene.add(bolo6);
	bolo5.add(bolo5_tronco_bottom);
	bolo5.add(bolo5_tronco_top);
	bolo5.add(bolo5_cabeza_bottom);
	bolo5.add(bolo5_cabeza_top);
	scene.add(bolo5);
	bolo4.add(bolo4_tronco_bottom);
	bolo4.add(bolo4_tronco_top);
	bolo4.add(bolo4_cabeza_bottom);
	bolo4.add(bolo4_cabeza_top);
	scene.add(bolo4);
	bolo3.add(bolo3_tronco_bottom);
	bolo3.add(bolo3_tronco_top);
	bolo3.add(bolo3_cabeza_bottom);
	bolo3.add(bolo3_cabeza_top);
	scene.add(bolo3);
	bolo2.add(bolo2_tronco_bottom);
	bolo2.add(bolo2_tronco_top);
	bolo2.add(bolo2_cabeza_bottom);
	bolo2.add(bolo2_cabeza_top);
	scene.add(bolo2);
	bolo1.add(bolo1_tronco_bottom);
	bolo1.add(bolo1_tronco_top);
	bolo1.add(bolo1_cabeza_bottom);
	bolo1.add(bolo1_cabeza_top);
	scene.add(bolo1);
	scene.add(bola);
	pista.add(guia2);
	pista.add(guia1);
	pista.add(tarima);
	marcador.add(pilar2_marcador);
	marcador.add(pilar1_marcador);
	marcador.add(cuerpo_marcador);
	pista.add(marcador);
	scene.add(pista);
	scene.add(guia_tope_der_f);
	scene.add(guia_tope_der_ld);
	scene.add(guia_tope_der_li);
	scene.add(guia_tope_der_la);
	scene.add(guia_tope_der_lb);
	scene.add(guia_tope_izq_f);
	scene.add(guia_tope_izq_ld);
	scene.add(guia_tope_izq_li);
	scene.add(guia_tope_izq_la);
	scene.add(guia_tope_izq_lb);
	scene.add(panelFrontal);
	scene.add(panelTrasero);
	scene.add(panelDerecho);
	scene.add(panelIzquierdo);
	scene.add(panelSuelo);
	scene.add(panelTecho);
	scene.add(new THREE.AxisHelper(5));

	// Texto
	var geometriaTexto = new THREE.TextGeometry('Proyecto GPC: BOWLING',
	{
		size:4, height:2, curveSegments:3,
		font:"helvetiker", weight:"bold", style:"normal",
		bevelThickness:0.05, bevelSize:0.04, bevelEnabled:true
	});
	var texto = new THREE.Mesh (geometriaTexto, material4);
	texto.position.set(-33,8,0);
	marcador.add(texto);

	var geometriaTexto = new THREE.TextGeometry('Mover bola: <-- o -->',
	{
		size:1, height:1, curveSegments:3,
		font:"helvetiker", weight:"bold", style:"normal",
		bevelThickness:0.05, bevelSize:0.04, bevelEnabled:true
	});
	var texto = new THREE.Mesh (geometriaTexto, material4);
	texto.position.set(-25,12,-12);
	texto.rotation.set(0,Math.PI/5,0);
	scene.add(texto);

	var geometriaTexto = new THREE.TextGeometry('Lanzar bola: espacio',
	{
		size:1, height:1, curveSegments:3,
		font:"helvetiker", weight:"bold", style:"normal",
		bevelThickness:0.05, bevelSize:0.04, bevelEnabled:true
	});
	var texto = new THREE.Mesh (geometriaTexto, material4);
	texto.position.set(-25,10,-12);
	texto.rotation.set(0,Math.PI/5,0);
	scene.add(texto);

	var geometriaTexto = new THREE.TextGeometry('Volver a lanzar: F5',
	{
		size:1, height:1, curveSegments:3,
		font:"helvetiker", weight:"bold", style:"normal",
		bevelThickness:0.05, bevelSize:0.04, bevelEnabled:true
	});
	var texto = new THREE.Mesh (geometriaTexto, material4);
	texto.position.set(-25,8,-12);
	texto.rotation.set(0,Math.PI/5,0);
	scene.add(texto);

	// Importar mesa billar
	var loader = new THREE.ObjectLoader(); // Cargador de objetos JSON
	loader.load('models/descargados/mesaBillar/pool-table.json',
		function(objeto){
			objeto.scale.set(0.8,0.8,0.8);
			objeto.position.set(36,-1,-40);
			objeto.rotation.y = Math.PI/2;
			scene.add(objeto)
		}

	);

}

function cargarMundoFisico(){
	
	// NOTA: la libreria demo funciona con el sistema de referencia cambiado
	// X = -X; Y = Z; Z = Y;

	var masa_bola = 2;
	var masa_bolo = 1;
	var radio_bola = 1.5;
	var radio_superior_cil_bolo = 0.8;
	var radio_inferior_cil_bolo = 0.8;
	var altura_cil_bolo = 5;
	var segmentos_cil_bolo = 10;

	demo.addScene("all shapes",function(){
        var world = setupWorld(demo);
       
        // Sphere ( BOLA )
        var sphereShape = new CANNON.Sphere(radio_bola);
        sphereBody = new CANNON.Body({ mass: masa_bola });
        sphereBody.addShape(sphereShape);
        sphereBody.position.set(0,-0.5,1.5);
        world.addBody(sphereBody);
        demo.addVisual(sphereBody);

        // Cylinder ( RECUBRIMIENTOS DE LOS BOLOS )
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo1 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo1.addShape(cylinderShape);
        cilindro_bolo1.position.set(0,-125,0);
        world.addBody(cilindro_bolo1);
        demo.addVisual(cilindro_bolo1);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo2 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo2.addShape(cylinderShape);
        cilindro_bolo2.position.set(-2.5,-127.5,0);
        world.addBody(cilindro_bolo2);
        demo.addVisual(cilindro_bolo2);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo3 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo3.addShape(cylinderShape);
        cilindro_bolo3.position.set(2.5,-127.5,0);
        world.addBody(cilindro_bolo3);
        demo.addVisual(cilindro_bolo3);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo4 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo4.addShape(cylinderShape);
        cilindro_bolo4.position.set(-5,-130,0);
        world.addBody(cilindro_bolo4);
        demo.addVisual(cilindro_bolo4);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo5 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo5.addShape(cylinderShape);
        cilindro_bolo5.position.set(0,-130,0);
        world.addBody(cilindro_bolo5);
        demo.addVisual(cilindro_bolo5);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo6 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo6.addShape(cylinderShape);
        cilindro_bolo6.position.set(5,-130,0);
        world.addBody(cilindro_bolo6);
        demo.addVisual(cilindro_bolo6);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo7 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo7.addShape(cylinderShape);
        cilindro_bolo7.position.set(-7.5,-132.5,0);
        world.addBody(cilindro_bolo7);
        demo.addVisual(cilindro_bolo7);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo8 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo8.addShape(cylinderShape);
        cilindro_bolo8.position.set(-2.5,-132.5,0);
        world.addBody(cilindro_bolo8);
        demo.addVisual(cilindro_bolo8);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo9 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo9.addShape(cylinderShape);
        cilindro_bolo9.position.set(2.5,-132.5,0);
        world.addBody(cilindro_bolo9);
        demo.addVisual(cilindro_bolo9);
        var cylinderShape = new CANNON.Cylinder(radio_superior_cil_bolo,radio_inferior_cil_bolo,altura_cil_bolo,segmentos_cil_bolo);
        cilindro_bolo10 = new CANNON.Body({ mass: masa_bolo });
        cilindro_bolo10.addShape(cylinderShape);
        cilindro_bolo10.position.set(7.5,-132.5,0);
        world.addBody(cilindro_bolo10);
        demo.addVisual(cilindro_bolo10);

        // Walls ( PAREDES PARA LIMITAR LA ESCENA )
		var frontWall = new CANNON.Body( {mass:0 } );
		frontWall.addShape( new CANNON.Plane() );
		frontWall.quaternion.setFromAxisAngle(new CANNON.Vec3(1,0,0),-Math.PI/2);
		frontWall.position.y = -140;
		world.addBody( frontWall );
		demo.addVisual(frontWall);
		//--------------------------------------------
		// Comentar para ver el mundo fisico
		//--------------------------------------------
		var leftWall = new CANNON.Body( {mass:0 } );
		leftWall.addShape( new CANNON.Plane() );
		leftWall.quaternion.setFromAxisAngle(new CANNON.Vec3(0,1,0),Math.PI/2);
		leftWall.position.x = -12.5;
		world.addBody( leftWall );
		demo.addVisual(leftWall);
		var rightWall = new CANNON.Body( {mass:0 } );
		rightWall.addShape( new CANNON.Plane() );
		rightWall.quaternion.setFromAxisAngle(new CANNON.Vec3(0,1,0),-Math.PI/2);
		rightWall.position.x = 12.5;
		world.addBody( rightWall );
		demo.addVisual(rightWall);
		//--------------------------------------------
	
    });

	demo.start();
}

// Crear un mundo fisico
function setupWorld(demo){
    world = demo.getWorld();
    world.gravity.set(0,0,-30);
    world.broadphase = new CANNON.NaiveBroadphase();
    world.solver.iterations = 10;

    world.defaultContactMaterial.contactEquationStiffness = 5e2;
    world.defaultContactMaterial.contactEquationRelaxation = 10;

    // ground plane
    var groundShape = new CANNON.Plane();
    var groundBody = new CANNON.Body({ mass: 0 });
    groundBody.addShape(groundShape);
    groundBody.position.set(0,0,0);
    world.addBody(groundBody);
    demo.addVisual(groundBody);
    return world;
 };

function setupGUI(){
	controller = {
		mensaje: "Controles Bowling",
		camara: []
	};

	var gui = new dat.GUI();
	var h = gui.addFolder("Control Bowling");
	h.add(controller,"camara",{Trasera: 1, Defecto: 2}).name("Camara");
}

function animacion(x,y,z){

	if(postStepHandler){
      world.removeEventListener('postStep', postStepHandler);
    }
    //console.log(sphereBody.position);
    // Tween (MOVIMIENTO)
    var startPosition = new CANNON.Vec3(x, y, z);
    var endPosition = new CANNON.Vec3(x, -140, z);
    var tweenTime = 3; // seconds

    // Compute direction vector and get total length of the path
    var direction = new CANNON.Vec3();
    endPosition.vsub(startPosition, direction);
    var totalLength = direction.length();
    direction.normalize();

    var speed = totalLength / tweenTime;
    direction.scale(speed, sphereBody.velocity);

    // Save the start time
    var startTime = world.time;

    var offset = new CANNON.Vec3();

    postStepHandler = function(){

      // Progress is a number where 0 is at start position and 1 is at end position
      var progress = (world.time - startTime) / tweenTime;

      if(progress < 1){
        direction.scale(progress * totalLength, offset);
        startPosition.vadd(offset, sphereBody.position);
      } else {
        sphereBody.velocity.set(0,0,0);
        sphereBody.position.copy(endPosition);
        world.removeEventListener('postStep', postStepHandler);
        postStepHandler = null;
      }
    }
    
    world.addEventListener('postStep', postStepHandler);
    flag_mover_bola = 0;
}

function updateAspectRatio(){
	var aspectRatio = window.innerWidth / window.innerHeight;
	renderer.setSize(window.innerWidth,window.innerHeight);
	camera.aspect = aspectRatio; // Para que no afecte la isometria al redimensionar la ventana
	camera.updateProjectionMatrix(); // Al cambiar el aspectRatio tenemos que actualizar la matriz de proyeccion
}

function update(){
	//console.log(sphereBody.position);
	if(flag_mover_bola){
		// Movimientos por teclado -> Mover bola
		if(keyboard.pressed("left") && sphereBody.position.x < 10){
			sphereBody.position.x += 0.2;
			bola_i_pos_x += 0.2;
		}
		if(keyboard.pressed("right") && sphereBody.position.x > -10){
			sphereBody.position.x -= 0.2;
			bola_i_pos_x -= 0.2;
		}
		if(keyboard.pressed("space") && flag_mover_bola) animacion(bola_i_pos_x,bola_i_pos_y,bola_i_pos_z); // Lanzamos
	}

    // Actualizar la camara segun el parametro introducido por el usuario
    if(controller.camara == 1){
    	camera.position.set(0,7,-150); // Camara trasera
    	controller.camara = 0;
    }
    if(controller.camara == 2){
    	camera.position.set(0,10,15); // Camara defecto
    	controller.camara = 0;
    }

	// Actualizar los objetos del mundo visual
	// con la posicion de los objetos del mundo fisico
	// NOTA: Sistema de referencia en el mundo fisico --> X = -X; Y = Z; Z = Y;
	// BOLA
	var bola_pos_x = -sphereBody.position.x;
	var bola_pos_y = sphereBody.position.z;
	var bola_pos_z = sphereBody.position.y;
	var bola_rot_x = -sphereBody.quaternion.x;
	var bola_rot_y = sphereBody.quaternion.z;
	var bola_rot_z = sphereBody.quaternion.y;
	bola.position.set(bola_pos_x,bola_pos_y,bola_pos_z);
	bola.rotation.set(-bola_rot_x,bola_rot_z,bola_rot_y);
	// BOLO 1
	var bolo1_pos_x = -cilindro_bolo1.position.x;
	var bolo1_pos_y = cilindro_bolo1.position.z;
	var bolo1_pos_z = cilindro_bolo1.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo1.quaternion.toEuler(aux_v3,'YZX');
	bolo1.position.set(bolo1_pos_x,bolo1_pos_y,bolo1_pos_z);
	bolo1.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 2
	var bolo2_pos_x = -cilindro_bolo2.position.x;
	var bolo2_pos_y = cilindro_bolo2.position.z;
	var bolo2_pos_z = cilindro_bolo2.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo2.quaternion.toEuler(aux_v3,'YZX');
	bolo2.position.set(bolo2_pos_x,bolo2_pos_y,bolo2_pos_z);
	bolo2.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 3
	var bolo3_pos_x = -cilindro_bolo3.position.x;
	var bolo3_pos_y = cilindro_bolo3.position.z;
	var bolo3_pos_z = cilindro_bolo3.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo3.quaternion.toEuler(aux_v3,'YZX');
	bolo3.position.set(bolo3_pos_x,bolo3_pos_y,bolo3_pos_z);
	bolo3.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 4
	var bolo4_pos_x = -cilindro_bolo4.position.x;
	var bolo4_pos_y = cilindro_bolo4.position.z;
	var bolo4_pos_z = cilindro_bolo4.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo4.quaternion.toEuler(aux_v3,'YZX');
	bolo4.position.set(bolo4_pos_x,bolo4_pos_y,bolo4_pos_z);
	bolo4.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 5
	var bolo5_pos_x = -cilindro_bolo5.position.x;
	var bolo5_pos_y = cilindro_bolo5.position.z;
	var bolo5_pos_z = cilindro_bolo5.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo5.quaternion.toEuler(aux_v3,'YZX');
	bolo5.position.set(bolo5_pos_x,bolo5_pos_y,bolo5_pos_z);
	bolo5.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 6
	var bolo6_pos_x = -cilindro_bolo6.position.x;
	var bolo6_pos_y = cilindro_bolo6.position.z;
	var bolo6_pos_z = cilindro_bolo6.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo6.quaternion.toEuler(aux_v3,'YZX');
	bolo6.position.set(bolo6_pos_x,bolo6_pos_y,bolo6_pos_z);
	bolo6.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 7
	var bolo7_pos_x = -cilindro_bolo7.position.x;
	var bolo7_pos_y = cilindro_bolo7.position.z;
	var bolo7_pos_z = cilindro_bolo7.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo7.quaternion.toEuler(aux_v3,'YZX');
	bolo7.position.set(bolo7_pos_x,bolo7_pos_y,bolo7_pos_z);
	bolo7.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 8
	var bolo8_pos_x = -cilindro_bolo8.position.x;
	var bolo8_pos_y = cilindro_bolo8.position.z;
	var bolo8_pos_z = cilindro_bolo8.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo8.quaternion.toEuler(aux_v3,'YZX');
	bolo8.position.set(bolo8_pos_x,bolo8_pos_y,bolo8_pos_z);
	bolo8.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 9
	var bolo9_pos_x = -cilindro_bolo9.position.x;
	var bolo9_pos_y = cilindro_bolo9.position.z;
	var bolo9_pos_z = cilindro_bolo9.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo9.quaternion.toEuler(aux_v3,'YZX');
	bolo9.position.set(bolo9_pos_x,bolo9_pos_y,bolo9_pos_z);
	bolo9.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// BOLO 10
	var bolo10_pos_x = -cilindro_bolo10.position.x;
	var bolo10_pos_y = cilindro_bolo10.position.z;
	var bolo10_pos_z = cilindro_bolo10.position.y;
	var aux_v3 = new CANNON.Vec3();
	cilindro_bolo10.quaternion.toEuler(aux_v3,'YZX');
	bolo10.position.set(bolo10_pos_x,bolo10_pos_y,bolo10_pos_z);
	bolo10.rotation.set(aux_v3.z,aux_v3.y,-aux_v3.x);
	// Actualiza el control de camara
	cameraControls.update();
	// Actualiza los stats
	stats_fps.update();
	stats_ms.update();
	// Refresco del video
	if( video.readyState === video.HAVE_ENOUGH_DATA ){
		videoImageContext.drawImage( video, 0, 0 );
		if( videoTexture ) videoTexture.needsUpdate = true;
	}
}

// Bucle -> se ejecuta cada frame
function render(){
	requestAnimationFrame(render);
	update();
	renderer.render(scene,camera);
}
