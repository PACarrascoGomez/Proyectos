#pragma config(Sensor, S1,     Luz,                 sensorLightActive)
#pragma config(Sensor, S2,     Proximidad,          sensorSONAR)
#pragma config(Sensor, S3,     Contacto1,           sensorTouch)
#pragma config(Sensor, S4,     Contacto2,           sensorTouch)
#pragma config(Motor,  motorA,          ,              tmotorNormal, PIDControl, )
#pragma config(Motor,  motorB,          ,              tmotorNormal, PIDControl, )
#pragma config(Motor,  motorC,          ,              tmotorNormal, PIDControl, )
//*!!Code automatically generated by 'ROBOTC' configuration wizard               !!*//

// Constantes
const tSensors sensorLuz = (tSensors) S1; //sensor Luz
const tSensors sensorProximidad = (tSensors) S2; //sensor Proximidad
const tSensors sensorContacto1 = (tSensors)S3; //sensor Contacto
const tSensors sensorContacto2 = (tSensors)S4; //sensor Contacto

// Cabecera de Funciones
void mover();
void permanecerDentro();
void atacar();
void acercarse();
void rastreador();


//------------------------------------------------------
// Funciones
//------------------------------------------------------
// Mover el robot
void mover(int speedA, int speedB){
	motor[motorA]=speedA;
	motor[motorB]=speedB;
}

// Funcion para permanecer dentro del circuito
void permanecerDentro(){
	ClearTimer(T1);
	while (time1[T1]<100){
		mover(0,0);
	}
	ClearTimer(T1);
	while (time1[T1]<2000){
		mover(-85,-85);
	}
	ClearTimer(T1); // Giramos y buscamos adversario
	while (SensorValue(sensorLuz) <= 50 && time1[T1]<1800){
		mover(40,-40);
		while (SensorValue(sensorProximidad)<50){ acercarse(); }
	}
	ClearTimer(T1); // Avanzamos y buscamos adversario
	while (SensorValue(sensorLuz) <= 50 && time1[T1]<1000){
		mover(90, 90);
		while (SensorValue(sensorProximidad)<50){ acercarse(); }
	}
}

// Funcion para atacar a un adversario cuando lo toca
void atacar(){
	while (SensorValue(sensorLuz) <= 50 && (SensorValue(sensorContacto1) == 1 || SensorValue(sensorContacto2) == 1)){
		mover(100, 100); // Empujamos al rival
		ClearTimer(T1);
		while(time1[T1]<400 && SensorValue(sensorLuz) <= 50){
		  motor[motorC] = 100; // Golpeamos arriba
		}
		ClearTimer(T1);
		while(time1[T1]<400 && SensorValue(sensorLuz) <= 50){
		  motor[motorC] = -100; // Golpeamos abajo
		}
	}
	motor[motorC] = 0; // Dejamos de golpear
	if (SensorValue(sensorLuz)>50){ permanecerDentro(); } // Permanecemos dentro
}

// Funcion para aproximarse a un adversario cuando lo ve
void acercarse(){
	while (SensorValue(sensorLuz) <= 50){
		mover(90, 90); // Nos aceracmos hacia el rival
		while(SensorValue(sensorContacto1) == 1 || SensorValue(sensorContacto2) == 1){ atacar(); } // Atacamos al rival
	}
	if (SensorValue(sensorLuz)>50){ permanecerDentro(); } // Permanecemos dentro
}

// Funcion para buscar rivales
void rastreador(){
	while (true){
		while (SensorValue(sensorLuz) <= 50){
			while (SensorValue(sensorProximidad)<50){
				acercarse();
			}
			ClearTimer(T1); // Giramos y buscamos rival
			while (SensorValue(sensorLuz) <= 50 && time1[T1]<2700){
				mover(40, -40);
				while (SensorValue(sensorProximidad)<50){ acercarse(); }
			}
			ClearTimer(T1); // Vamos hacia delante y buscamos rival
			while (SensorValue(sensorLuz) <= 50 && time1[T1]<1300){
				mover(90, 90);
				while (SensorValue(sensorProximidad)<50){ acercarse(); }
			}
		}
		permanecerDentro();
	}
}


//------------------------------------------------------
// Tarea Principal
//------------------------------------------------------
task main(){
	mover(90,90);
	rastreador();
}




