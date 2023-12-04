import multiprocessing as mp
import subprocess
import sys
import json
import os
import pandas as pd
import networkx as nx
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
    #df = pd.read_csv('lfr_accuracy.csv')#, sep='\t')
    df = pd.read_csv('lfr_accuracy_node_count.csv')#, encoding='latin-1')  # , sep='\t')
    #df = pd.read_csv('disconnected_clusters.csv')  # , sep='\t')
    #df = pd.read_csv('cm_stats.csv')  # , sep='\t')
    print(df)
    #df['net'] = df['net'].str.replace('cen', 'CEN')
    #df['net'] = df['net'].str.replace('oc', 'open_citations')
    #df['net_name'] = df['net_name'].str.replace('wiki_talk', 'Wikipedia talk')
    #df['net_name'] = df['net_name'].str.replace('wiki_topcats', 'Wikipedia hyperlinks')

    #df['type'] = df['type'].str.replace('gt', 'LFR ground-truth')
    #df['type'] = df['type'].str.replace('leiden-lfr', 'Leiden clustering of LFR')
    #df['type'] = df['type'].str.replace('leiden-orig', 'Original Leiden clustering')
    #df['net_name'] = df['net_name'].str.replace('cit_patents', 'Patents')
    #df['net_name'] = df['net_name'].str.replace('cit_hepph', 'High energy physics')
    #df['proportion_well_connected_gt'] = 100 * df['proportion_well_connected_gt']
    #df['proportion_small_clusters_gt'] = 100 * df['proportion_small_clusters_gt']
    #df['proportion_disconnected_gt'] = 100 * df['proportion_disconnected_gt']
   # df['proportion_disconnected'] = 100 * df['proportion_disconnected']
    #df['proportion_not_well_connected'] = 100 - 100 * df['proportion_well_connected']
    #df['proportion_small_clusters'] = 100 * df['proportion_small_clusters']
    #df['node_coverage_10'] = 100 * df['node_coverage_10']
    #g = sns.FacetGrid(df[df['type']!='leiden-lfr'], col="net", margin_titles=True, height=4.5, col_wrap=3,
    #                  row_order=['open_citations','CEN','cit_patents','cit_hepph','wiki_topcats','wiki_talk', 'orkut'])
    g = sns.FacetGrid(df, col="res", margin_titles=True, height=4.5, col_wrap=3, aspect=1.3,
                     row_order=['open_citations','CEN','cit_patents','cit_hepph','wiki_topcats','wiki_talk', 'orkut'])
    g.map_dataframe(sns.pointplot, x="count", y="ARI", hue='type', palette='Dark2', order=['2K', '5K', '10K', '20K', '50K', '100K', '200K', '500K', '1M'])
    g.set_xlabels("")  # number of genes
    g.set_ylabels("")  # ("Species Tree Error (nCD)")
    g.set_titles(row_template='{row_name}',col_template='{col_name}', size=22)
    g.fig.subplots_adjust(top=0.8, bottom=0.16, left=0.14)
    #g.fig.text(0.5, 0.06, s='Mixing parameter', fontsize=22)
    g.fig.text(0.4, 0.06, s='Network size', fontsize=22)
    #g.fig.text(0.095, 0.2, s='Normalized mutual information (NMI)', rotation=90, fontsize=22)
    #g.fig.text(0.105, 0.31, s='Node coverage (%)', rotation=90, fontsize=22)
    #g.fig.text(0.095, 0.2, s='Adjusted mutual information (AMI)', rotation=90, fontsize=22)
    g.fig.text(0.095, 0.25, s='Adjusted Rand index (ARI)', rotation=90, fontsize=22)
    #g.fig.text(0.095, 0.4, s='F1-score', rotation=90, fontsize=22)
    #g.fig.text(0.09, 0.3, s='Not well-connected clusters (%)', rotation=90, fontsize=14)
    #g.fig.text(0.085, 0.28, s='Disconnected clusters (%)', rotation=90, fontsize=22)
    #g.fig.text(0.105, 0.32, s='Small Clusters (%)', rotation=90, fontsize=20)
    #g.set(ylim=(0.5, None))
    #g.fig.text(0.09, 0.4, s='log10 (Cluster count)', rotation=90, fontsize=14)
    g.set_xticklabels(fontsize=16, rotation=30)
    plt.subplots_adjust(hspace=0.2)
   # g.fig.tight_layout()
    #g.set_yticklabels(fontsize=16)
    #g.set_yticklabels(fontsize=13)
    g.add_legend(bbox_to_anchor=(0.44, 0.92), fontsize=20, loc='upper center', ncol=2, frameon=True)
    #g.add_legend(bbox_to_anchor=(0.44, 0.92), fontsize=22, loc='upper center', ncol=2, frameon=True)
    #plt.savefig('proportion_disconnected.pdf', bbox_inches='tight')
    #plt.savefig('proportion_small.pdf', bbox_inches='tight')
    #plt.savefig('proportion_disconnected.pdf', bbox_inches='tight')
    #plt.savefig('node_coverage.pdf', bbox_inches='tight')
    plt.savefig('ari_nc.pdf', bbox_inches='tight')


