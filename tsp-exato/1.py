import itertools
import time
start_time = time.time()



def tsp_brute_force(distances):
    num_cities = len(distances)
    cities = range(num_cities)                            # Nomear as cidades através de um vetor de 0 a num_cities
    best_path = None
    best_distance = float('inf')

    for path in itertools.permutations(cities):           # Permuta todas as cidades (permutacao de 0 para todas as cidades)
        current_distance = 0
        for i in range(num_cities - 1):
            current_distance += distances[path[i]][path[i+1]]

        current_distance += distances[path[-1]][path[0]]  # Adiciona a distância de volta à cidade inicial

        if current_distance < best_distance:
            best_distance = current_distance
            best_path = path

    return best_path, best_distance


# Exemplo de uso com a matriz de distâncias fornecida

distances = [
    [0, 29, 20, 21, 16, 31, 100, 12, 4, 31, 18],
    [29, 0, 15, 29, 28, 40, 72, 21, 29, 41, 12],
    [20, 15, 0, 15, 14, 25, 81, 9, 23, 27, 13],
    [21, 29, 15, 0, 4, 12, 92, 12, 25, 13, 25],
    [16, 28, 14, 4, 0, 16, 94, 9, 20, 16, 22],
    [31, 40, 25, 12, 16, 0, 95, 24, 36, 3, 37],
    [100, 72, 81, 92, 94, 95, 0, 90, 101, 99, 84],
    [12, 21, 9, 12, 9, 24, 90, 0, 15, 25, 13],
    [4, 29, 23, 25, 20, 36, 101, 15, 0, 35, 18],
    [31, 41, 27, 13, 16, 3, 99, 25, 35, 0, 38],
    [18, 12, 13, 25, 22, 37, 84, 13, 18, 38, 0]
]

best_path, best_distance = tsp_brute_force(distances)

print("Melhor caminho:", best_path)
print("Distância total:", best_distance)
print("--- %s seconds ---" % (time.time() - start_time))