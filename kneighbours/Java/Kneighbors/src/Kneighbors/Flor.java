
package Kneighbors;

/*

Autor: Pascual Andres Carrasco Gomez
Descripcion: Algoritmo k vecinos mas cercanos
Corpus: Flores: Virginica, Setosa, Versicolor (150 muestas etiquetadas)
Entorno: JAVA

*/

public class Flor {
    
    // Atributos
    private float largo_sepalo;
    private float ancho_sepalo;
    private float largo_petalo;
    private float ancho_petalo;
    private String tipo;

    // Metodos
    public float getLargo_sepalo() {return largo_sepalo;}
    public void setLargo_sepalo(float largo_sepalo) {this.largo_sepalo = largo_sepalo;}
    public float getAncho_sepalo() {return ancho_sepalo;}
    public void setAncho_sepalo(float ancho_sepalo) {this.ancho_sepalo = ancho_sepalo;}
    public float getLargo_petalo() {return largo_petalo;}
    public void setLargo_petalo(float largo_petalo) {this.largo_petalo = largo_petalo;}
    public float getAncho_petalo() {return ancho_petalo;}
    public void setAncho_petalo(float ancho_petalo) {this.ancho_petalo = ancho_petalo;}
    public String getTipo() {return tipo;}
    public void setTipo(String tipo) {this.tipo = tipo;}
    
    
    // Constructor
    public Flor(float largo_sepalo, float ancho_sepalo, float largo_petalo, float ancho_petalo, String tipo){
        this.largo_sepalo = largo_sepalo;
        this.ancho_sepalo = ancho_sepalo;
        this.largo_petalo = largo_petalo;
        this.ancho_petalo = ancho_petalo;
        this.tipo = tipo;
    }
    
}
