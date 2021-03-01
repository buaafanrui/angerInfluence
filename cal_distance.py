# coding: utf-8
import os

from read_graph import read_graph, read_users_mood


def cal_distances(graph, weight_threshold, max_distance=1):
    if not os.path.isdir('distances'):
        os.mkdir('distances')
    distance_files = {}
    for distance in range(1, max_distance + 1):
        distance_files[distance] = open(('distances/threshold=%d_distance=%d.txt' % (weight_threshold, distance)), 'w')
    for uid in graph:
        closer_uid_set = set()
        last_uid_set = set([uid])
        for distance in range(1, max_distance + 1):
            next_uid_set = set()
            for uid1 in last_uid_set:
                for uid2 in graph[uid1]:
                    if uid2 != uid and uid2 not in closer_uid_set:
                        next_uid_set.add(uid2)
            for uid_next in next_uid_set:
                if uid < uid_next:
                    distance_files[distance].write('%s\t%s\n' % (uid, uid_next))
            closer_uid_set.update(next_uid_set)
            last_uid_set = next_uid_set
    for distance in range(1, max_distance + 1):
        distance_files[distance].close()


if __name__ == '__main__':
    graph = read_graph("10_graph.txt", 30)
    cal_distances(graph, 30, 6)
    for weight_threshold in range(10, 81, 5):
        graph = read_graph("10_graph.txt", weight_threshold)
        cal_distances(graph, weight_threshold, 3)
