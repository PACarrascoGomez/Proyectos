/*
Practica 5: Iluminacion y Texturas
Autor: Pascual Andres Carrasco Gomez
*/

// Variables globales consensuadas
var renderer, scene, camera;

// Variables componentes del robot
var suelo , robot, base, brazo, eje, esparrago, rotula, antebrazo, disco, nervio1;
var nervio2, nervio3, nervio4, mano, pinzaIzq, pinzaDer;

// Variables setupGUI
var controller;

// Variables tiempo
var antes = Date.now();

// Variable teclado
var keyboard = new THREEx.KeyboardState();


init();
loadScene();
setupGUI();
render();

function init(){
	// Configurar el motor de render
	renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);
	renderer.setClearColor(new THREE.Color(0x0000AA));
	renderer.shadowMapEnabled = true; // habilitamos sombras
	renderer.antialias = true;
	document.getElementById('container').appendChild(renderer.domElement);

	// Escena
	scene = new THREE.Scene();

	// Camara para la entrega de la practica
	var aspectRatio = window.innerWidth / window.innerHeight;
	camera = new THREE.PerspectiveCamera(55,aspectRatio,1,2000);
	camera.position.set(250,250,300);
	//camera.lookAt(new THREE.Vector3(0,50,0));
	// Controles de camara por raton
	cameraControls = new THREE.OrbitAndPanControls(camera,renderer.domElement);
	cameraControls.target.set(0,50,0);

	// Stats
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

	// Luz ambiental
	var luzAmbiente = new THREE.AmbientLight (0x999999);
	scene.add(luzAmbiente);
	// Luz puntual
	var luzPuntual = new THREE.PointLight(0xBBBBBB, 1.0);
	luzPuntual.position.set(150,150,100);
	scene.add(luzPuntual);
	// Luz Focal
	var luzFocal = new THREE.SpotLight (0xFFFFFF);
	luzFocal.position.set(200,600,300);
	luzFocal.target.position.set(400,1600,400);
	luzFocal.angle = Math.PI/3;
	luzFocal.rotation.set( 0, Math.PI, 0 );

	// Sombras (Solo funcionan para luz focal en WebGL)
	luzFocal.shadowCameraNear = 200;
	luzFocal.shadowCameraFar = 2000;
	//luzFocal.shadowCameraVisible = true;
	luzFocal.castShadow = true; 
	luzFocal.shadowCameraFov = 30;
	luzFocal.shadowDarkness = 1;
	luzFocal.shadowMapWidth = 1024;
	luzFocal.shadowMapHeight = 1024;
	scene.add (luzFocal);

	// Atencion al evento de resize
	window.addEventListener('resize',updateAspectRatio);

}

