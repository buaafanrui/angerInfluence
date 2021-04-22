# coding: utf-8

uid_idx = 0
uid_dict = {}
with open('10_graph.txt') as f, open('10_graph_ano.txt', 'w') as fout:
    for line in f:
        uid1, uid2, edge, emotion_list = line.strip().split('\t')
        uid1, uid2 = int(uid1), int(uid2)
        if uid1 not in uid_dict:
            uid_dict[uid1] = uid_idx
            uid_idx += 1
        if uid2 not in uid_dict:
            uid_dict[uid2] = uid_idx
            uid_idx += 1
        fout.write('%d\t%d\t%s\t%s\n' % (uid_dict[uid1], uid_dict[uid2], edge, emotion_list))
