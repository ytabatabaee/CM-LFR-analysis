import multiprocessing as mp
import subprocess
import sys
import json
import os
import pandas as pd
import networkx as nx
import numpy as np

dataset_path = './'


def membership_to_partition(membership):
    part_dict = {}
    for index, value in membership.items():
        if value in part_dict:
            part_dict[value].append(index)
        else:
            part_dict[value] = [index]
    return part_dict.values()


def clustering_statistics(name, step, r, net, membership, df):
    partition = membership_to_partition(membership)
    larger_10_clusters = [len(c) for c in partition if len(c) > 10]
    non_singletons = [len(c) for c in partition if len(c) > 1]
    if len(larger_10_clusters) == 0:
        min_size, max_size, mean_size, median_size = 0, 0, 0, 0
    else:
        min_size, max_size, mean_size, median_size = int(np.min(larger_10_clusters)), int(np.max(larger_10_clusters)), \
                                                 np.mean(larger_10_clusters), np.median(larger_10_clusters)
    non_singleton_num = len(non_singletons)
    if name == 'oc':
        node_count = 75025194
    else:
        node_count = net.number_of_nodes()
    node_cov = sum(non_singletons) / node_count
    node_cov_10 = sum(larger_10_clusters) / node_count
    df = df.append({'net_name': name,
                    'step': step,
                    'r':r,
                    'clus_count': non_singleton_num,
                    'clus_count_10': len(larger_10_clusters),
                    'node_cov': node_cov,
                    'node_cov_10': node_cov_10,
                    'mean_size': mean_size,
                    'min_size': min_size,
                    'med_size': median_size,
                    'max_size': max_size},
                   ignore_index=True)
    return df


def get_membership_list_from_file(net, file_name):
    membership = dict()
    with open(file_name) as f:
        for line in f:
            i, m = line.strip().split()
            if net is None:
                membership[int(i)] = m
            elif int(i) in net.nodes:
                membership[int(i)] = m
    return membership


if __name__ == '__main__':
    nets = ["cit_hepph", "orkut", "oc", "cen", "cit_patents", "wiki_topcats", "wiki_talk"]
    resolutions = ["0.0001", "0.001", "0.01", "0.1", "0.5", "modularity"]
    df = pd.DataFrame(columns=['net_name', 'step', 'r', 'clus_count', 'clus_count_10', 'node_cov', 'node_cov_10',
                                 'mean_size', 'min_size', 'med_size', 'max_size'])
    for net in nets:
        print(net)
        if net == 'oc':
            edgelist = None
        else:
            edgelist = nx.read_edgelist(net + '_cleaned.tsv', nodetype=int)
        for r in resolutions:
            if r == 'modularity':
                r_str = '_modularity'
            else:
                r_str = '.'+r
            print(r)
            try:
                membership = get_membership_list_from_file(edgelist, 'S2_'+net+'_leiden'+r_str+'_i2_clustering.tsv')
                df = clustering_statistics(net, 'Leiden', r, edgelist, membership, df)
                membership = get_membership_list_from_file(edgelist, 'S4_'+net+'_leiden'+r_str+'_i2_make_cm_ready.R.tsv')
                df = clustering_statistics(net, 'Filter', r, edgelist, membership, df)
                membership = get_membership_list_from_file(edgelist, 'S6_'+net+'_leiden'+r_str+'_i2_post_cm_filter.R.tsv')
                df = clustering_statistics(net, 'CM+Filter', r, edgelist, membership, df)

                edgelist_lfr = nx.read_edgelist(net+'_lfr_'+r+'_cleaned.tsv', nodetype=int)

                membership = get_membership_list_from_file(edgelist_lfr, 'S2_'+net+'_lfr_leiden'+r_str+'_i2_clustering.tsv')
                df = clustering_statistics(net+'_lfr', 'Leiden', r, edgelist_lfr, membership, df)
                membership = get_membership_list_from_file(edgelist_lfr, 'S4_'+net+'_lfr_leiden'+r_str+'_i2_make_cm_ready.R.tsv')
                df = clustering_statistics(net+'_lfr', 'Filter', r, edgelist_lfr, membership, df)
                membership = get_membership_list_from_file(edgelist_lfr, 'S6_'+net+'_lfr_leiden'+r_str+'_i2_post_cm_filter.R.tsv')
                df = clustering_statistics(net+'_lfr', 'CM+Filter', r, edgelist_lfr, membership, df)
            except:
                df.to_csv('cm_stats.csv')
            df.to_csv('cm_stats.csv')

