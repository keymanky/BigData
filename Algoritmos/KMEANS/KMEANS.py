#Libreria para calculo de distancia Euclidiana
from scipy.spatial import distance
import random
import math


#Obtiene el vector de puntos maximos de una matriz dada; es decir el elemento i, es el maximo de todos los i de la matriz (eje vertical)
def max (matriz):

    first_array = matriz[0]
    points = len(first_array)
    array_maximos = []

    i=0

    while i < points:
        max = 0
        for j in matriz:
            if j[i] > max:
                max = j[i]
        array_maximos.append(max)
        i +=1

    return array_maximos


#Obtener el vector de puntos minimios de una matriz dada; es decir el elemento i, es el minimo de todos los i de la matriz (eje horizontal)
def min (matriz):

    first_array = matriz[0]
    points = len(first_array)
    array_minimos = []

    i=0

    while i < points:
        min = 0
        for j in matriz:
            if j[i] < min:
                min = j[i]
        array_minimos.append(min)
        i +=1

    return array_minimos


#Genera un numero aleatorio entre 1 y la longitud del vector
def num_aleatorio (vector):
    return ( random.randint(1, len(vector)-1 ) )
    #return 3


#Genera random vectores aleatorios cada uno de longitud igual a matriz (columnas)
def generar_matriz_aleatoria(matriz):

    maximo = max( matriz )
    minimo = min( matriz )

    n = len( matriz[0] )
    n_vectores = num_aleatorio(matriz)

    #print("n vectores: " + str( n_vectores) )

    array_random = []
    i = 0

    while i <= n_vectores:
        #print(i)
        tmp = []
        j = 0
        while j < n:
             tmp.append( random.uniform( minimo[j],  maximo[j]) )
             j+= 1
        array_random.append(tmp)
        i+= 1

    return array_random



def matrizDistancias (matriz_datos, random_clusters):

    matriz_distancias = []
    for vector in matriz_datos:
        tmp = []
        for random_vector in random_clusters:
            tmp.append(distance.euclidean(vector, random_vector))
        #print(tmp)
        matriz_distancias.append(tmp)

    return matriz_distancias


def ObtenerMiembroDeCluster (matriz_distancias):

    result = []
    for vector in matriz_distancias:
        min = 10000000000000
        j = 0
        for i in vector:
            if i < min:
                min = i
                vector = j
            j += 1
        result.append(vector)

    return result


def CalcularNuevoCluster (matriz_datos, vector_miembro_cluster, vectores_clusters):

    n = len( matriz_datos[0] )
    i = 0
    result = []

    while i < len(vectores_clusters):
        #print("Corrida: " + str(i) + "----------" )
        tmp = []
        k = 0

        #Almacena en la matriz tmp todos los puntos de la matriz de datos que corresponden a ese vector
        for j in vector_miembro_cluster:
            #print( str(i) + ":" + str(j) + ":" + str(k) )
            if j == i:
                tmp.append(matriz_datos[k])
            k +=1

        #print(tmp)
        #print("finaliza")

        if(len(tmp) > 0):

            k = 0
            tmp2 = []

            #Recalculamos el nuevo vector clustering en base al promedio
            while k < n:

                suma = 0
                for vectores in tmp:
                    suma = suma + vectores[k]
                tmp2.append( suma/n  )
                k+= 1
            result.append(tmp2)

        else:

             #El vector en cuestion no tienen ningun vector de la matriz de datos asignado, retorna el mismo vector
             result.append(vectores_clusters[i])

        i += 1

    return result



### CONTENIDO DEL MAIN ###

#Set de datos de prueba contenido en: /usr/local/spark/data/mllib/kmeans_data2.txt
a = (0.0, 0.0, 0.0)
b = (0.1, 0.1, 0.1)
c = (0.2, 0.2, 0.2)
d = (9.0, 9.0, 9.0)
e = (9.1, 9.1, 9.1)
f = (9.2, 9.2, 9.2)

#La lista de puntos puede contener n vectores, para este ejemplo se inserto el set de pruebas
points = []
points.append(a)
points.append(b)
points.append(c)
points.append(d)
points.append(e)
points.append(f)

#Iniciamos con n valores aleatorios
random_clusters = generar_matriz_aleatoria( points )

#N iteraciones
x = random.randint(1,100)
i = 0


while i < x:

    distancias = matrizDistancias(points, random_clusters)
    agrupamiento =  ObtenerMiembroDeCluster( distancias )
    tmp= CalcularNuevoCluster( points, agrupamiento, random_clusters )

    i+=1

print(tmp)