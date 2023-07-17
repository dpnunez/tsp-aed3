import numpy as np
import time
start_time = time.time()

def tsp_2opt(distances):
    # Inicialização
    n = len(distances)
    best_route = np.arange(n)  # Rota inicial: [0, 1, 2, ..., n-1]
    improvement = True

    def calculate_total_distance(route):
        # Calcula a distância total de uma rota
        return sum(distances[route[i], route[i+1]] for i in range(n-1)) + distances[route[n-1], route[0]]

    def two_opt_swap(route, i, k):
        # Realiza a troca 2-Opt entre os índices i e k da rota
        new_route = np.copy(route)
        new_route[i:k+1] = route[i:k+1][::-1]
        return new_route

    best_distance = calculate_total_distance(best_route)

    # Loop principal
    while improvement:
        improvement = False
        for i in range(1, n - 2):
            for k in range(i + 1, n - 1):
                new_route = two_opt_swap(best_route, i, k)
                new_distance = calculate_total_distance(new_route)
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance
                    improvement = True

    return best_route, best_distance

# Matriz de distâncias fornecida
distances = np.array([
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
])

best_route, best_distance = tsp_2opt(distances)

print("Melhor rota encontrada:", best_route)
print("Distância total:", best_distance)
print("--- %s seconds ---" % (time.time() - start_time))