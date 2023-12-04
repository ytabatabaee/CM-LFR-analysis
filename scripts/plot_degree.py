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


'''def plot_degree_dist(df_emp, df_lfr, r, name):
    plt.cla()
    plt.grid(linestyle='--', linewidth=0.5)
    df_emp['log10(count)'] = np.log10(df_emp['count'])
    df_emp['log10(degree)'] = np.log10(df_emp['degree'])
    df_lfr['log10(count)'] = np.log10(df_lfr['count'])
    df_lfr['log10(degree)'] = np.log10(df_lfr['degree'])
    sns.scatterplot(data=df_emp, y="log10(count)", x="log10(degree)", linewidth=0, color='black', alpha=0.8, label='Empirical network')
    sns.scatterplot(data=df_lfr, y="log10(count)", x="log10(degree)", linewidth=0, color='turquoise', alpha=0.8, label='LFR network')
    plt.title(name_map[name])
    plt.xlabel('log10 (degree)')
    plt.ylabel('log10 (node count)')
    plt.savefig(name + '_degree_'+r+'.pdf')'''


def plot_degree_dist(ax, df_emp, df_lfr, r, name):
    ax.cla()
    ax.grid(linestyle='--', linewidth=0.5)
    '''df_emp['log10(count)'] = np.log10(df_emp['count'])
    df_emp['log10(degree)'] = np.log10(df_emp['degree'])
    df_lfr['log10(count)'] = np.log10(df_lfr['count'])
    df_lfr['log10(degree)'] = np.log10(df_lfr['degree'])'''
    sns.scatterplot(ax=ax, data=df_emp, y="count", x="degree", linewidth=0, color='black', alpha=0.7, label='Empirical network')
    sns.scatterplot(ax=ax, data=df_lfr, y="count", x="degree", linewidth=0, color='turquoise', alpha=0.7, label='LFR network')
    ax.set_title(name_map[name])
    ax.set_yscale('log')
    ax.set_xscale('log')
    #ax.set_xlabel('log10 (degree)')
    #ax.set_ylabel('log10 (node count)')

def vertical_line_10(**kwargs):
    plt.grid(linestyle='--', linewidth=0.5)
    #plt.axvline(10, linestyle = '--', color='grey', ls='--', lw=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ploting degree and community size distribution.')
    #parser.add_argument('-n', metavar='net', type=str, required=True,
    #                   help='network name')
    args = parser.parse_args()

    r = '01'
    '''lfr_net = nx.read_edgelist('S2_' + args.n + '_leiden.0.' + r + '_i2_clustering_lfr/' + 'network_cleaned.dat',
                               nodetype=int)
    degrees_lfr = [d for _, d in lfr_net.degree()]
    degree_dfs_lfr = pd.Series(Counter(degrees_lfr)).sort_index().rename_axis('degree').reset_index(name='count')
    degree_dfs_lfr.to_csv('S2_' + args.n + '_leiden.0.' + r + '_i2_clustering_lfr/' + 'network_cleaned_degrees.tsv')'''


    net_list = ["oc", "cen", "cit_patents", "cit_hepph", "wiki_topcats", "wiki_talk"]
    
    # fig, axes = plt.subplots(3, 2, figsize=(12, 15))

    all_dfs = pd.DataFrame()

    for net in net_list:
        df = pd.read_csv(net + '_cleaned_degrees.csv')
        df['name'] = net
        df['type'] = 'Empirical'
        all_dfs = all_dfs.append(df)
        df = pd.read_csv('S2_' + net + '_leiden.0.' + r + '_i2_clustering_lfr/' + 'network_cleaned_degrees.tsv')
        df['name'] = net
        df['type'] = 'LFR'
        all_dfs = all_dfs.append(df)

    all_dfs['name'] = all_dfs['name'].str.replace('cen', 'CEN')
    all_dfs['name'] = all_dfs['name'].str.replace('oc', 'open_citations')

    '''g = sns.FacetGrid(all_dfs, col="name", margin_titles=True, height=5.5, col_wrap=2)
    g.map_dataframe(sns.scatterplot, x="degree", y="count", hue='type', palette='Dark2', alpha=0.55, linewidth=0).set(
        yscale='log', xscale='log')
    g.map(vertical_line_10)
    g.set_xlabels("")  # number of genes
    g.set_ylabels("")  # ("Species Tree Error (nCD)")
    g.set_titles(row_template='\n{row_name}', col_template='\n{col_name}', size=16)
    g.fig.subplots_adjust(top=0.9, bottom=0.16, left=0.14)
    g.fig.text(0.4, 0.13, s='Degree', fontsize=16)
    g.fig.text(0.08, 0.45, s='Count', rotation=90, fontsize=16)
    # g.add_legend(fontsize=16)
    g.add_legend(bbox_to_anchor=(0.45, 0.96), fontsize=16, loc='upper center', ncol=2, frameon=True)'''

    '''for i in range(3):
        for j in range(2):
            net = net_list[i][j]
            degree_df = pd.read_csv(net + '_cleaned_degrees.csv')
            degree_dfs_lfr = pd.read_csv('S2_' + net + '_leiden.0.' + r + '_i2_clustering_lfr/' + 'network_cleaned_degrees.tsv')
            plot_degree_dist(axes[i, j], degree_df, degree_dfs_lfr, r, net)'''
    
    all_dfs.to_csv('all_degrees.csv')

    #plt.savefig('all_degrees.pdf', bbox_inches='tight')

    '''net = nx.read_edgelist('yasamin/'+args.n+'_cleaned.tsv', nodetype=int)
    degrees = [d for _, d in net.degree()]
    degree_df = pd.Series(Counter(degrees)).sort_index().rename_axis('degree').reset_index(name='count')
    degree_df.to_csv('yasamin/'+args.n+'_cleaned_degrees.csv')'''
    #degree_df = pd.read_csv('yasamin/'+args.n+'_cleaned_degrees.csv')

    # S2_cit_patents_leiden.0.01_i2_clustering_lfr


    #degree_dfs_lfr = pd.read_csv('yasamin/' + args.n + '_leiden.' + r + '_lfr/' + 'network_cleaned_degrees.tsv')

    #plot_degree_dist(degree_df, degree_dfs_lfr, r, args.n)

