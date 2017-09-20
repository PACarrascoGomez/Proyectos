#include <stdio.h>
#include <math.h>
#include <opencv2/opencv.hpp>
#include "grafica.cpp"
#include "dft.cpp"

using namespace cv;
using namespace std;

int main(int argc, char** argv )
{
 
    int opcion;
    bool graficas = false;
    float sv = 100.0; // Segmentacion vertical
    string inFileName="", opgraficas="", opverbose="";
    while ((opcion=getopt(argc,argv,"i:g:m:s:"))!=-1)
        switch (opcion)  {
        case 'i':
          inFileName = optarg;
          break;
        case 'g':
          opgraficas = optarg;
          graficas = true;
          break;
        case 'm':
          opverbose = optarg;
          break;
        case 's':
          sv = atof(optarg);
          break;
        default:
          return -1;
        }

    // Comprobamos los argumentos
    if (inFileName.compare("") == 0){
        printf("------------------------------------------------------------\n");
        printf("Error: No se ha introducido una imagen\n");
        printf("Uso: ./alturaX [-g vg] -i path_imagen [-m v] [-s valor]\n");
        printf("-g -> Indicar que muestre graficas\n");
        printf("\tvg -> hace referencia al tipo de grafica:\n");
        printf("\t\tp: proyeccion horizontal\n");
        printf("\t\te: espectro\n");
        printf("\t\ta: all\n");
        printf("-m -> Indicar el modo de salida por pantalla\n");
        printf("\tv -> modo verbose\n");
        printf("-s -> Segmentacion vertical de la imagen\n");
        printf("\tvalor -> numero real de particiones final\n");
        printf("------------------------------------------------------------\n");

        return -1;
    }

    // Cargamos la imagen en escala de grises
    Mat imagen_entrada = imread(inFileName,0);

    // Comprobamos que el fichero indicado sea una imagen
    if ( !imagen_entrada.data )
    {
        printf("El archivo introducido no corresponde con una imagen\n");
        return -1;
    }

    // Invertimos la matriz para darle mas peso a los pixeles negros que blancos
    Mat tmp = imagen_entrada ^ 0xFF;
    imagen_entrada = tmp;
    
    // Declaramos la imagen a color
    Mat imagen_lineas;

    // Realizamos una normalizacion de la imagen respecto a la proyeccion vertical 
    // para realizar un filtro en las segmentaciones verticales de la imagen
    int p_v[imagen_entrada.cols];
    int m_v = 0;
    for(int c=0;c<imagen_entrada.cols;c++){
        p_v[c] = 0;
        for(int f=0;f<imagen_entrada.rows;f++) p_v[c] += imagen_entrada.at<uchar>(f,c);
        m_v += p_v[c];
    }
    float p_v_p[imagen_entrada.cols];
    for(int c=0;c<imagen_entrada.cols;c++) p_v_p[c] = (float)p_v[c]/m_v;

    // Vectores para la gestion general de las alturas de las lineas
    int talla_alturas_general = 0;
    int v_alturas_general[imagen_entrada.rows];
    int v_freq_general[imagen_entrada.rows];

    // segmentar verticalmente la imagen
    for(int vp=20;vp<=sv;vp+=20){

        // Abrimos la imagen para segmentarla con lineas (En color)
        if(opverbose.compare("v") == 0) imagen_lineas = imread(inFileName,1); // Modo verbose

        // Anchura de la segmentacion por columna
        int ac = round(imagen_entrada.cols/float(vp));

        int q_cols = ceil((float)imagen_entrada.cols/ac);
        float v_calidad_roi_vertical[q_cols];
        float v_calidad_roi_vertical_ord[q_cols];

        // Filtro sobre la segmentacion vertical de la imagen
        int ac_aux = ac;
        for(int rc=0,p=0;rc<imagen_entrada.cols;rc+=ac_aux,p++){

            // Comprobamos que la ROI no se salga de la imagen
            if(rc+ac_aux > imagen_entrada.cols) ac_aux = imagen_entrada.cols - rc;

            float aux = 0.0;
            for(int c=rc;c<rc+ac_aux;c++) aux += p_v_p[c];
            v_calidad_roi_vertical[p] = aux;
            v_calidad_roi_vertical_ord[p] = v_calidad_roi_vertical[p];
            
        }
        sort(v_calidad_roi_vertical_ord,v_calidad_roi_vertical_ord+q_cols);
        int q_cols_malas = round(q_cols*0.3);
        int q_cols_buenas = q_cols-q_cols_malas;
        int columnas_buenas[q_cols_buenas];
        for(int c=q_cols_malas;c<q_cols;c++){
            int i = 0;
            while(v_calidad_roi_vertical_ord[c] != v_calidad_roi_vertical[i]) i++;
            columnas_buenas[c-q_cols_malas] = i;
        }

        // Segmentacion de la imagen en columnas
        for(int rc=0,columna=0;rc<imagen_entrada.cols;rc+=ac,columna++){

            // Trabajamos unicamente con las columnas buenas
            int aux_c = 0;
            while(columna != columnas_buenas[aux_c]) aux_c++;
            if(aux_c != q_cols_buenas){

                // Comprobamos que la ROI no se salga de la imagen
                if(rc+ac > imagen_entrada.cols) ac = imagen_entrada.cols - rc;

                // Creamos la ROI de anchura la segmentacion vertical
                Rect roi_vertical(rc, 0, ac, imagen_entrada.rows);
                Mat imagen = imagen_entrada(roi_vertical);

                // Suma de valores de pixeles por columna de la imagen
                int v[imagen.rows];
                int v_aux[imagen.rows];
                int media = 0;
              	for(int f=0;f<imagen.rows;f++){
                    v[f] = 0;
                    v_aux[f] = 0;
              		for(int c=0;c<imagen.cols;c++){
              			v[f] += imagen.at<uchar>(f,c); // Para trabajar con graficas
                        v_aux[f] += imagen.at<uchar>(f,c); // Para trabajar con el (conversion a Mat posterior)
              		}
                    media += v[f];
              	}

                // Creamos el vector de normalizacion para estimar la calidad de las lineas
                float v_proyeccion_norm[imagen.rows];
                if(media != 0) // Por el caso de la imagen completamente blanca
                    for(int f=0;f<imagen.rows;f++) v_proyeccion_norm[f] = (float)v[f]/media;

                // Quitamos el valor de continua
                media /= imagen.rows;
                for(int f=0;f<imagen.rows;f++){
                    v[f] -= media;
                    v_aux[f] -= media;
                }

                // Aplicamos la dft
                Mat mat_f = dft_v(v_aux,imagen.rows);

                // Valor de la frecuencia
                float dw = 1.0/imagen.rows;
                float w[mat_f.rows];
                for(int i=0;i<mat_f.rows;i++){
                    w[i] = i*dw;
                }

                // Ordenamos las intensidades de energia del espectro de menor a mayor
                int i_length = mat_f.rows/2; // El espectro es una funcion simetrica por lo tanto nos quedamos con la mitad de los datos
                float i_ord[i_length-2]; // La dft devuelve frecuencia[0] = informacion dft y frecuencia[1] = tamaño texto
                for(int i=0;i<i_length;i++) i_ord[i] = mat_f.at<float>(0,i+2);
                size_t size = sizeof(i_ord) / sizeof(i_ord[0]);
                sort(i_ord,i_ord+size);

                // Obtenemos la intensidad mas alta
                float i_max = i_ord[i_length-3];

                // Obtenemos la frecuencia correspondiente a la intensidad mas alta
                float f_imax = 0.0;
                int i = 2; // La dft devuelve frecuencia[0] = informacion dft y frecuencia[1] = tamaño texto
                bool encontrado = false;
                while(i < i_length && !encontrado){
                    if(i_max == mat_f.at<float>(0,i)){
                        f_imax = w[i];
                        encontrado = true;
                    }
                    i++;
                }

                // La aproximacion de la altura de la linea corresponde al periodo
                int altura_linea = round(1.0/f_imax);

                // Aproximacion de las alturas de cada linea y su valor de calidad
                int v_altura_lineas[imagen.rows];
                float v_calidad_lineas[imagen.rows];
                int talla_val = 0; // Talla del vector v_altura_lineas y v_calidad_lineas

                // Modo verbose
                if(opverbose.compare("v") == 0){
                    printf("---------------------------------------------------------------------\n");
                    printf("ALTURAS DE CADA LINEA CON SU PONDERACION\n");
                    printf("---------------------------------------------------------------------\n");
                }

                // Obtenemos los fragmentos que corresponden a las lineas
                // y aplicamos el algoritmo sobre cada linea formateada
                for(int i=0;i<imagen.rows;i+=altura_linea){

                    // Comprobamos que no nos salimos al hacer la ROI
                    if(i+altura_linea<imagen.rows){
                  
                        // ROI
                        Rect roi(0, i, imagen.cols, altura_linea);
                        Mat imagen_roi = imagen(roi);

                        // Proyección horizontal de la ROI
                        int v_roi[imagen_roi.rows];
                        int v_roi_ord[imagen_roi.rows]; // Para ordenarlos posteriormente
                        for(int f=0;f<imagen_roi.rows;f++){
                            v_roi[f] = 0;
                            v_roi_ord[f] = 0;
                            for(int c=0;c<imagen_roi.cols;c++){
                                v_roi[f] += imagen_roi.at<uchar>(f,c);
                                v_roi_ord[f] += imagen_roi.at<uchar>(f,c);
                            }
                        }

                        // Ordenamos el vector de la proyeccion de menor a mayor
                        size_t size = sizeof(v_roi_ord) / sizeof(v_roi_ord[0]); 
                        sort(v_roi_ord,v_roi_ord+size);

                        // Obtenemos el valor mas alto en el eje Y
                        int ymax = v_roi_ord[imagen_roi.rows-1];

                        // Obtenemos el valor del eje X correspondiente al Y max
                        int x_ymax = 0;
                        int j = 0; // La dft devuelve frecuencia[0] = 0 y frecuencia[1] = informacion de la dft 
                        bool encontrado = false;
                        while(j < imagen_roi.rows && !encontrado){
                            if(ymax == v_roi[j]){
                                x_ymax = j;
                                encontrado = true;
                            }
                            j++;
                        }

                        // Centramos la linea sobre el eje Y
                        // Dividimos la proyeccion en 3 ventanas iguales
                        if(x_ymax >= 2.0*(altura_linea/3.0)){
                            i += x_ymax - altura_linea/2;
                            if((i+altura_linea)<=imagen.rows){ // Comprobamos los margenes de la imagen
                                Rect roi(0, i, imagen.cols, altura_linea);
                                imagen_roi = imagen(roi);
                            }else i -= x_ymax - altura_linea/2; // Dejamos la i como estaba
                        }else if(x_ymax <= altura_linea/3.0){
                            i -= altura_linea/2 - x_ymax;
                            if(i >= 0){ // Comprobamos los margenes de la imagen
                                Rect roi(0, i, imagen.cols, altura_linea);
                                imagen_roi = imagen(roi);
                            }else i += altura_linea/2 - x_ymax; // Dejamos la i como estaba
                        }

                        //----------------------------------------------------------------------------
                        // Obtenemos la aproximación de la altura de el caracter
                        //----------------------------------------------------------------------------

                        // Proyección horizontal de la ROI
                        float roi_ponderada = 0.0;
                        for(int f=0;f<imagen_roi.rows;f++){
                            v_roi[f] = 0.0;
                            v_roi_ord[f] = 0.0;
                            for(int c=0;c<imagen_roi.cols;c++){
                                v_roi[f] += imagen_roi.at<uchar>(f,c);
                                v_roi_ord[f] += imagen_roi.at<uchar>(f,c);
                            }
                            // Ponderamos la ROI -> i+f es la fila correspondiente de la imagen de entrada
                            roi_ponderada += v_proyeccion_norm[i+f];
                        }
                        
                        // Asignamos la calidad calculada a la linea
                        v_calidad_lineas[talla_val] = roi_ponderada;

                        // Obtenemos la diferencia entre los picos de la señal sobre el eje X
                        // Ordenamos el vector de la proyeccion de menor a mayor
                        size = sizeof(v_roi_ord) / sizeof(v_roi_ord[0]); 
                        sort(v_roi_ord,v_roi_ord+size);

                        // Obtenemos la tercera parte entre el valor mas alto y el mas bajo
                        // Este valor es el que utilizamos para generar la señal cuadrada
                        int valor_max = v_roi_ord[imagen_roi.rows-1];
                        int valor_min = v_roi_ord[0];
                        int tercera_roi = round((valor_max-valor_min)/3.0);
                        tercera_roi += valor_min;

                        // Señal cuadrada
                        j = 0;
                        while(j < imagen_roi.rows){
                            if(v_roi[j] <= tercera_roi) v_roi[j] = valor_min;
                            else v_roi[j] = valor_max;
                            j++;
                        }

                        // Obtenemos el primer punto en el eje X (p1) donde Y es maximo
                        // y el ultimo punto (p2) donde Y es maximo
                        int p1 = 0;
                        int p2 = 0;
                        j = 0;
                        while((j < imagen_roi.rows-1) && (v_roi[j] == v_roi[j+1])) j++;
                        p1 = j;
                        j++;
                        while(j < imagen_roi.rows){
                            if(v_roi[j] == valor_max) p2 = j;
                            j++;
                        }

                        // Diferencia entre puntos = altura caracter
                        int altura_caracter = abs(p2-p1);
                        v_altura_lineas[talla_val] = altura_caracter;
                        talla_val++;
                        
                        // Modo verbose
                        // Segmentamos la imagen para ver el resultado de la separacion por lineas
                        if(opverbose.compare("v") == 0){
                            printf("ALTURA CARACTER: %i, Ponderacion: %f\n", altura_caracter, roi_ponderada);
                            line(imagen_lineas, Point(rc,i), Point(rc+ac,i), Scalar(255, 0, 0), 2,4,false); // Modo verbose
                            line(imagen_lineas, Point(rc,i+altura_linea), Point(rc+ac,i+altura_linea), Scalar(0, 255, 0), 2,4,false); // Modo verbose
                        }


                        // MOSTRAR TRAZA
                        // Grafica de la proyeccion horizontal señal cuadrada
                        //grafica_proyeccion(imagen_roi.rows,v_roi);
                        //imshow("Imagen",imagen_roi);
                        //waitKey();
                        
                    }

                }

                // ######################################################################################
                // Ponderacion de la altura -> lineas buenas = +peso
                // ######################################################################################

                float v_calidad_lineas_ord[talla_val];
                for(int z=0;z<talla_val;z++) v_calidad_lineas_ord[z] = v_calidad_lineas[z];
                sort(v_calidad_lineas_ord,v_calidad_lineas_ord+talla_val);
                int cantidad_alturas_validas = talla_val/2;
                int alturas_buenas[cantidad_alturas_validas];
                int talla_alturas = 0;
                for(int z=talla_val-1;z>=talla_val-cantidad_alturas_validas;z--){
                    int posicion = 0;
                    while(v_calidad_lineas_ord[z] != v_calidad_lineas[posicion]) posicion++;
                    alturas_buenas[talla_alturas] = v_altura_lineas[posicion];
                    talla_alturas++;
                }

                // Modo verbose
                if(opverbose.compare("v") == 0){
                    printf("---------------------------------------------------------------------\n");
                    printf("ALTURAS CON MEJOR PONDERACION\n");
                    printf("---------------------------------------------------------------------\n");
                    for(int z=0;z<talla_alturas;z++){
                        printf("ALTURAS BUENAS: %i\n", alturas_buenas[z]);
                    }
                    printf("---------------------------------------------------------------------\n");
                }

                // Rellenamos el vector de frecuencias con las alturas buenas que aparecen
                int aux_freq_alturas[talla_alturas];
                int aux_alturas[talla_alturas];
                int aux_cont = 0;
                sort(alturas_buenas,alturas_buenas+talla_alturas); // ordenamos las alturas        
                for(int z=0;z<talla_alturas;z++){
                    aux_alturas[aux_cont] = alturas_buenas[z];
                    aux_freq_alturas[aux_cont] = 1;
                    if(z < talla_alturas-1){
                        while(alturas_buenas[z] == alturas_buenas[z+1]){
                            aux_freq_alturas[aux_cont] += 1;
                            z++;
                        }
                    }
                    aux_cont++;
                }

                // Modo verbose
                if(opverbose.compare("v") == 0){
                    printf("---------------------------------------------------------------------\n");
                    printf("ALTURAS BUENAS CON SUS RESPECTIVAS FRECUENCIAS\n");
                    printf("---------------------------------------------------------------------\n");
                    for(int z=0;z<aux_cont;z++){
                        printf("ALTURAS LOCALES: %i\n", aux_alturas[z]);
                        printf("FREQ LOCALES: %i\n", aux_freq_alturas[z]);
                    }
                    printf("---------------------------------------------------------------------\n");
                }

                // Gestionamos el vector de alturas y frecuencias generales de todas las iteraciones
                for(int z=0;z<aux_cont;z++){
                    int posicion = 0;
                    bool encontrado = false;
                    while((posicion < talla_alturas_general) && !encontrado){
                        if(aux_alturas[z] == v_alturas_general[posicion]){
                            encontrado = true;
                            v_freq_general[posicion] += aux_freq_alturas[z];
                        }else posicion++;
                    }
                    if(!encontrado){
                        v_alturas_general[talla_alturas_general] = aux_alturas[z];
                        v_freq_general[talla_alturas_general] = aux_freq_alturas[z];
                        talla_alturas_general++;
                    }
                }

                // Modo verbose
                if(opverbose.compare("v") == 0){
                    printf("---------------------------------------------------------------------\n");
                    printf("ALTURAS ALMACENADAS HASTA EL MOMENTO CON SUS RESPECTIVAS FRECUENCIAS\n");
                    printf("---------------------------------------------------------------------\n");
                    for(int z=0;z<talla_alturas_general;z++){
                        printf("ALTURAS GENERALES: %i\n", v_alturas_general[z]);
                        printf("FREQ GENERALES: %i\n", v_freq_general[z]);
                    }
                    printf("---------------------------------------------------------------------\n");

                    // Resultado por pantalla
                    printf("-----------------------------------------------------\n");
                    printf("INFORMACION:\n");
                    printf("-----------------------------------------------------\n");
                    printf("Dimension: %i x %i pixeles\n",imagen.rows,imagen.cols);
                    printf("La frecuencia fundamental (ciclos/pixel) es: %f\n",f_imax);
                    printf("Altura linea (pixeles): %i\n",altura_linea);
                    printf("-----------------------------------------------------\n");
                }

                // opgraficas:
                //  p: proyeccion horizontal
                //  e: espectro
                //  a: all
                if(graficas){
                    // Graficas
                    if(opgraficas.compare("p") == 0) grafica_proyeccion(imagen.rows,v);
                    else if(opgraficas.compare("e") == 0) grafica_espectro(mat_f.rows/2, w, mat_f);
                    else if(opgraficas.compare("a") == 0){
                        grafica_proyeccion(imagen.rows,v);
                        grafica_espectro(mat_f.rows/2, w, mat_f);
                    }
                    else printf("La opcion escogida para las graficas no es valida\n");
                }

            }
        
        }

        // Modo verbose
        if(opverbose.compare("v") == 0){
            // Imagen de entrada en color con la fragmentacion en lineas realizada
            namedWindow("Segmentacion en lineas",WINDOW_NORMAL);
            imshow("Segmentacion en lineas",imagen_lineas);
            printf("###########################################################################################\n");
            printf("--> Pulsa cualquier tecla sobre la imagen 'Segmentacion en lineas' para continuar.\n");
            printf("###########################################################################################\n");
            waitKey();
        }


    }

    // ######################################################################################
    // Moda con contexto
    // ######################################################################################

    // Ordenamos el vector de alturas generales con su respectivas frecuencias
    int v_alturas_general_ord[talla_alturas_general];
    int v_freq_general_ord[talla_alturas_general];
    for(int z=0;z<talla_alturas_general;z++) v_alturas_general_ord[z] = v_alturas_general[z];
    sort(v_alturas_general_ord,v_alturas_general_ord+talla_alturas_general);
    for(int z=0;z<talla_alturas_general;z++){
        int posicion = 0;
        while(v_alturas_general_ord[z] != v_alturas_general[posicion]) posicion++;
        v_freq_general_ord[z] = v_freq_general[posicion];
    }
  
    // Calculamos la moda con contexto con una ventana de tres valores
    float aux_freq_contexto[talla_alturas_general]; 
    float aux_freq_contexto_ord[talla_alturas_general];
    if(v_alturas_general_ord[1] == (v_alturas_general_ord[0]+1)){
        aux_freq_contexto[0] = (v_freq_general_ord[0]+v_freq_general_ord[1])/3.0;
    }
    else aux_freq_contexto[0] = (v_freq_general_ord[0])/3.0;
    aux_freq_contexto_ord[0] = aux_freq_contexto[0];
    int posicion = 1;
    while(posicion<talla_alturas_general-1){
        aux_freq_contexto[posicion] = v_freq_general_ord[posicion];
        if(v_alturas_general_ord[posicion-1] == (v_alturas_general_ord[posicion]-1)){
            aux_freq_contexto[posicion] += v_freq_general_ord[posicion-1];
        }
        if(v_alturas_general_ord[posicion+1] == (v_alturas_general_ord[posicion]+1)){
            aux_freq_contexto[posicion] += v_freq_general_ord[posicion+1];
        }
        aux_freq_contexto[posicion] /= 3.0;
        aux_freq_contexto_ord[posicion] = aux_freq_contexto[posicion];
        posicion++;
    }
    if(v_alturas_general_ord[posicion-1] == (v_alturas_general_ord[posicion]-1)){
        aux_freq_contexto[posicion] = (v_freq_general_ord[posicion-1]+v_freq_general_ord[posicion])/3.0;
    }
    else aux_freq_contexto[posicion] = (v_freq_general_ord[posicion])/3.0;
    aux_freq_contexto_ord[posicion] = aux_freq_contexto[posicion];

    // Modo verbose
    if(opverbose.compare("v") == 0){
        printf("---------------------------------------------------------------------\n");
        printf("ALTURAS GENERALES ORDENADAS CON SU FRECUENCIA CON CONTEXTO\n");
        printf("---------------------------------------------------------------------\n");
        for(int z=0;z<talla_alturas_general;z++){
            printf("ALTURAS GENERALES ORD: %i\n", v_alturas_general_ord[z]);
            printf("FREQ CONTEXTO CORRESPONDIENTE: %f\n", aux_freq_contexto[z]);
        }
        printf("---------------------------------------------------------------------\n");
    }

    // Obtenemos el valor maximo que corresponde a la frecuencia de de altura con contexto
    sort(aux_freq_contexto_ord,aux_freq_contexto_ord+(talla_alturas_general)); // ordenamos las alturas 
    float aux_max = aux_freq_contexto_ord[talla_alturas_general-1];
    posicion = 0;
    while(aux_max != aux_freq_contexto[posicion]) posicion++;
    int mejor_altura = v_alturas_general_ord[posicion];

    printf("##########################################################\n");
    printf("SOLUCION OBTENIDA:\n");
    printf("##########################################################\n");
    printf("Dimension: %i x %i pixeles\n",imagen_entrada.rows,imagen_entrada.cols);
    printf("Altura optima: %i pixeles\n", mejor_altura);
    printf("##########################################################\n");


    //printf("%i\n", mejor_altura); // Para los scripts de la experimentacion

    return 0;
}
