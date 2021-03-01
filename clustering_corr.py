# coding: utf-8
import numpy as np
from correlation import get_simi
import matplotlib.pyplot as plt


def main(fpath='node_properties.txt', foutpath='30_graph/hop_correlation/Pearson.txt'):
    clusterings = {}
    with open(fpath) as f:
        for line in f:
            uid, _, clustering, mood_list1, mood_list2 = line.strip().split('\t')
            uid, clustering = int(uid), float(clustering)
            clustering = int(float(clustering) * 10) / 10.0
            mood_list1, mood_list2 = eval(mood_list1), eval(mood_list2)
            clusterings.setdefault(clustering, [])
            clusterings[clustering].append((mood_list1, mood_list2))

    for clustering in clusterings.keys():
        if len(clusterings[clustering]) < 45:
            del clusterings[clustering]

    clustering_sorted_list = sorted(clusterings.items(), key=lambda d: d[0])
    fout = open(foutpath, 'w')
    for (clustering, mood_list_pairs) in clustering_sorted_list:
        fout.write('%f' % clustering)
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
                clustering = float(line_arr[0])
                for i in range(1, 5):
                    mood = i - 1
                    simi, error = line_arr[i].split(',')
                    corr_simis.setdefault(mood, {})
                    corr_errs.setdefault(mood, {})
                    corr_simis[mood][clustering] = float(simi)
                    corr_errs[mood][clustering] = float(error)
        return corr_simis, corr_errs

    corr_simis, corr_errs = read_file("results/clustering_correlation.txt")
    legends = {0: 'Anger', 1: 'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        errs = [corr_errs[mood][distance] for distance in x]
        plt.errorbar(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                     yerr=errs, linewidth=2, capsize=15, markersize=10, fillstyle='none', markeredgewidth=2)
    plt.xlabel('$clustering$', fontsize=25)
    plt.ylabel('$C_p$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='lower right', fontsize=15)
    plt.xlim(-0.05, 1.05)
    plt.ylim(0, 0.85)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    # main(fpath='results/node_properties.txt', foutpath='results/clustering_correlation.txt')
    draw_chart()
