# coding: utf-8
from read_graph import read_users_mood
import networkx as nx


def create_nx_graph():
    graph = nx.Graph()
    with open('10_graph.txt') as f:
        for line in f:
            uid1, uid2, weight, mood_list = line.strip().split('\t')
            uid1, uid2 = int(uid1), int(uid2)
            graph.add_node(uid1)
            graph.add_edge(uid1, uid2)
    return graph


def main():
    user_mood_dict = read_users_mood('10_graph.txt', original=True)
    graph = create_nx_graph()
    degrees = nx.degree(graph)
    clusterings = nx.clustering(graph)
    with open('results/node_properties.txt', 'w') as fout:
        for uid1 in graph:
            degree = degrees[uid1]
            clustering = clusterings[uid1]
            mood_list = user_mood_dict[uid1]
            neighbors_mood_list = [0, 0, 0, 0]
            for uid2 in graph[uid1]:
                neighbor_mood_list = user_mood_dict[uid2]
                for mood in range(4):
                    neighbors_mood_list[mood] += neighbor_mood_list[mood]
            fout.write('%d\t%d\t%f\t%s\t%s\n' % (uid1, degree, clustering, str(mood_list), str(neighbors_mood_list)))


if __name__ == '__main__':
    main()