function loadScene(){
	
	// Cargar la textura de mapa de entorno
	var path = "images/";
	var urls = [path+"posx.jpg",path+"negx.jpg",path+"posy.jpg",path+"negy.jpg",path+"posz.jpg",path+"negz.jpg"];
	var mapaEntorno = THREE.ImageUtils.loadTextureCube(urls);
	mapaEntorno.format = THREE.RGBFormat;

	// Textura Cubo (Habitacion)
	var shader = THREE.ShaderLib.cube;
	shader.uniforms.tCube.value = mapaEntorno;
	var materialParedes = new THREE.ShaderMaterial({
		fragmentShader: shader.fragmentShader,
		vertexShader: shader.vertexShader,
		uniforms: shader.uniforms,
		depthWrite: false,
		side: THREE.BackSide
	});

	// Creamos un Cubo que cubra la escena (Habitacion)
    var habitacion = new THREE.Mesh(new THREE.BoxGeometry(1500,1500,1500), materialParedes);
    scene.add(habitacion);

	// Textura para el suelo
	var texturaSuelo = new THREE.ImageUtils.loadTexture("./images/pisometal_1024x1024.jpg");
	texturaSuelo.wrapS = texturaSuelo.wrapT = THREE.RepeatWrapping;
	texturaSuelo.repeat.set(5,5);
	texturaSuelo.magFilter = THREE.LinearFilter;
	texturaSuelo.minFilter = THREE.LinearFilter;
	
	// Textura de Metal
	var texturaMetal = new THREE.ImageUtils.loadTexture("./images/metal_128.jpg");
	texturaMetal.wrapS = texturaMetal.wrapT = THREE.RepeatWrapping;
	texturaMetal.repeat.set(1,1);
	texturaMetal.magFilter = THREE.LinearFilter;
	texturaMetal.minFilter = THREE.LinearFilter;
	
	// Textura de Bronce
    var texturaBronce = new THREE.ImageUtils.loadTexture("./images/bronce.jpg");
    texturaBronce.wrapS = texturaBronce.wrapT = THREE.RepeatWrapping;
    texturaBronce.repeat.set(1,1);
    texturaBronce.magFilter = THREE.LinearFilter;
    texturaBronce.minFilter = THREE.LinearFilter;

	// Materiales
	var materialSuelo = new THREE.MeshPhongMaterial({color:0x999999, map: texturaSuelo, side: THREE.DoubleSide});
	var materialMetal = new THREE.MeshLambertMaterial({color:0x000000, map: texturaMetal});
	var materialBronce = new THREE.MeshLambertMaterial({color:0xFFFFFF, map: texturaBronce, side: THREE.DoubleSide});
	var materialRotula = new THREE.MeshPhongMaterial({ambient:0xFF0000,color:0xFFFFFF,specular:0x222222,shininess:50,envMap: mapaEntorno});
	var materialPinza = new THREE.MeshPhongMaterial ({ambient:0x555555, color:0x555555, specular:0x666666, shininess:100, shading: THREE.FlatShading});

	// Geometrias
	var geometria_suelo = new THREE.PlaneGeometry(1000,1000,20,20);
	var geometria_base = new THREE.CylinderGeometry(50,50,15,30,1);
	var geometria_eje = new THREE.CylinderGeometry(20,20,18,30,1);
	var geometria_esparrago = new THREE.BoxGeometry(18,120,12);
	var geometria_rotula = new THREE.SphereGeometry(20,20,20);
	var geometria_disco = new THREE.CylinderGeometry(22,22,6,50,1);
	var geometria_nervio = new THREE.BoxGeometry(4,80,4);
	var geometria_mano = new THREE.CylinderGeometry(15,15,40,40,1);


	// Geometria definida a mano: pinzas
	var malla = new THREE.Geometry();
	var coordenadas = [
					0.0,20.0,0.0, 		// v0
					19.0,20.0,0.0, 		// v1
					19.0,0.0,0.0,		// v2
					0.0,0.0,0.0,		// v3
					0.0,20.0,-4.0, 		// v4
					19.0,20.0,-4.0, 	// v5
					19.0,0.0,-4.0,		// v6
					0.0,0.0,-4.0,		// v7
					38.0,15.0,0.0,		// v8
					38.0,5.0,0.0,		// v9
					38.0,15.0,-2.0,		// v10
					38.0,5.0,-2.0 ];	// v11
	var indices = [
				// Parte delantera
				3,2,1, 1,0,3, 2,9,8, 8,1,2,
				// Parte superior
				0,1,5, 5,4,0, 1,8,10, 10,5,1,
				// Parte inferior
				7,6,2, 2,3,7, 6,11,9, 9,2,6,
				// Parte trasera
				4,5,6, 6,7,4, 5,10,11, 11,6,5,
				// Lateral izquierdo
				7,3,0, 0,4,7,
				// Lateral derecho
				9,11,10, 10,8,9 ];

	// Pasamos las coordenadas
	for(var i=0;i<coordenadas.length;i+=3){
		var vertice = new THREE.Vector3(coordenadas[i],coordenadas[i+1],coordenadas[i+2]);
		malla.vertices.push(vertice);
	}
	// Pasamos los indices de los triangulos
	for(var i=0;i<indices.length;i+=3){
		var triangulo = new THREE.Face3(indices[i],indices[i+1],indices[i+2]);
		malla.faces.push(triangulo);
	}

	// Contruimos objetos
	suelo = new THREE.Mesh(geometria_suelo,materialSuelo);
	robot = new THREE.Object3D();
	base = new THREE.Mesh(geometria_base,materialMetal);
	brazo = new THREE.Object3D();
	eje = new THREE.Mesh(geometria_eje,materialMetal);
	esparrago = new THREE.Mesh(geometria_esparrago,materialMetal);
	rotula = new THREE.Mesh(geometria_rotula,materialRotula);
	antebrazo = new THREE.Object3D();
	disco = new THREE.Mesh(geometria_disco,materialBronce);
	nervio1 = new THREE.Mesh(geometria_nervio,materialBronce);
	nervio2 = new THREE.Mesh(geometria_nervio,materialBronce);
	nervio3 = new THREE.Mesh(geometria_nervio,materialBronce);
	nervio4 = new THREE.Mesh(geometria_nervio,materialBronce);
	mano = new THREE.Mesh(geometria_mano,materialBronce);
	pinzaIzq = new THREE.Mesh(malla,materialPinza);
	pinzaDer = new THREE.Mesh(malla,materialPinza);
	
	// Emision y recepcion de sombras de los objetos
	suelo.receiveShadow = true;
	base.castShadow = true;
	base.receiveShadow = true;
	eje.castShadow = true;
	eje.receiveShadow = true;
	esparrago.castShadow = true;
	esparrago.receiveShadow = true;
	rotula.castShadow = true;
	rotula.receiveShadow = true;
	disco.castShadow = true;
	disco.receiveShadow = true;
	nervio1.castShadow = true;
	nervio1.receiveShadow = true;
	nervio2.castShadow = true;
	nervio2.receiveShadow = true;
	nervio3.castShadow = true;
	nervio3.receiveShadow = true;
	nervio4.castShadow = true;
	nervio4.receiveShadow = true;
	mano.castShadow = true;
	mano.receiveShadow = true;
	pinzaIzq.castShadow = true;
	pinzaIzq.receiveShadow = true;
	pinzaDer.castShadow = true;
	pinzaDer.receiveShadow = true;

	// Transformaciones
	suelo.rotation.x = Math.PI/2;
	eje.rotation.x = Math.PI/2;
	esparrago.position.y = 60.0;
	rotula.position.y = 120.0;
	disco.position.y = 120.0;
	nervio1.position.set(-9.0,40.0,-9.0);
	nervio2.position.set(9.0,40.0,-9.0);
	nervio3.position.set(-9.0,40.0,9.0);
	nervio4.position.set(9.0,40.0,9.0);
	mano.rotation.x = Math.PI/2;
	mano.position.y = 80.0;
	pinzaDer.position.set(0,-15,10);
	pinzaDer.rotation.x = -Math.PI/2;
	pinzaIzq.position.set(0,15,-10);
	pinzaIzq.rotation.x = Math.PI/2;


	// Anadimos la forma a la escena
	mano.add(pinzaDer);
	mano.add(pinzaIzq);
	antebrazo.add(mano);
	antebrazo.add(nervio1);
	antebrazo.add(nervio2);	
	antebrazo.add(nervio3);
	antebrazo.add(nervio4);
	disco.add(antebrazo);
	brazo.add(disco);
	brazo.add(rotula);
	brazo.add(esparrago);
	brazo.add(eje);
	base.add(brazo);
	robot.add(base);
	scene.add(robot);
	scene.add(suelo);
	scene.add(new THREE.AxisHelper(1));

	// Anadimos un texto a la escena
	var geometriaTexto = new THREE.TextGeometry('Robot GPC: Pascual Andres Carrasco Gomez',
	{
		size:35, height:10.1, curveSegments:3,
		font:"helvetiker", weight:"bold", style:"normal",
		bevelThickness:0.05, bevelSize:0.04, bevelEnabled:true
	});
	var texto = new THREE.Mesh (geometriaTexto, materialBronce);
	texto.position.set(-500,200,-470);
	texto.castShadow = true;
	scene.add(texto);

}

