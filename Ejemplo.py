import numpy as np
from AntColonia import AntColony

# Ciudades disponibles
ciudades = ['Tijuana', 'Rosarito', 'Tecate', 'Ensenada', 'Mexicali', 'San Felipe', 'San Quintín', 'Guerrero Negro']

# Pedir la ciudad inicial
ciudad_inicial = input("Ingresa la ciudad inicial: ")

# Pedir la ciudad destino
ciudad_destino = input("Ingresa la ciudad destino: ")

# Verificar que las ciudades ingresadas sean válidas
if ciudad_inicial not in ciudades or ciudad_destino not in ciudades:
    print("Ciudad invalida. Por favor, ingresa una ciudad válida.")
else:
    # Obtener los índices de las ciudades
    indice_inicial = ciudades.index(ciudad_inicial)
    indice_destino = ciudades.index(ciudad_destino)

    # Definir la matriz de distancias
    distancias = np.array([[np.inf, 20, 52, np.inf, np.inf, np.inf, np.inf, np.inf],
                           [20, np.inf, np.inf, 83, np.inf, np.inf, np.inf, np.inf],
                           [52, np.inf, np.inf, 83, 135, 197, np.inf, np.inf],
                           [np.inf, 83, 83, np.inf, 185, np.inf, 246, np.inf],
                           [np.inf, np.inf, 197, np.inf, np.inf, np.inf, np.inf, 394],
                           [np.inf, np.inf, np.inf, 246, np.inf, np.inf, 425, 336],
                           [np.inf, np.inf, np.inf, np.inf, 394, 336, np.inf, 425],
                           [np.inf, np.inf, np.inf, np.inf, np.inf, 425, 425, np.inf]])

    # Crear una instancia de AntColony
    colonia = AntColony(distancias, 30, 30, 100, 0.50, alpha=1, beta=1)

    # Ejecutar el algoritmo y obtener el camino más corto
    camino, distancia = colonia.correr(indice_inicial, indice_destino)

    # Mostrar el camino más corto
    ciudades_camino = [ciudades[indice_inicial] for indice_destino in camino]
    print(f"El camino más corto de {ciudad_inicial} a {ciudad_destino} es: {' -> '.join(ciudades_camino)} (distancia: {distancia})")