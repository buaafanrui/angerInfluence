# coding:utf-8
"""
计算边权重和情绪相关性的关系
输入：用户网络和情绪分布（10_graph.txt）；不同距离下的用户对（distances目录下的一系列文件）
输出：不同边权重下的皮尔逊相关系数（results/weight_pearson_mood=*）
"""
import numpy as np
from read_graph import read_users_mood
from correlation import get_simi
import matplotlib.pyplot as plt


def main(mood, foutpath='temp.txt'):
    mood_dict = read_users_mood("10_graph.txt")
    fout = file(foutpath, 'w')
    fout.write('weight\tdistance\tpearson\n')
    for weight in range(10, 81, 5):
        print('weight=%d\n' % weight)
        for distance in range(1, 4):
            print('distance=%d\n' % distance)
            S, T = [], []
            f = file('distances/threshold=%d_distance=%d.txt' % (weight, distance))
            for line in f:
                uid1, uid2 = line.strip().split('\t')
                S.append(mood_dict[int(uid1)][mood])
                T.append(mood_dict[int(uid2)][mood])
            f.close()
            S, T = np.array(S), np.array(T)
            print("sequence length: %d" % len(S))
            P_simi, P_error = get_simi(S, T, "Pearson")
            fout.write('%d\t%d\t%f,%f\n' % (weight, distance, P_simi, P_error))
            fout.flush()
    fout.close()


def draw_chart():
    def read_file(fpath):
        corr_simis = {}
        with open(fpath) as f:
            f.readline()
            for line in f:
                weight, distance, pearson_tuple = line.strip().split('\t')
                weight, distance = int(weight), int(distance)
                simi, err = pearson_tuple.strip().split(',')
                simi, err = float(simi), float(err)
                corr_simis.setdefault(distance, {})
                corr_simis[distance][weight] = (simi, err)
        return corr_simis

    plt.figure(figsize=(16, 12))

    colors = ['red', 'green', 'blue', 'black']
    labels = ['$h=1$', '$h=2$', '$h=3$']
    markers = ['o', 's', '^']
    titles = ['(a) anger', '(b) disgust', '(c) joy', '(d) sadness']
    for mood in range(4):
        plt.subplot(2, 2, mood+1)
        fpath = 'results/weight_pearson_mood=%d.txt' % mood
        corr_simis = read_file(fpath)
        for distance in range(1, 4):
            x = sorted(corr_simis[distance].keys())
            y = [corr_simis[distance][weight][0] for weight in x]
            errs = [corr_simis[distance][weight][1] for weight in x]
            plt.errorbar(x, y, marker=markers[distance-1], label=labels[distance-1], color=colors[distance-1],
                         yerr=errs, linewidth=2, capsize=10, markersize=10, fillstyle='none', markeredgewidth=2)
        plt.xlabel('$T$', fontsize=25)
        plt.ylabel('$C_p$', fontsize=25)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.title(titles[mood], y=-0.2, fontsize=25)
        plt.legend(loc='upper left', fontsize=25)
        plt.ylim(-0.1, 0.8)
        plt.xlim(5, 85)
    plt.tight_layout()
    # plt.show()
    plt.savefig("figures/weight_corr.eps")


if __name__ == '__main__':
    # for mood in range(4):
    #     print('mood=%d\n' % mood)
    #     main(mood, foutpath='results/weight_pearson_mood=%d.txt' % mood)

    draw_chart()