function setupGUI(){
	controller = {
		mensaje: "Controles Peonza",
		giroBase: 0,
		giroBrazo: 0,
		giroAntebrazoY: 0,
		giroAntebrazoZ: 0,
		giroPinza: 0,
		separacionPinza: 0
	};

	var gui = new dat.GUI();
	var h = gui.addFolder("Control Robot");
	h.add(controller,"giroBase",-180,180,0.5).name("Giro Base");
	h.add(controller,"giroBrazo",-45,45,0.5).name("Giro Brazo");
	h.add(controller,"giroAntebrazoY",-180,180,0.5).name("Giro Antebrazo Y");
	h.add(controller,"giroAntebrazoZ",-90,90,0.5).name("Giro Antebrazo Z");
	h.add(controller,"giroPinza",-220,40,0.5).name("Giro Pinza");
	h.add(controller,"separacionPinza",0,15,0.5).name("Separacion Pinza");
}

function update(){
	// Movimientos por teclado
	if(keyboard.pressed("left") && robot.position.x > -500) robot.translateX(-1.0);
	if(keyboard.pressed("right") && robot.position.x < 500) robot.translateX(1.0);
    if(keyboard.pressed("up") && robot.position.z > -500) robot.translateZ(-1.0);
    if(keyboard.pressed("down") && robot.position.z < 500)robot.translateZ(1.0);
	//Actualiza los movimientos
	base.rotation.y = (controller.giroBase*Math.PI)/180;
	brazo.rotation.z = (controller.giroBrazo*Math.PI)/180;
	disco.rotation.z = (controller.giroAntebrazoZ*Math.PI)/180;
	disco.rotation.y = (controller.giroAntebrazoY*Math.PI)/180;
    mano.rotation.y = (controller.giroPinza*Math.PI)/-180;
    pinzaIzq.position.set(pinzaIzq.position.x,controller.separacionPinza,pinzaIzq.position.z);
    pinzaDer.position.set(pinzaDer.position.x,-controller.separacionPinza,pinzaDer.position.z);
    // Actualiza los stats
	stats_fps.update();
	stats_ms.update();
}

function updateAspectRatio(){
	var aspectRatio = window.innerWidth / window.innerHeight;
	renderer.setSize(window.innerWidth,window.innerHeight);
	camera.aspect = aspectRatio; // Para que no afecte la isometria al redimensionar la ventana
	camera.updateProjectionMatrix(); // Al cambiar el aspectRatio tenemos que actualizar la matriz de proyeccion
}

// Bucle -> se ejecuta cada frame
function render(){
	requestAnimationFrame(render);
	update()
	cameraControls.update();
	renderer.render(scene,camera);
}
