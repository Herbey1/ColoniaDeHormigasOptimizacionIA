import random as rn
import numpy as np
from numpy.random import choice as np_choice

class AntColony(object):
    def __init__(self, distancias, n_ants, n_best, n_veces, decay, alpha=1, beta=1):
#distances: Matriz cuadrada de distancias entre ciudades.
#n_ants: Número de hormigas que corren por iteración.
#n_best: Número de mejores hormigas que depositan feromona.
#n_iterations: Número de iteraciones.
#decay: Tasa en la que la feromona decae.
#alpha y beta: Exponentes en la formula de seleccion de la proxima ciudad.
        
        #Pasamos el valor a los atributos de la instancia
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_veces = n_veces
        self.decay = decay
        self.alpha = alpha
        self.beta = beta
        self.distancias  = distancias
        self.feromona = np.ones(self.distancias.shape) / len(distancias)
        #Creamos una matriz de 1, con las dimensiones especificadas en self.distance.shape, que es la forma de la matriz de distancias.
        #Despues, dividimos la matriz de 1, entre el numero de ciudades (len(distances)), para obtener una matriz de feromonas inicial.
        self.all_indices = range(len(distancias))

    def correr(self, inicio, destino):
        cortoiteracion = None
        elmascorto = ("unodostres", np.inf)

        for i in range(self.n_veces):
            # Generamos todas las rutas posibles
            todoscaminos = self.hacertodoscaminos(inicio, destino)
            # Esparcimos feromonas en las n_best rutas, si es que son mejores que la mejor ruta actual.
            self.tirarferomona(todoscaminos, self.n_best, cortoiteracion=cortoiteracion)
            # Actualizamos la mejor ruta
            cortoiteracion = min(todoscaminos, key=lambda x: x[1])
            # Si la mejor ruta actual es mejor que la mejor ruta de todos los tiempos.
            if cortoiteracion[1] < elmascorto[1]:
                # Actualizamos la mejor ruta de todos los tiempos.
                elmascorto = cortoiteracion    
            # Decrecemos la feromona en todas las rutas        
            self.feromona = self.feromona * self.decay    
        # Regresamos la mejor ruta de todos los tiempos.        
        return elmascorto
    
    #Función para esparcir feromonas en las n_best rutas.
    def tirarferomona(self, todoscaminos, n_best, cortoiteracion):
        #Ordenamos las rutas por distancia. Se ordena usando la funcion sorted, con una funcion de clave "key" que es la distancia de la ruta.
        caminosordenados = sorted(todoscaminos, key=lambda x: x[1])
        #Para cada ruta "path" y distancia se itera sobre cada movimiento en la ruta.
        for camino, dist in caminosordenados[:n_best]:
            #En cada movimiento incrementaremos la cantidad de feromona depositada en la matriz de feomona correspondiente a ese movimiento.
            for moverse in camino:
                self.feromona[moverse] += 1.0 / self.distancias[moverse]

    def distanciatotal(self, camino):
        total_dist = 0
        for ele in camino:
            total_dist += self.distancias[ele]
        return total_dist
# Distancia total de una ruta. Una ruta "path" de entrada, itera sobre cada elemento de la ruta, entra a la matriz de distancias para obtener la distancia correspondiente a cada par de ciudades consecutivas en la ruta, y suma todas las distancias para obtener la distancia total de la ruta, devolviendo la distancia total calculada.

    def hacertodoscaminos(self, inicio, destino):
        todoscaminos = []
        for i in range(self.n_ants):
            camino = self.generarcamino(inicio, destino)
            todoscaminos.append((camino, self.distanciatotal(camino)))
        return todoscaminos
# Posibles rutas. Genera una lista vacia que almacena las rutas generadas. Itera sobre self.n_ants, y para cada iteracion se genera una ruta para una hormiga y calcula la distancia total de esa ruta usando el metodo anterior. Y agregamos la ruta con la distancia a la matriz generada. Y devuelve todas al final.

    def generarcamino(self, inicio, destino):
        camino = []
        visito = set()
        visito.add(inicio)
        prev = inicio
        for i in range(len(self.distancias) - 1):
            moverse = self.movimiento(self.feromona[prev], self.distancias[prev], visito)
            if moverse is None:
                # No hay movimientos válidos disponibles, romper el ciclo
                break
            camino.append((prev, moverse))
            prev = moverse
            visito.add(moverse)
        camino.append((prev, destino))
        return camino
# Genera una ruta para una hormiga. Se inicializa una lista vacia "path" que almacenara la ruta generada. Se inicializa un conjunto vacio "visited" que almacenara las ciudades visitadas. Se agrega la ciudad inicial a "visited". Se inicializa la variable "prev" con la ciudad inicial. Se itera sobre el rango de la longitud de la matriz de distancias menos 1. Se elige un movimiento con el metodo "pick_move" que se explicara despues. Se agrega el movimiento a la ruta. Se actualiza la ciudad previa a la ciudad actual. Se agrega la ciudad actual a las ciudades visitadas. Al final se agrega el movimiento de regreso a la ciudad inicial. Y se devuelve la ruta generada.

    def movimiento(self, feromona, dist, visito):
        feromona = np.copy(feromona)
        feromona[list(visito)] = 0

        fila = feromona ** self.alpha * ((1.0 / dist) ** self.beta)
        fila[np.isinf(dist)] = 0  # Establecer probabilidad a cero para distancias infinitas

        indices_validos = np.flatnonzero(fila)
        if indices_validos.size > 0:
            norm_fila = fila[indices_validos] / fila[indices_validos].sum()
            moverse = np_choice(indices_validos, 1, p=norm_fila)[0]
        else:
            # No hay movimientos válidos disponibles
            moverse = None

        return moverse
# Elige un movimiento para una hormiga. Se copia la matriz de feromonas. Se establece a 0 las feromonas de las ciudades visitadas. Se calcula la probabilidad de moverse a una ciudad con la formula de seleccion de la proxima ciudad. Se normaliza la fila de probabilidades. Se elige un movimiento con la funcion np_choice. Y se devuelve el movimiento elegido.