#include <opencv2/opencv.hpp>
#include "gnuplot/gnuplot-iostream.h"
using namespace cv;

// -------------------------------------------------------------
//  GRAFICAS
// -------------------------------------------------------------

void grafica_proyeccion(int total_cols, int proyeccion[]){

    Gnuplot gp;

    // Grafica pixeles_horizontales/suma_columnas
    std::vector<std::pair<int,int> > puntos_xy;
    for(int c=0;c<total_cols;c++){
        puntos_xy.push_back(std::make_pair(c,proyeccion[c]));
    }
    gp << "set title 'Proyeccion horizontal de pixeles'\n";
    gp << "set ylabel 'Suma por columnas de pixeles'\n";
    gp << "set xlabel 'Filas de la imagen'\n";
    gp << "plot '-' with lines\n";
    gp.send1d(puntos_xy);

}

void grafica_espectro(int total_cols, float frecuencia[], Mat potencia){

    Gnuplot gp;

    // Grafica frecuencia/potencia (Transformada de fourier)
    std::vector<std::pair<float,float> > puntos_xy;
    for(int c=0;c<total_cols;c++){
        puntos_xy.push_back(std::make_pair(frecuencia[c],potencia.at<float>(0,c)));
        //puntos_xy.push_back(std::make_pair(c,potencia.at<float>(0,c)));
    }    
    gp << "set title 'Espectro'\n";
    gp << "set ylabel 'Energia (dbi)'\n";
    gp << "set xlabel 'Frecuencia (ciclos/pixel)'\n";
    gp << "plot '-' with impulses\n";
    gp.send1d(puntos_xy);

}

