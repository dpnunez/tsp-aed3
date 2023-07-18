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
    [0, 141, 134, 152, 173, 289, 326, 329, 285, 401, 388, 366, 343, 305, 276],
    [141, 0, 152, 150, 153, 312, 354, 313, 249, 324, 300, 272, 247, 201, 176],
    [134, 152, 0, 24, 48, 168, 210, 197, 153, 280, 272, 257, 237, 210, 181],
    [152, 150, 24, 0, 24, 163, 206, 182, 133, 257, 248, 233, 214, 187, 158],
    [173, 153, 48, 24, 0, 160, 203, 167, 114, 234, 225, 210, 190, 165, 137],
    [289, 312, 168, 163, 160, 0, 43, 90, 124, 250, 264, 270, 264, 267, 249],
    [326, 354, 210, 206, 203, 43, 0, 108, 157, 271, 290, 299, 295, 303, 287],
    [329, 313, 197, 182, 167, 90, 108, 0, 70, 164, 183, 195, 194, 210, 201],
    [285, 249, 153, 133, 114, 124, 157, 70, 0, 141, 147, 148, 140, 147, 134],
    [401, 324, 280, 257, 234, 250, 271, 164, 141, 0, 36, 67, 88, 134, 150],
    [388, 300, 272, 248, 225, 264, 290, 183, 147, 36, 0, 33, 57, 104, 124],
    [366, 272, 257, 233, 210, 270, 299, 195, 148, 67, 33, 0, 26, 73, 96],
    [343, 247, 237, 214, 190, 264, 295, 194, 140, 88, 57, 26, 0, 48, 71],
    [305, 201, 210, 187, 165, 267, 303, 210, 147, 134, 104, 73, 48, 0, 30],
    [276, 176, 181, 158, 137, 249, 287, 201, 134, 150, 124, 96, 71, 30, 0]
])
best_cost = 1194

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


