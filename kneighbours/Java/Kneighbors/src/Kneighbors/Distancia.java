
package Kneighbors;

/*

Autor: Pascual Andres Carrasco Gomez
Descripcion: Algoritmo k vecinos mas cercanos
Corpus: Flores: Virginica, Setosa, Versicolor (150 muestas etiquetadas)
Entorno: JAVA

*/

public class Distancia implements Comparable<Distancia> {
    
    // Atributos
    private float distancia;
    private String tipo;

    // Metodos
    public float getDistancia() {return distancia;}
    public void setDistancia(float distancia) {this.distancia = distancia;}
    public String getTipo() {return tipo;}
    public void setTipo(String tipo) {this.tipo = tipo;}
    
    @Override
    public int compareTo(Distancia d) {
       int res;
       if(this.distancia > d.distancia){ res = 1; }
       else if(this.distancia < d.distancia){ res = -1; }
       else{ res = 0; }
       return res;
    }
    
    // Constructor
    public Distancia(float distancia, String tipo){
        this.distancia = distancia;
        this.tipo = tipo;
    }
    
}
