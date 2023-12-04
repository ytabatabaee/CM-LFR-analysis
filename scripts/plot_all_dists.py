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


def plot_cm_steps(axes, dfs, dfs_lfr, name):
    for ax in axes:
        ax.cla()
    #step3['log10(count)'] = np.log10(step3['count'])
    #step3['log10(x)'] = np.log10(step3['x'])
    for i in range(len(dfs)):
        sns.scatterplot(ax=axes[i], data=dfs[i], y="count", x="x", linewidth=0, color='black', alpha=0.5)
        try:
            sns.scatterplot(ax=axes[i], data=dfs_lfr[i], y="count", x="x", linewidth=0, color='cornflowerblue', alpha=0.5)
        except:
            print('error for ', name)
        #axes[i].set_xlim(left=-0.1, right=3.8)
        axes[i].vlines(x=10, ymin=0, ymax=5, colors='grey', ls='--', lw=1)
        axes[i].grid(linestyle='--', linewidth=0.5)
        #axes[i].set_xlabel('log10 (cluster size)')
        #axes[i].set_ylabel('log10 (cluster count)')
        axes[i].set_xlabel(None)
        axes[i].set_ylabel(None)
        axes[i].set_yscale('log')
        axes[i].set_xscale('log')
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

def vertical_line_10(**kwargs):
    plt.grid(linestyle='--', linewidth=0.2)
    #plt.axvline(10, linestyle = '--', color='grey', ls='--', lw=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ploting degree and community size distribution.')
    #parser.add_argument('-n', metavar='net', type=str, required=True,
    #                    help='network name')
    args = parser.parse_args()

    resolutions = ["modularity", "0.0001", "0.001", "0.01", "0.1", "0.5"]
    net_list = ["oc", "cen", "cit_patents", "cit_hepph", "wiki_topcats", "wiki_talk", "orkut"]

    plt.cla()
    #fig, axes = plt.subplots(7, 6, figsize=(21, 18))

    all_dfs = pd.DataFrame()

    for net in net_list:
        df_all_res = []
        df_lfr_all_res = []
        for r in resolutions:
            if r == 'modularity':
                r_str = '_modularity'
            else:
                r_str = '.' + r
            df = pd.read_csv('S2_' + net + '_leiden' + r_str + '_i2_clustering_csizes.tsv')
            df['res'] = r
            df['type'] = 'Original Leiden clustering'
            df['name'] = net
            all_dfs = all_dfs.append(df)
            try:
                df = pd.read_csv(
                    '/shared/yasamin/' + 'S2_' + net + '_leiden' + r_str + '_i2_clustering_lfr/community_csizes.tsv')
                df['res'] = r
                df['type'] = 'LFR ground-truth'
                df['name'] = net
                all_dfs = all_dfs.append(df)

                df = pd.read_csv('S2_' + net + '_lfr_leiden' + r_str + '_i2_clustering_csizes.tsv')
                df['res'] = r
                df['type'] = 'Leiden clustering of LFR'
                df['name'] = net
                all_dfs = all_dfs.append(df)

            except:
                print('error for ', net, r)

        #plot_cm_steps(axes[net_list.index(net)], df_all_res, df_lfr_all_res, net)
    print(all_dfs)

    #sns.set_style('whitegrid')
    # =sns.color_palette(['black', 'turquoise', 'orange']),

    all_dfs['name'] = all_dfs['name'].str.replace('cen', 'CEN')
    all_dfs['name'] = all_dfs['name'].str.replace('oc', 'open_citations')
    '''g = sns.FacetGrid(all_dfs, col="res", row="name", margin_titles=True, height=2.5,
                      row_order=['open_citations', 'CEN', 'cit_patents', 'cit_hepph', 'wiki_topcats', 'wiki_talk',
                                 'orkut'],
                      col_order=['0.5', '0.1', '0.01', '0.001', '0.0001', 'modularity'])
    g.map_dataframe(sns.scatterplot, x="x", y="count", hue='type', palette='Dark2', alpha=0.5, linewidth=0).set(yscale = 'log', xscale='log')
    g.map(vertical_line_10)
    g.set_xlabels("")  # number of genes
    g.set_ylabels("")  # ("Species Tree Error (nCD)")
    g.set_titles(row_template='{row_name}', col_template='{col_name}\n', size=16)
    g.fig.subplots_adjust(top=0.8, bottom=0.16, left=0.14)
    g.fig.text(0.4, 0.13, s='Cluster size', fontsize=16)
    g.fig.text(0.095, 0.4, s='Cluster count', rotation=90, fontsize=16)
    #g.add_legend(fontsize=16)
    g.add_legend(bbox_to_anchor=(0.35, 0.87), fontsize=16, loc='upper center', ncol=3, frameon=True)'''

    '''axes[0, 0].set_title('Leiden clustering', fontsize=14)
    axes[0, 1].set_title('Filtering', fontweight="bold", fontsize=14)
    axes[0, 2].set_title('CM + Filtering', fontweight="bold", fontsize=14)
    fig.text(0.43, 0.04, s='log10 (cluster size)', fontsize=14)
    fig.text(0.085, 0.35, s='log10 (cluster count)', rotation=90, fontsize=14)
    fig.text(0.065, 0.25, s='LFR', rotation=90, fontweight="bold", fontsize=14)
    fig.text(0.065, 0.65, s='Empirical', rotation=90, fontweight="bold", fontsize=14)'''

        #plt.suptitle('CM pipeline - '+ name_map[args.n]+ ' - r=0.'+r)
    #plt.savefig('all_cm_distributions.pdf', bbox_inches='tight')
    all_dfs.to_csv('all_cm_distributions.csv')

