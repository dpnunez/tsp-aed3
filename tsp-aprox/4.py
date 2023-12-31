import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time

def tsp_2opt(distances, initialRoute):
    # Inicialização
    n = len(distances)
    best_route = initialRoute  # Rota inicial: gerada pelo christophides
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

def tsp_christofides(distances):
    # Obter as dimensões da matriz
    num_vertices = len(distances)

    # Converter a matriz de adjacência em uma lista de arestas
    edges = []
    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            edges.append((i, j, distances[i][j]))

    # Criar um grafo a partir das arestas
    graph = nx.Graph()
    graph.add_weighted_edges_from(edges)

    # Construir uma árvore geradora mínima usando o algoritmo de Prim
    mst = nx.minimum_spanning_tree(graph)

    # Obter os vértices de grau ímpar na árvore geradora mínima
    odd_vertices = [v for v, degree in mst.degree() if degree % 2 != 0]

    # Adicionar arestas de peso mínimo para formar um emparelhamento perfeito mínimo
    odd_graph = nx.subgraph(graph, odd_vertices)
    min_weight_matching = nx.max_weight_matching(odd_graph)

    # Combinar a árvore geradora mínima e o emparelhamento perfeito mínimo
    combined_graph = nx.MultiGraph(mst)
    for edge in min_weight_matching:
        combined_graph.add_edge(*edge)

    # Calcular um circuito euleriano no grafo combinado
    eulerian_circuit = list(nx.eulerian_circuit(combined_graph))

    # Converter o circuito euleriano em uma lista de vértices visitados
    visited_vertices = [eulerian_circuit[0][0]]
    for edge in eulerian_circuit:
        visited_vertices.append(edge[1])

    # Remover vértices duplicados para obter o caminho do TSP aproximado
    tsp_path = list(dict.fromkeys(visited_vertices))

    # Calcular o custo total do caminho do TSP
    total_cost = sum(distances[tsp_path[i-1]][tsp_path[i]] for i in range(len(tsp_path)))

    return tsp_path, total_cost


