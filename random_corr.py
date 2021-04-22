# coding: utf-8
"""
计算随机打散后的情绪相关性
输入：为用户网络和情绪分布（10_graph.txt）；不同距离下的用户对（distances目录下的一系列文件）
输出：随机打散后的皮尔逊相关系数和斯皮尔曼等级相关系数（results/random_Pearson和results/random_Spearman.txt）
"""

from read_graph import read_users_mood
import scipy.stats as scistat
import numpy as np
import matplotlib.pyplot as plt


def main():
    mood_dict = read_users_mood("10_graph.txt")
    fout_pearson = file("results/random_Pearson.txt", 'w')
    fout_spearman = file("results/random_Spearman.txt", 'w')
    fout_pearson.write("distance\tanger\tdisgust\tjoy\tsadness\n")
    fout_spearman.write("distance\tanger\tdisgust\tjoy\tsadness\n")
    for distance in range(1, 7):
        print("distance=%d" % distance)
        fpath = 'distances/threshold=30_distance=%d.txt' % distance
        f = file(fpath)
        S_uid, T_uid = [], []
        for line in f:
            uid1, uid2 = line.strip().split('\t')
            S_uid.append(int(uid1))
            T_uid.append(int(uid2))
        f.close()
        pearson_simis = []
        spearman_simis = []
        for mood in range(4):
            print("mood=%d" % mood)
            S, T = [], []
            for i in range(len(S_uid)):
                S.append(mood_dict[S_uid[i]][mood])
                T.append(mood_dict[T_uid[i]][mood])
            S = np.array(S)
            T = np.array(T)
            np.random.shuffle(S)
            np.random.shuffle(T)
            print("sequence length: %d" % len(S))
            P_simi, _ = scistat.pearsonr(S, T)
            S_simi, _ = scistat.spearmanr(S, T)
            pearson_simis.append(P_simi)
            spearman_simis.append(S_simi)
        fout_pearson.write("%d" % distance)
        fout_spearman.write("%d" % distance)
        for mood in range(4):
            fout_pearson.write('\t%f' % pearson_simis[mood])
            fout_spearman.write('\t%f' % spearman_simis[mood])
        fout_pearson.write('\n')
        fout_spearman.write('\n')
    fout_pearson.close()
    fout_spearman.close()


def draw_chart():
    def read_file(fpath):
        corr_simis = {}
        with open(fpath) as f:
            f.readline()
            for line in f:
                line_arr = line.strip().split('\t')
                distance = int(line_arr[0])
                for i in range(1, 5):
                    mood = i - 1
                    simi = float(line_arr[i])
                    corr_simis.setdefault(mood, {})
                    corr_simis[mood][distance] = float(simi)
        return corr_simis

    plt.figure(figsize=(16, 7))
    plt.subplot(121)
    corr_simis = read_file("results/random_Pearson.txt")
    legends = {0: 'Anger', 1: 'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        plt.plot(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                 linewidth=2, markersize=10, fillstyle='none', markeredgewidth=2)
    plt.xlabel('$h$', fontsize=25)
    plt.ylabel('$C_p$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='best', fontsize=25)
    plt.title('(a) Pearson correlation', y=-0.2, fontsize=25)
    plt.xlim(0, 7)
    plt.ylim(-0.1, 0.28)

    plt.subplot(122)
    corr_simis = read_file("results/random_Spearman.txt")
    legends = {0: 'Anger', 1: 'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        plt.plot(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                     linewidth=2, markersize=10, fillstyle='none', markeredgewidth=2)
    plt.xlabel('$h$', fontsize=25)
    plt.ylabel('$C_s$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='best', fontsize=25)
    plt.title('(b) Spearman correlation', y=-0.2, fontsize=25)
    plt.xlim(0, 7)
    plt.ylim(-0.1, 0.28)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # main()
    draw_chart()
