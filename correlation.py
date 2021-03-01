# coding:utf-8
import numpy as np
import scipy.stats as scistat
from read_graph import read_users_mood
import matplotlib.pyplot as plt


def bootstrapping(S_raw, T_raw, sample_strategy='fixed'):
    if len(S_raw) != len(T_raw):
        return -1
    N = len(S_raw)
    if sample_strategy == 'equal':
        sample_num = N
    else:
        sample_num = 20000
    label_list = np.random.choice(N, sample_num)
    S, T = S_raw[label_list], T_raw[label_list]
    return S, T


def get_simi(S_raw, T_raw, _type="Pearson", sample_strategy='fixed'):
    if _type != "Pearson" and _type != "Spearman":
        return 0, 0
    n_S = len(S_raw)
    n_T = len(T_raw)
    if n_S != n_T:
        return -1
    result_l = []
    for i in range(1000):
        S, T = bootstrapping(S_raw, T_raw, sample_strategy)
        corr_simi = 0
        if _type == "Pearson":
            corr_simi = scistat.pearsonr(S, T)[0]
        elif _type == "Spearman":
            corr_simi = scistat.spearmanr(S, T)[0]
        result_l.append(corr_simi)
    avg, err = np.mean(result_l), np.std(result_l)
    return avg, err


def main():
    mood_dict = read_users_mood("10_graph.txt")
    fout_pearson = file("results/Pearson.txt", 'w')
    fout_spearman = file("results/Spearman.txt", 'w')
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
            print("sequence length: %d" % len(S))
            P_simi, P_error = get_simi(S, T, "Pearson")
            S_simi, S_error = get_simi(S, T, "Spearman")
            pearson_simis.append((P_simi, P_error))
            spearman_simis.append((S_simi, S_error))
        fout_pearson.write("%d" % distance)
        fout_spearman.write("%d" % distance)
        for mood in range(4):
            fout_pearson.write('\t%f,%f' % pearson_simis[mood])
            fout_spearman.write('\t%f,%f' % spearman_simis[mood])
        fout_pearson.write('\n')
        fout_spearman.write('\n')
    fout_pearson.close()
    fout_spearman.close()


def draw_chart():
    def read_file(fpath):
        corr_simis = {}
        corr_errs = {}
        with open(fpath) as f:
            f.readline()
            for line in f:
                line_arr = line.strip().split('\t')
                distance = int(line_arr[0])
                for i in range(1, 5):
                    mood = i - 1
                    simi, error = line_arr[i].split(',')
                    corr_simis.setdefault(mood, {})
                    corr_errs.setdefault(mood, {})
                    corr_simis[mood][distance] = float(simi)
                    corr_errs[mood][distance] = float(error)
        return corr_simis, corr_errs
    plt.figure(figsize=(16, 7))
    plt.subplot(1, 2, 1)
    corr_simis, corr_errs = read_file("results/Pearson.txt")
    legends = {0: 'Anger', 1:'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        errs = [corr_errs[mood][distance] for distance in x]
        plt.errorbar(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                     yerr=errs, linewidth=2, capsize=15, markersize=10, fillstyle='none', markeredgewidth=2)
    plt.xlabel('$h$', fontsize=25)
    plt.ylabel('$C_p$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='best', fontsize=25)
    plt.title('(a) Pearson correlation', y=-0.2, fontsize=25)
    plt.xlim(0, 7)

    plt.subplot(1, 2, 2)
    corr_simis, corr_errs = read_file("results/Spearman.txt")
    legends = {0: 'Anger', 1: 'Disgust', 2: 'Joy', 3: 'Sadness'}
    markers = ['o', 'D', 's', '^', 'c*-', 'mx-', 'yp-', 'g+-']
    colors = ['red', 'black', 'green', 'blue']
    for mood in range(4):
        x = sorted(corr_simis[mood].keys())
        y = [corr_simis[mood][distance] for distance in x]
        errs = [corr_errs[mood][distance] for distance in x]
        plt.errorbar(x, y, marker=markers[mood], label=legends[mood], color=colors[mood],
                     yerr=errs, linewidth=2, capsize=15, markersize=10, fillstyle='none', markeredgewidth=2)
    plt.xlabel('$h$', fontsize=25)
    plt.ylabel('$C_s$', fontsize=25)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(loc='best', fontsize=25)
    plt.title('(b) Spearman correlation', y=-0.2, fontsize=25)
    plt.xlim(0, 7)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # main()
    draw_chart()
