# coding: utf-8
"""
计算节点度和情绪相关性的关系
输入：用户情绪分布（10_graph.txt）；节点度计算结果（node_properties.txt）
输出：不同节点度下的情绪相关性结果（results/degree_correlation.txt）
"""

import numpy as np
from correlation import get_simi
import matplotlib.pyplot as plt


def main(fpath='node_properties.txt', foutpath='30_graph/hop_correlation/Pearson.txt'):
    degrees = {}
    with open(fpath) as f:
        for line in f:
            uid, degree, _, mood_list1, mood_list2 = line.strip().split('\t')
            uid, degree = int(uid), int(degree)
            mood_list1, mood_list2 = eval(mood_list1), eval(mood_list2)
            degrees.setdefault(degree, [])
            degrees[degree].append((mood_list1, mood_list2))

    for degree in degrees.keys():
        if len(degrees[degree]) < 45:
            del degrees[degree]

    degree_sorted_list = sorted(degrees.items(), key=lambda d: d[0])
    fout = open(foutpath, 'w')
    for (degree, mood_list_pairs) in degree_sorted_list:
        fout.write('%d' % degree)
        for mood in range(4):
            S, T = [], []
            for (mood_list1, mood_list2) in mood_list_pairs:
                if sum(mood_list1) > 0:
                    mood_list1 = [float(val) / sum(mood_list1) for val in mood_list1]
                if sum(mood_list2) > 0:
                    mood_list2 = [float(val) / sum(mood_list2) for val in mood_list2]
                S.append(mood_list1[mood])
                T.append(mood_list2[mood])
            S, T = np.array(S), np.array(T)
            P_simi, P_error = get_simi(S, T, "Pearson", "equal")
            fout.write('\t%f,%f' % (P_simi, P_error))
            fout.flush()
        fout.write('\n')
    fout.close()


def draw_chart():
    def read_file(fpath):
        corr_simis = {}
        corr_errs = {}
        with open(fpath) as f:
            for line in f:
                line_arr = line.strip().split('\t')
                degree = int(line_arr[0])
                for i in range(1, 5):
                    mood = i - 1
                    simi, error = line_arr[i].split(',')
                    corr_simis.setdefault(mood, {})
                    corr_errs.setdefault(mood, {})
                    corr_simis[mood][degree] = float(simi)
                    corr_errs[mood][degree] = float(error)
        return corr_simis, corr_errs

    corr_simis, corr_errs = read_file("results/degree_correlation.txt")
    legends = {0: 'Anger', 1:'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        errs = [corr_errs[mood][distance] for distance in x]
        plt.errorbar(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                     yerr=errs, linewidth=2, capsize=7, markersize=8, fillstyle='none', markeredgewidth=1)
    plt.xlabel('$k$', fontsize=25)
    plt.ylabel('$C_p$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='lower left', fontsize=20)
    plt.xlim(0, 32)
    plt.show()


if __name__ == '__main__':
    # main(fpath='results/node_properties.txt', foutpath='results/degree_correlation.txt')
    draw_chart()
