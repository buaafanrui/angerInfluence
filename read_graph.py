# coding: utf-8


def read_graph(fgraph_path="10_graph.txt", weight_threshold=30):
    graph = {}
    f = file(fgraph_path)
    for line in f:
        uid1, uid2, weight, mood_list = line.strip().split('\t')
        if int(weight) > weight_threshold:
            uid1 = int(uid1)
            uid2 = int(uid2)
            weight = int(weight)
            if uid1 not in graph:
                graph[uid1] = {}
            if uid2 not in graph:
                graph[uid2] = {}
            graph[uid1][uid2] = weight
            graph[uid2][uid1] = weight
    f.close()
    return graph


def read_users_mood(fgraph_path="10_graph.txt", original=False):
    mood_dict = {}
    with open(fgraph_path) as f:
        for line in f:
            uid1, uid2, weight, mood_list = line.strip().split('\t')
            mood_list = eval(mood_list)
            if not original and sum(mood_list) > 0:
                mood_list = [val / float(sum(mood_list)) for val in mood_list]
            mood_dict[int(uid1)] = mood_list
    return mood_dict


def main():
    graph = read_graph("10_graph.txt", 30)
    fout = open("30_graph_tmp.txt", "w")
    for uid1 in graph:
        for uid2 in graph[uid1]:
            fout.write("%d\t%d\n" % (uid1, uid2))
    fout.close()


if __name__ == "__main__":
    main()
