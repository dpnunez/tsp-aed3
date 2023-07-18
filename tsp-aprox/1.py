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
best_cost = 253

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


