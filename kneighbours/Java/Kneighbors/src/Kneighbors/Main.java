
package Kneighbors;

/*

Autor: Pascual Andres Carrasco Gomez
Descripcion: Algoritmo k vecinos mas cercanos
Corpus: Flores: Virginica, Setosa, Versicolor (150 muestas etiquetadas)
Entorno: JAVA

*/

import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Collections;

public class Main {

    //--------------------------------------------------------
    // Funciones
    //--------------------------------------------------------
    // Imprime texto por pantalla
    public static void print(String texto){System.out.println(texto);}
    
    // Carga a partir de un fichero los datos del corpus
    public static ArrayList cargarDatos(String fichero){
        ArrayList datos = new ArrayList();
        String cadena;
        try{
            FileReader f = new FileReader(fichero);
            BufferedReader b = new BufferedReader(f);
            while((cadena = b.readLine())!=null) {
                String[] aux_datos = cadena.split(" ");
                Flor flor = new Flor(Float.parseFloat(aux_datos[0]),Float.parseFloat(aux_datos[1]),Float.parseFloat(aux_datos[2]),Float.parseFloat(aux_datos[3]),aux_datos[4]);
                datos.add(flor);
            }
            b.close();
        }catch(Exception e){
            print("Se ha producido un error al cargar los datos del corpus");
        }
        return datos;
    }
    
    // Calcula la distancia euclidea entre las caracteristicas de dos flores
    public static float d_euclidea(Flor f1, Flor f2){
        float aux1 = (float) Math.pow(f2.getLargo_sepalo()-f1.getLargo_sepalo(),2);
        float aux2 = (float) Math.pow(f2.getAncho_sepalo()-f1.getAncho_sepalo(),2);
        float aux3 = (float) Math.pow(f2.getLargo_petalo()-f1.getLargo_petalo(),2);
        float aux4 = (float) Math.pow(f2.getAncho_petalo()-f1.getAncho_petalo(),2);
        float d = (float) Math.sqrt(aux1+aux2+aux3+aux4);
        return d;
    }
    
    // Convierte la clase de la flor (String) a entero (int) -> Comodidad y eficiencia
    public static int int_clase(String clase){
        int n;
        switch(clase){
            case "virginica": n = 0; break;
            case "setosa": n = 1; break;
            case "versicolor": n = 2; break;
            default: n = -1;
        }
        return n;
    }
    
    // Argumentos de entrada
    // args[0] = ruta del fichero del corpus (iris.dat)
    // args[1] = k
    public static void main(String[] args) {
        // Fichero que hace referencia al corpus (Flores: Iris)
        String ruta_f = "./corpus/iris.dat";
        // Parametro k del algoritmo kneighbors
        int k = 5;
        // Cargamos los datos
        ArrayList datos = cargarDatos(ruta_f);
        // Separamos el corpus en entrenamiento (train) y evaluacion (test)
        // 20% test (30 muestras) 80% train (120 muestras)
        int n_test = (datos.size()*20)/100;
        int n_train = datos.size()-n_test;
        ArrayList test = new ArrayList();
        ArrayList train = new ArrayList();
        for(int i=0;i<n_test;i++){
            test.add(datos.get(i));
        }
        for(int i=n_test;i<datos.size();i++){
            train.add(datos.get(i));
        }
        // Algoritmo kneighbours
        ArrayList res_test = new ArrayList();
        for(int i=0;i<n_test;i++){
            ArrayList distancias = new ArrayList();
            Flor f_test = (Flor) test.get(i);
            for(int j=0;j<n_train;j++){
                Flor f_train = (Flor) train.get(j);
                float d_e = d_euclidea(f_test, f_train);
                Distancia d = new Distancia(d_e, f_train.getTipo());
                distancias.add(d);
            }
            // Ordenamos las distancias por distancia_euclidea (de menor a mayor)
            Collections.sort(distancias);
            // Etiquetamos al objeto de train con la clase mas votada
            int n_clases = 3;
            ArrayList cont = new ArrayList();
            for(int j=0;j<n_clases;j++){
                cont.add(0);
            }
            for(int j=0;j<k;j++){
                Distancia d = (Distancia) distancias.get(j);
                int clase = int_clase(d.getTipo());
                int aux = ((int) cont.get(clase)) + 1;
                cont.set(clase,aux);
            }
            int cont_max = (int) Collections.max(cont);
            res_test.add(cont.indexOf(cont_max));
        }        
        // Evaluacion
        int aciertos = 0;
        int muestras_totales = n_test;
        int muestras_analizadas = res_test.size();
        for(int i=0;i<n_test;i++){
            int clase_obtenida = (int) res_test.get(i);
            int clase_real =  int_clase(((Flor) test.get(i)).getTipo());
            if(clase_obtenida == clase_real){
                aciertos++;
            }
        }
        float coverage = muestras_analizadas/(float)muestras_totales;
        float precision = aciertos/(float)muestras_analizadas;
        float recall = aciertos/(float)muestras_totales;
        float f1 = (2*precision*recall)/(float)(precision+recall);
        print("-----------------------------------------");
        print("Resultados:");
        print("-----------------------------------------");
        print("Aciertos: " + aciertos);
        print("Muestras analizadas: " + muestras_analizadas);
        print("Muestras totales: " + muestras_totales);
        print("-----------------------------------------");
        print("Medidas de evaluación:");
        print("-----------------------------------------");
        print("Coverage: " + String.format("%.5f", coverage).replace(",", "."));
        print("Precision: " + String.format("%.5f", precision).replace(",", "."));
        print("Recall: " + String.format("%.5f", recall).replace(",", "."));
        print("F1-score: " + String.format("%.5f", f1).replace(",", "."));
    }
    
}
