#include <stdio.h>
#include <math.h>

using namespace cv;
using namespace std;

Mat dft_v(int *v_aux, int v_aux_length)
{

    // Convertimos el vector a float
    float v_aux_f[v_aux_length];
    for(int i=0;i<v_aux_length;i++) v_aux_f[i] = v_aux[i];

    // Convertimos el vector v_aux[cols] a Mat
    Mat mat_v = Mat(v_aux_length,1,CV_32F,v_aux_f);

    // Expandimos la matriz de la imagen para obtener un tamaño optimo
    // para aplicar la dft
    Mat exp_mat;
    int m = getOptimalDFTSize(mat_v.rows);
    int n = getOptimalDFTSize(mat_v.cols); // En el borde insertamos 0
    copyMakeBorder(mat_v, exp_mat, 0, m - mat_v.rows, 0, n - mat_v.cols, BORDER_CONSTANT, Scalar::all(0));

    // Gestionamos una matriz 2D para poder trabajar con numeros complejos donde:
    //        mat_v2D[0] = exp_mat  <-- Parte real del numero complejo
    //        mat_v2D[1] = matriz de 0 <-- Parte imaginaria del numero complejo
    Mat mat_v2D[] = {Mat_<float>(exp_mat),Mat::zeros(exp_mat.size(), CV_32F)};

    // Le aplicamos un formato correcto a la matriz mat_dft para poder aplicar la transformada
    // de fourier y poder almacenar el resultado correctamente en numeros complejos, la funcion
    // dft() utiliza matrices de 1D por lo tanto el formato utilizado es para cada par de valores 
    // de la matriz dft, el primer valor hace refencia a dft_origen2D[0] y el segundo valor a 
    // dft_origen2D[1].
    Mat mat_dft;
    merge(mat_v2D,2,mat_dft);

    // Aplicamos la transformada de fourier discreta dtf() dejando el resultado en la 
    // matriz de origen
    dft(mat_dft,mat_dft);

    // Transformamos los valores complejos obtenidos a una magnitud real
    split(mat_dft,mat_v2D); // mat_v2D[0] = Parte real;  mat_v2D[1] = Parte imaginaria
    magnitude(mat_v2D[0],mat_v2D[1],mat_v2D[0]); // mat_v2D[0] = magnitud 

    // Matriz de frecuencias
    Mat mat_f = mat_v2D[0];

    // Aplicamos una escala logaritmica para poder visualizar los resultados
    mat_f += Scalar::all(1);
    log(mat_f,mat_f);

    // Transformamos la matriz en un rango de valores entre 0 y 1
    normalize(mat_f, mat_f, 0, 1, CV_MINMAX);

    return mat_f;
}