distances = np.array([
    [0, 509, 501, 312, 1019, 736, 656, 60, 1039, 726, 2314, 479, 448, 479, 619, 150, 342, 323, 635, 604, 596, 202, 0, 509, 501, 312, 1019, 736, 656, 60, 1039, 726, 2314, 479, 448, 479, 619, 150, 342, 323, 635, 604, 596, 202],
    [509, 0, 126, 474, 1526, 1226, 1133, 532, 1449, 1122, 2789, 958, 941, 978, 1127, 542, 246, 510, 1047, 1021, 1010, 364, 509, 0, 126, 474, 1526, 1226, 1133, 532, 1449, 1122, 2789, 958, 941, 978, 1127, 542, 246, 510, 1047, 1021, 1010, 364],
    [501, 126, 0, 541, 1516, 1184, 1084, 536, 1371, 1045, 2728, 913, 904, 946, 1115, 499, 321, 577, 976, 952, 941, 401, 501, 126, 0, 541, 1516, 1184, 1084, 536, 1371, 1045, 2728, 913, 904, 946, 1115, 499, 321, 577, 976, 952, 941, 401],
    [312, 474, 541, 0, 1157, 980, 919, 271, 1333, 1029, 2553, 751, 704, 720, 783, 455, 228, 37, 936, 904, 898, 171, 312, 474, 541, 0, 1157, 980, 919, 271, 1333, 1029, 2553, 751, 704, 720, 783, 455, 228, 37, 936, 904, 898, 171],
    [1019, 1526, 1516, 1157, 0, 478, 583, 996, 858, 855, 1504, 677, 651, 600, 401, 1033, 1325, 1134, 818, 808, 820, 1179, 1019, 1526, 1516, 1157, 0, 478, 583, 996, 858, 855, 1504, 677, 651, 600, 401, 1033, 1325, 1134, 818, 808, 820, 1179],
    [736, 1226, 1184, 980, 478, 0, 115, 740, 470, 379, 1581, 271, 289, 261, 308, 687, 1077, 970, 342, 336, 348, 932, 736, 1226, 1184, 980, 478, 0, 115, 740, 470, 379, 1581, 271, 289, 261, 308, 687, 1077, 970, 342, 336, 348, 932],
    [656, 1133, 1084, 919, 583, 115, 0, 667, 455, 288, 1661, 177, 216, 207, 343, 592, 997, 913, 236, 226, 237, 856, 656, 1133, 1084, 919, 583, 115, 0, 667, 455, 288, 1661, 177, 216, 207, 343, 592, 997, 913, 236, 226, 237, 856],
    [60, 532, 536, 271, 996, 740, 667, 0, 1066, 759, 2320, 493, 454, 479, 598, 206, 341, 278, 666, 634, 628, 194, 60, 532, 536, 271, 996, 740, 667, 0, 1066, 759, 2320, 493, 454, 479, 598, 206, 341, 278, 666, 634, 628, 194],
    [1039, 1449, 1371, 1333, 858, 470, 455, 1066, 0, 328, 1387, 591, 650, 656, 776, 933, 1367, 1333, 408, 438, 447, 1239, 1039, 1449, 1371, 1333, 858, 470, 455, 1066, 0, 328, 1387, 591, 650, 656, 776, 933, 1367, 1333, 408, 438, 447, 1239],
    [726, 1122, 1045, 1029, 855, 379, 288, 759, 328, 0, 1697, 333, 400, 427, 622, 610, 1046, 1033, 96, 128, 133, 922, 726, 1122, 1045, 1029, 855, 379, 288, 759, 328, 0, 1697, 333, 400, 427, 622, 610, 1046, 1033, 96, 128, 133, 922],
    [2314, 2789, 2728, 2553, 1504, 1581, 1661, 2320, 1387, 1697, 0, 1838, 1868, 1841, 1789, 2248, 2656, 2540, 1755, 1777, 1789, 2512, 2314, 2789, 2728, 2553, 1504, 1581, 1661, 2320, 1387, 1697, 0, 1838, 1868, 1841, 1789, 2248, 2656, 2540, 1755, 1777, 1789, 2512],
    [479, 958, 913, 751, 677, 271, 177, 493, 591, 333, 1838, 0, 68, 105, 336, 417, 821, 748, 243, 214, 217, 680, 479, 958, 913, 751, 677, 271, 177, 493, 591, 333, 1838, 0, 68, 105, 336, 417, 821, 748, 243, 214, 217, 680],
    [448, 941, 904, 704, 651, 289, 216, 454, 650, 400, 1868, 68, 0, 52, 287, 406, 789, 698, 311, 281, 283, 645, 448, 941, 904, 704, 651, 289, 216, 454, 650, 400, 1868, 68, 0, 52, 287, 406, 789, 698, 311, 281, 283, 645],
    [479, 978, 946, 720, 600, 261, 207, 479, 656, 427, 1841, 105, 52, 0, 237, 449, 818, 712, 341, 314, 318, 672, 479, 978, 946, 720, 600, 261, 207, 479, 656, 427, 1841, 105, 52, 0, 237, 449, 818, 712, 341, 314, 318, 672],
    [619, 1127, 1115, 783, 401, 308, 343, 598, 776, 622, 1789, 336, 287, 237, 0, 636, 932, 764, 550, 528, 535, 785, 619, 1127, 1115, 783, 401, 308, 343, 598, 776, 622, 1789, 336, 287, 237, 0, 636, 932, 764, 550, 528, 535, 785],
    [150, 542, 499, 455, 1033, 687, 592, 206, 933, 610, 2248, 417, 406, 449, 636, 0, 436, 470, 525, 496, 486, 319, 150, 542, 499, 455, 1033, 687, 592, 206, 933, 610, 2248, 417, 406, 449, 636, 0, 436, 470, 525, 496, 486, 319],
    [342, 246, 321, 228, 1325, 1077, 997, 341, 1367, 1046, 2656, 821, 789, 818, 932, 436, 0, 265, 959, 930, 921, 148, 342, 246, 321, 228, 1325, 1077, 997, 341, 1367, 1046, 2656, 821, 789, 818, 932, 436, 0, 265, 959, 930, 921, 148],
    [323, 510, 577, 37, 1134, 970, 913, 278, 1333, 1033, 2540, 748, 698, 712, 764, 470, 265, 0, 939, 907, 901, 201, 323, 510, 577, 37, 1134, 970, 913, 278, 1333, 1033, 2540, 748, 698, 712, 764, 470, 265, 0, 939, 907, 901, 201],
    [635, 1047, 976, 936, 818, 342, 236, 666, 408, 96, 1755, 243, 311, 341, 550, 525, 959, 939, 0, 33, 39, 833, 635, 1047, 976, 936, 818, 342, 236, 666, 408, 96, 1755, 243, 311, 341, 550, 525, 959, 939, 0, 33, 39, 833],
    [604, 1021, 952, 904, 808, 336, 226, 634, 438, 128, 1777, 214, 281, 314, 528, 496, 930, 907, 33, 0, 14, 803, 604, 1021, 952, 904, 808, 336, 226, 634, 438, 128, 1777, 214, 281, 314, 528, 496, 930, 907, 33, 0, 14, 803],
    [596, 1010, 941, 898, 820, 348, 237, 628, 447, 133, 1789, 217, 283, 318, 535, 486, 921, 901, 39, 14, 0, 794, 596, 1010, 941, 898, 820, 348, 237, 628, 447, 133, 1789, 217, 283, 318, 535, 486, 921, 901, 39, 14, 0, 794],
    [202, 364, 401, 171, 1179, 932, 856, 194, 1239, 922, 2512, 680, 645, 672, 785, 319, 148, 201, 833, 803, 794, 0, 202, 364, 401, 171, 1179, 932, 856, 194, 1239, 922, 2512, 680, 645, 672, 785, 319, 148, 201, 833, 803, 794, 0]
])
best_cost = 7013

