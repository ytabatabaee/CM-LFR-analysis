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


'''def plot_cm_steps(step1, step2, step3, step4, r, name):
    fig, axes = plt.subplots(1, 4, figsize=(12, 15))
    plt.cla()
    plt.grid(linestyle='--', linewidth=0.5)
    step1['log10(count)'] = np.log10(step1['count'])
    step1['log10(x)'] = np.log10(step1['x'])
    step2['log10(count)'] = np.log10(step2['count'])
    step2['log10(x)'] = np.log10(step2['x'])
    step3['log10(count)'] = np.log10(step3['count'])
    step3['log10(x)'] = np.log10(step3['x'])
    step4['log10(count)'] = np.log10(step4['count'])
    step4['log10(x)'] = np.log10(step4['x'])
    sns.scatterplot(ax=axes[0], data=step1, y="log10(count)", x="log10(x)", linewidth=0, color='black', alpha=0.5, label='Leiden clustering')
    sns.scatterplot(ax=axes[1], data=step2, y="log10(count)", x="log10(x)", linewidth=0, color='turquoise', alpha=0.5, label='Filtering trees and small clusters')
    sns.scatterplot(ax=axes[2], data=step3, y="log10(count)", x="log10(x)", linewidth=0, color='#c51b8a', alpha=0.5, label='Connectivity-Modifier (CM)')
    sns.scatterplot(ax=axes[3], data=step4, y="log10(count)", x="log10(x)", linewidth=0, color='orange', alpha=0.5,label='Filtering small clusters')
    # plt.title('Community size distribution for ' + name)
    plt.xlim(left=0)
    plt.vlines(x=1, ymin=0, ymax=5, colors='grey', ls='--', lw=1)
    # plt.text(0.65, 1, 'cluster size = 10', fontsize=10)
    plt.legend(loc='upper right')
    plt.title('CM pipeline - '+ name_map[name]+ ' - r=0.'+r)
    plt.xlabel('log10 (cluster size)')
    plt.ylabel('log10 (cluster count)')
    plt.savefig(name + '_cm_steps_lfr_'+r+'.pdf', bbox_inches='tight')'''


def plot_cm_steps(axes, step1, step2, step4, r, name):
    for ax in axes:
        ax.cla()
    step1['log10(count)'] = np.log10(step1['count'])
    step1['log10(x)'] = np.log10(step1['x'])
    step2['log10(count)'] = np.log10(step2['count'])
    step2['log10(x)'] = np.log10(step2['x'])
    #step3['log10(count)'] = np.log10(step3['count'])
    #step3['log10(x)'] = np.log10(step3['x'])
    step4['log10(count)'] = np.log10(step4['count'])
    step4['log10(x)'] = np.log10(step4['x'])
    sns.scatterplot(ax=axes[0], data=step1, y="log10(count)", x="log10(x)", linewidth=0, color='black', alpha=1)
    #axes[0,0].set_title('Leiden clustering')
    sns.scatterplot(ax=axes[1], data=step2, y="log10(count)", x="log10(x)", linewidth=0, color='cornflowerblue', alpha=1)# label='Filtering')
    #axes[0,1].set_title('Filtering')
    #sns.scatterplot(ax=axes[2], data=step3, y="log10(count)", x="log10(x)", linewidth=0, color='#c51b8a', alpha=1, label='Connectivity-Modifier (CM)')
    sns.scatterplot(ax=axes[2], data=step4, y="log10(count)", x="log10(x)", linewidth=0, color='#c51b8a', alpha=1)#,label='Connectivity-Modifier (CM) + Filtering')
    #axes[0,2].set_title('CM + Filtering')
    for i in range(3):
        axes[i].set_xlim(left=-0.1, right=3.8)
        axes[i].vlines(x=1, ymin=0, ymax=5, colors='grey', ls='--', lw=1)
        axes[i].grid(linestyle='--', linewidth=0.5)
        #axes[i].set_xlabel('log10 (cluster size)')
        #axes[i].set_ylabel('log10 (cluster count)')
        axes[i].set_xlabel(None)
        axes[i].set_ylabel(None)
        #axes[i].get_legend().remove()


