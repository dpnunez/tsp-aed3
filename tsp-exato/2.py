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
    [0, 64, 378, 519, 434, 200],
    [64, 0, 318, 455, 375, 164],
    [378, 318, 0, 170, 265, 344],
    [519, 455, 170, 0, 223, 428],
    [434, 375, 265, 223, 0, 273],
    [200, 164, 344, 428, 273, 0]
]

best_path, best_distance = tsp_brute_force(distances)

print("Melhor caminho:", best_path)
print("Distância total:", best_distance)
print("--- %s seconds ---" % (time.time() - start_time))