chr_path, cost_single = tsp_christofides(distances)
opt_path, total_cost = tsp_2opt(distances, chr_path)

print("christofides cost: ", chr_path, cost_single)
print("total cost: ", opt_path, total_cost)

num_iterations = 500


# Listas para armazenar os tempos e custos encontrados
execution_times = []
total_costs = []

# Executar o algoritmo e medir o tempo para cada iteração
for _ in range(num_iterations):
    start_time = time.time()

    chr_path, _ = tsp_christofides(distances)
    opt_path, total_cost = tsp_2opt(distances, chr_path)

    execution_time = time.time() - start_time

    execution_times.append(execution_time * 1000)
    total_costs.append(total_cost)

# Calcular a média de tempo e custo
average_time = np.mean(execution_times)
average_cost = np.mean(total_costs)
std_deviation = np.std(execution_times)

# Plotar gráfico de linhas para tempos de execução
plt.plot(range(num_iterations), execution_times, label='tempo de execução', color='#00ab44')
plt.axhline(y=average_time, color='red', linestyle='--', label='tempo médio')
plt.text(num_iterations + 2, average_time, f'     μ: {average_time:.2f} ms', color='r', va='center', fontweight='bold')
plt.text(num_iterations + 2, average_time - 0.6 * std_deviation, f'     σ: {std_deviation:.2f} ms', color='b', va='center', fontweight='bold')
plt.xlabel('Iteração')
plt.ylabel('tempo (ms)')
plt.title('Tempo de execução')
plt.legend()
plt.show()


# Plotar gráfico de barras horizontais para custos totais
plt.barh(['Custo encontrado', 'Melhor custo possível'], [average_cost, best_cost], color="#00ab44")
plt.xlabel('Custo')
plt.title('Melhor custo possível vs encontrado')

# Adicionar os valores das barras ao gráfico
for i, v in enumerate([average_cost, best_cost]):
    plt.text(0, i, str(int(v)), color='white', va='center', fontweight='bold')

plt.show()


