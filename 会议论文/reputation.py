import networkx as nx
import random
import numpy as np
import matplotlib.pyplot as plt


# 初始化网络
def init_graph():
    # 生成规模为L*L的方格网络（生成你需要的网络，查询networkx指令即可）
    H = nx.grid_2d_graph(L, L, periodic=True)
    new_mapping = {}
    for i in H.nodes:
        new_mapping[i] = i[0] * L + i[1]
    graph = nx.relabel_nodes(H, new_mapping)
    for node in graph.nodes:
        if random.random() < 0.5:
            graph.add_node(node, strategy=0)
        else:
            graph.add_node(node, strategy=1)
    return graph

# 收益矩阵
def payoff_matrix(strategy1, strategy2):
    if strategy1 == 0 and strategy2 == 0:
        return 1
    elif strategy1 == 0 and strategy2 == 1:
        return -r
    elif strategy1 == 1 and strategy2 == 0:
        return 1 + r
    elif strategy1 == 1 and strategy2 == 1:
        return 0


# 计算结点收益
def calculate_payoff():
    payoff_dictionary = {}
    # 遍历所有结点
    for node in nodes:
        neighbors = [neighbor for neighbor in nx.neighbors(network, node)]
        payoff = 0
        own_strategy = strategies[node]
        # 遍历邻居，计算累计收益
        for neighbor in neighbors:
            neighbor_strategy = strategies[neighbor]
            payoff += payoff_matrix(own_strategy, neighbor_strategy)
        payoff_dictionary[node] = payoff
    return payoff_dictionary


# 费米函数
def Fermi_function(x, y):
    return 1 / (1 + np.exp((x - y) / K))


# 计算合作者频率
def calculate_cooperator_rate(G, strategies):
    c = 0
    for value in strategies.values():
        if value == 0:
            c += 1
    cooperator_rate = c / len(G.nodes)
    return cooperator_rate


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


L = 50
K = 0.5
iterations = 100000
r = 0.3
T = 50
# 平均次数
simulations = 1
total_cooperator_rates = np.zeros(iterations)

for i in range(simulations):
    network = init_graph()
    strategies = nx.get_node_attributes(network, 'strategy')
    last_strategies = strategies.copy()
    nodes = network.nodes
    num_nodes = len(network.nodes)
    N = {node: 0 for node in network.nodes()}  # 存储连续合作次数
    Rep = {node: 0 for node in network.nodes()}  # 存储节点声誉
    PP = {node: 0 for node in network.nodes()}
    cooperator_rates = []


    for iteration in range(1, iterations + 1):
        payoff_dict = calculate_payoff()

        for node_i in network.nodes:
            neighbors = list(network.neighbors(node_i))
            rep = 0

            if strategies[node_i] == 0:
                N[node_i] += 1
                for neighbor in neighbors:
                    if strategies[neighbor] == 1:
                        rep += 1
                    else:
                        rep += 0.5
            else:
                N[node_i] += -1
                for neighbor in neighbors:
                    if strategies[neighbor] == 1:
                        rep += -1
                    else:
                        rep += -0.5
            if N[node_i] > T:
                P = (N[node_i] - T) / N[node_i]
            else:
                P = 0

            Rep[node_i] = Rep[node_i] * P + rep  # 更新节点声誉
            PP[node_i] = sigmoid(Rep[node_i])

        for node_i in network.nodes:
            payoff_i = payoff_dict[node_i]

            neighbors = list(network.neighbors(node_i))

            probabilities = {n: PP[n] for n in neighbors}
            total_probability = sum(probabilities.values())
            probabilities = {n: p / total_probability for n, p in probabilities.items()}
            selected_neighbor = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]
            payoff_neighbor = payoff_dict[selected_neighbor]

            probability = Fermi_function(payoff_i, payoff_neighbor)
            if random.random() < probability:
                strategies[node_i] = last_strategies[selected_neighbor]
        last_strategies = strategies.copy()
        cooperator_rate = calculate_cooperator_rate(network, strategies)
        cooperator_rates.append(cooperator_rate)
        print("\r t: {:d}/{:d}, fc: {:.4f}".format(iteration, iterations, cooperator_rate), end="     ")
    total_cooperator_rates += cooperator_rates

average_cooperator_rates = total_cooperator_rates / simulations

plt.plot(range(iterations), average_cooperator_rates)
plt.xlim([1, iterations + 1])
plt.ylim([-0.1, 1.1])
plt.xscale("log")
plt.show()