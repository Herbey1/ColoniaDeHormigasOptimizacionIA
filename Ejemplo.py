import numpy as np

from AntColonia import AntColony
distancias = np.array([[np.inf, 20, 56, 43, 75],
                       [10, np.inf, 65, 84, 92],
                       [34, 23, np.inf, 23, 45],
                       [75, 59, 72, np.inf, 98],
                       [93, 24, 87, 41, np.inf]])
colonia=AntColony(distancias, 30, 30, 100, 0.50, alpha=1, beta=1)
camino = colonia.correr()
print("El camino mas corto fue: {}".format(camino))