import argparse
import json
import math
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
from networkx.algorithms.community import modularity

name_map = {"cen": "Curated Exosome citation network (CEN)",
                "oc": "Open Citations network",
                "cit_hepph": "High energy physics citation network",
                "cit_patents":"US patents citation network",
                "wiki_topcats":"Wikipedia hyperlinks network",
                "wiki_talk":"Wikipedia talk (communication) network"}


def membership_to_partition(membership):
    part_dict = {}
    for index, value in membership.items():
        if value in part_dict:
            part_dict[value].append(index)
        else:
            part_dict[value] = [index]
    return part_dict.values()


def get_membership_list_from_file(net, file_name):
    membership = dict()
    with open(file_name) as f:
        for line in f:
            i, m = line.strip().split()
            if int(i) in net.nodes:
                membership[int(i)] = m
    return membership


def plot_cm_dist(ax, df_emp, df_lfr, df_leiden_lfr, name, r):
    ax.cla()
    ax.grid(linestyle='--', linewidth=0.5)
    df_emp['log10(count)'] = np.log10(df_emp['count'])
    df_emp['log10(x)'] = np.log10(df_emp['x'])
    df_lfr['log10(count)'] = np.log10(df_lfr['count'])
    df_lfr['log10(x)'] = np.log10(df_lfr['x'])
    df_leiden_lfr['log10(count)'] = np.log10(df_leiden_lfr['count'])
    df_leiden_lfr['log10(x)'] = np.log10(df_leiden_lfr['x'])
    sns.scatterplot(ax=ax, data=df_emp, y="log10(count)", x="log10(x)", linewidth=0, color='black', alpha=0.9, label='Leiden clustering of empirical net')
    sns.scatterplot(ax=ax, data=df_lfr, y="log10(count)", x="log10(x)", linewidth=0, color='turquoise', alpha=0.9, label='LFR ground-truth communities')
    sns.scatterplot(ax=ax, data=df_leiden_lfr, y="log10(count)", x="log10(x)", linewidth=0, color='orange', alpha=0.9,label='Leiden clustering of LFR net')
    ax.set_title('r=0.'+r)
    if r != '001':
        ax.get_legend().remove()
    else:
        ax.legend(loc='upper center', bbox_to_anchor=(1.16, 1.2), ncol=3, fontsize=12)
    ax.set_xlabel('log10 (cluster size)')
    ax.set_ylabel('log10 (cluster count)')


'''def plot_cm_dist(df_emp, df_lfr, df_leiden_lfr, name, r):
    plt.cla()
    plt.grid(linestyle='--', linewidth=0.5)
    df_emp['log10(count)'] = np.log10(df_emp['count'])
    df_emp['log10(x)'] = np.log10(df_emp['x'])
    df_lfr['log10(count)'] = np.log10(df_lfr['count'])
    df_lfr['log10(x)'] = np.log10(df_lfr['x'])
    df_leiden_lfr['log10(count)'] = np.log10(df_leiden_lfr['count'])
    df_leiden_lfr['log10(x)'] = np.log10(df_leiden_lfr['x'])
    sns.scatterplot(data=df_emp, y="log10(count)", x="log10(x)", linewidth=0, color='black', alpha=0.8, label='Leiden clustering of empirical net')
    sns.scatterplot(data=df_lfr, y="log10(count)", x="log10(x)", linewidth=0, color='turquoise', alpha=0.8, label='LFR ground-truth communities')
    sns.scatterplot(data=df_leiden_lfr, y="log10(count)", x="log10(x)", linewidth=0, color='orange', alpha=0.8,label='Leiden clustering of LFR net')
    plt.title('Community size distribution - '+ name_map[name]+ ' - r=0.'+r)
    plt.xlabel('log10 (cluster size)')
    plt.ylabel('log10 (cluster count)')
    plt.savefig(name+'_'+r+'_cm_size.pdf')'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ploting degree and community size distribution.')
    parser.add_argument('-n', metavar='net', type=str, required=True,
                        help='network name')
    args = parser.parse_args()

    net = nx.read_edgelist('yasamin/'+args.n+'_cleaned.tsv', nodetype=int)
    resolutions = [["001", "01"],
                   ["1", "5"]]
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    for i in range(2):
        for j in range(2):
            r = resolutions[i][j]

            header = 'yasamin/'+args.n+'_leiden.'+r+'_lfr/'

            lfr_net = nx.read_edgelist(header + 'network_cleaned.tsv', nodetype=int)

            partition = membership_to_partition(get_membership_list_from_file(net, 'yasamin/'+ args.n + '_leiden.' + r + '.tsv'))
            cluster_sizes = [len(c) for c in partition]
            cm_size_dfs = pd.Series(Counter(cluster_sizes)).sort_index().rename_axis('x').reset_index(name='count')
            cm_size_dfs.to_csv('yasamin/'+ args.n + '_leiden.' + r + '_csizes.csv')

            lfr_partition = membership_to_partition(get_membership_list_from_file(lfr_net, header+'/community.dat'))
            cluster_sizes_lfr = [len(c) for c in lfr_partition]
            cm_size_dfs_lfr = pd.Series(Counter(cluster_sizes_lfr)).sort_index().rename_axis('x').reset_index(name='count')
            cm_size_dfs_lfr.to_csv(header+'/community'+'_csizes.csv')

            lfr_leiden_partition = membership_to_partition(get_membership_list_from_file(lfr_net, header+'/leiden.'+r+'_lfr.tsv'))
            cluster_sizes_lfr_leiden = [len(c) for c in lfr_leiden_partition]
            cm_size_dfs_lfr_leiden = pd.Series(Counter(cluster_sizes_lfr_leiden)).sort_index().rename_axis('x').reset_index(name='count')
            cm_size_dfs_lfr_leiden.to_csv(header+'/leiden.'+r+'_lfr_csizes.csv')

            plot_cm_dist(axes[i,j], cm_size_dfs, cm_size_dfs_lfr, cm_size_dfs_lfr_leiden, args.n, r)

    plt.suptitle(name_map[args.n], fontsize=13)
    plt.savefig(args.n + '_cm_size.pdf', bbox_inches='tight')

    #plot_resolution_dist(cm_size_dfs, resolutions, args.n)

