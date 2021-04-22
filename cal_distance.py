# coding: utf-8
"""
计算距离为h的用户对
输入：用户网络（10_graph.txt）
输出：不同距离的用户对列表（distances目录下的一系列文件）
"""

import os

from read_graph import read_graph, read_users_mood


def cal_distances(graph, weight_threshold, max_distance=1):
    if not os.path.isdir('distances'):
        os.mkdir('distances')
    distance_files = {}
    for distance in range(1, max_distance + 1):
        # 计算结果输出到以下文件中
        distance_output_file_name = 'distances/threshold=%d_distance=%d.txt' % (weight_threshold, distance)
        distance_files[distance] = open(distance_output_file_name, 'w')
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