def plot_resolution_dist(dfs, resolutions, name):
    plt.cla()
    plt.grid(linestyle='--', linewidth=0.5)
    colors = ['black', 'turquoise', 'pink', 'orange']
    for i in range(len(resolutions)):
        dfs[i]['log10(count)'] = np.log10(dfs[i]['count'])
        dfs[i]['log10(x)'] = np.log10(dfs[i]['x'])
        sns.scatterplot(data=dfs[i], y="log10(count)", x="log10(x)", linewidth=0, color=colors[i], alpha=0.8,
                        label='Leiden clustering (r=0.'+resolutions[i]+')')
        plt.title('Community size distribution for ' + name)
        #plt.xlabel('log10 (cluster size)')
        #plt.ylabel('log10 (node count)')
        plt.xlabel('')
        plt.ylabel('')
        plt.savefig(name + '_cm_size_res.pdf')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ploting degree and community size distribution.')
    parser.add_argument('-n', metavar='net', type=str, required=True,
                        help='network name')
    args = parser.parse_args()

    net = nx.read_edgelist('yasamin/'+args.n+'_cleaned.tsv', nodetype=int)

    '''
    degrees = [d for _, d in net.degree()]
    degree_df = pd.Series(Counter(degrees)).sort_index().rename_axis('x').reset_index(name='count')'''

    resolutions = ["001", "01", "1", "5"]
    cm_size_dfs = [None] * len(resolutions)
    cm_size_dfs_lfr = [None] * len(resolutions)
    cm_size_dfs_lfr_leiden = [None] * len(resolutions)
    degree_dfs_lfr = [None] * len(resolutions)

    header_cm = 'yasamin/'+args.n+'_processed_cm/'

    plt.cla()
    fig, axes = plt.subplots(2, 3, figsize=(11, 6))

    for i in range(len(resolutions)):
        r = resolutions[i]
        header = 'yasamin/'+args.n+'_leiden.'+r+'_lfr/'

        lfr_net = nx.read_edgelist(header + 'network_cleaned.tsv', nodetype=int)
        #degrees_lfr = [d for _, d in lfr_net.degree()]
        #degree_dfs_lfr[i] = pd.Series(Counter(degrees_lfr)).sort_index().rename_axis('x').reset_index(name='count')

        '''lfr_net = nx.read_edgelist('yasamin/'+args.n + '_leiden.' + r + '_lfr/network_cleaned.tsv', nodetype=int)
        degrees_lfr = [d for _, d in lfr_net.degree()]
        degree_dfs_lfr[i] = pd.Series(Counter(degrees_lfr)).sort_index().rename_axis('x').reset_index(name='count')

        plot_degree_dist(degree_df, degree_dfs_lfr[i], r, args.n)'''

        '''partition = membership_to_partition(get_membership_list_from_file(net, args.n + '_leiden.' + r + '.tsv'))
        cluster_sizes = [len(c) for c in partition]
        cm_size_dfs[i] = pd.Series(Counter(cluster_sizes)).sort_index().rename_axis('x').reset_index(name='count')'''

        '''

        lfr_partition = membership_to_partition(get_membership_list_from_file(lfr_net, args.n + '_leiden.' + r + '_lfr/community.dat'))
        cluster_sizes_lfr = [len(c) for c in lfr_partition]
        cm_size_dfs_lfr[i] = pd.Series(Counter(cluster_sizes_lfr)).sort_index().rename_axis('x').reset_index(name='count')

        lfr_leiden_partition = membership_to_partition(get_membership_list_from_file(lfr_net, args.n + '_leiden.' + r + '_lfr/leiden.'+r+'_lfr.tsv'))
        cluster_sizes_lfr_leiden = [len(c) for c in lfr_leiden_partition]
        cm_size_dfs_lfr_leiden[i] = pd.Series(Counter(cluster_sizes_lfr_leiden)).sort_index().rename_axis('x').reset_index(name='count')

        plot_cm_dist(cm_size_dfs[0], cm_size_dfs_lfr[0], cm_size_dfs_lfr_leiden[0], args.n, r)'''


        partition1 = membership_to_partition(get_membership_list_from_file(net, header_cm + args.n + '_leiden.' + r + '.tsv'))
        cluster_sizes1 = [len(c) for c in partition1]
        step1 = pd.Series(Counter(cluster_sizes1)).sort_index().rename_axis('x').reset_index(name='count')
        step1.to_csv(header_cm + args.n + '_leiden.' + r + '_csizes.tsv')
        step1 = pd.read_csv(header_cm + args.n + '_leiden.' + r + '_csizes.tsv')

        partition2 = membership_to_partition(get_membership_list_from_file(net, header_cm + args.n + '_leiden.' + r + '_nontree_n10_clusters.tsv'))
        cluster_sizes2 = [len(c) for c in partition2]
        step2 = pd.Series(Counter(cluster_sizes2)).sort_index().rename_axis('x').reset_index(name='count')
        step2.to_csv(header_cm + args.n + '_leiden.' + r + '_nontree_n10_clusters_csizes.tsv')
        step2 = pd.read_csv(header_cm + args.n + '_leiden.' + r + '_nontree_n10_clusters_csizes.tsv')


        '''partition3 = membership_to_partition(get_membership_list_from_file(net, header_cm+ args.n + '_leiden.' + r + '_after.tsv'))
        cluster_sizes3 = [len(c) for c in partition3]
        step3 = pd.Series(Counter(cluster_sizes3)).sort_index().rename_axis('x').reset_index(name='count')'''

        partition4 = membership_to_partition(get_membership_list_from_file(net, header_cm + args.n + '_leiden.' + r + '_r2nontree_n10_clusters.tsv'))
        cluster_sizes4 = [len(c) for c in partition4]
        step4 = pd.Series(Counter(cluster_sizes4)).sort_index().rename_axis('x').reset_index(name='count')
        step4.to_csv(header_cm + args.n + '_leiden.' + r + '_r2nontree_n10_clusters_csizes.tsv')
        step4 = pd.read_csv(header_cm + args.n + '_leiden.' + r + '_r2nontree_n10_clusters_csizes.tsv')

        plot_cm_steps(axes[0], step1, step2, step4, r, args.n)

        #partition1 = membership_to_partition(get_membership_list_from_file(lfr_net, header + 'leiden.'+r+'_lfr.tsv'))
        #cluster_sizes1 = [len(c) for c in partition1]
        #step1 = pd.Series(Counter(cluster_sizes1)).sort_index().rename_axis('x').reset_index(name='count')
        #step1.to_csv(header + 'leiden.'+r+'_lfr_csizes.csv')
        step1 = pd.read_csv(header + 'leiden.'+r+'_lfr_csizes.csv')

        #partition2 = membership_to_partition(get_membership_list_from_file(lfr_net, header + 'leiden.'+r+'_lfr_nontree_n10_clusters.tsv'))
        #cluster_sizes2 = [len(c) for c in partition2]
        #step2 = pd.Series(Counter(cluster_sizes2)).sort_index().rename_axis('x').reset_index(name='count')
        #step2.to_csv(header + 'leiden.'+r+'_lfr_nontree_n10_clusters_csizes.csv')
        step2 = pd.read_csv(header + 'leiden.'+r+'_lfr_nontree_n10_clusters_csizes.csv')

        '''partition3 = membership_to_partition(get_membership_list_from_file(lfr_net, header + 'cm_leiden.'+r+'_lfr_after.tsv'))
        cluster_sizes3 = [len(c) for c in partition3]
        step3 = pd.Series(Counter(cluster_sizes3)).sort_index().rename_axis('x').reset_index(name='count')
        step3.to_csv(header + 'cm_leiden.'+r+'_lfr_after_csizes.csv')'''

        #partition4 = membership_to_partition(get_membership_list_from_file(lfr_net, header + 'cm_leiden.'+r+'_lfr_r2nontree_n10_clusters.tsv'))
        #cluster_sizes4 = [len(c) for c in partition4]
        #step4 = pd.Series(Counter(cluster_sizes4)).sort_index().rename_axis('x').reset_index(name='count')
        #step4.to_csv(header + 'cm_leiden.'+r+'_lfr_r2nontree_n10_clusters_csizes.csv')
        step4 = pd.read_csv(header + 'cm_leiden.'+r+'_lfr_r2nontree_n10_clusters_csizes.csv')

        plot_cm_steps(axes[1], step1, step2, step4, r, args.n)

        axes[0, 0].set_title('Leiden clustering', fontweight="bold", fontsize=14)
        axes[0, 1].set_title('Filtering', fontweight="bold", fontsize=14)
        axes[0, 2].set_title('CM + Filtering', fontweight="bold", fontsize=14)
        fig.text(0.43, 0.04, s='log10 (cluster size)', fontsize=14)
        fig.text(0.085, 0.35, s='log10 (cluster count)', rotation=90, fontsize=14)
        fig.text(0.065, 0.25, s='LFR', rotation=90, fontweight="bold", fontsize=14)
        fig.text(0.065, 0.65, s='Empirical', rotation=90, fontweight="bold", fontsize=14)

        #plt.suptitle('CM pipeline - '+ name_map[args.n]+ ' - r=0.'+r)
        plt.savefig(args.n + '_cm_steps_lfr'+r+'.pdf', bbox_inches='tight')

    #plot_resolution_dist(cm_size_dfs, resolutions, args.n)

