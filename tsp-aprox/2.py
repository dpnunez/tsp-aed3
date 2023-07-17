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
    [0, 64, 378, 519, 434, 200],
    [64, 0, 318, 455, 375, 164],
    [378, 318, 0, 170, 265, 344],
    [519, 455, 170, 0, 223, 428],
    [434, 375, 265, 223, 0, 273],
    [200, 164, 344, 428, 273, 0]
])


best_route, best_distance = tsp_2opt(distances)

print("Melhor rota encontrada:", best_route)
print("Distância total:", best_distance)
print("--- %s seconds ---" % (time.time() - start_time))