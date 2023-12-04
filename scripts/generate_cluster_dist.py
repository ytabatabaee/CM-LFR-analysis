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
            if net is None:
                membership[int(i)] = m
            elif int(i) in net.nodes:
                membership[int(i)] = m
    return membership


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate community size distribution.')
    parser.add_argument('-n', metavar='net', type=str, required=True,
                        help='network name')
    args = parser.parse_args()

    resolutions = ["0.0001", "0.001", "0.01", "0.1", "0.5", "modularity"]
    net = args.n
    #net_list = ["oc", "cen", "cit_patents", "cit_hepph", "wiki_topcats", "wiki_talk"]

    for r in resolutions:
        if r == 'modularity':
            r_str = '_modularity'
        else:
            r_str = '.' + r
        print(r)
        try:
            edgelist_lfr = nx.read_edgelist('/shared/cm_paper_composite_view/' + net + '_lfr_' + r + '_cleaned.tsv', nodetype=int)
            partition = membership_to_partition(get_membership_list_from_file(edgelist_lfr, '/shared/yasamin/' + 'S2_'+net+'_leiden'+r_str+'_i2_clustering_lfr/community.dat'))
            cluster_sizes = [len(c) for c in partition]
            df = pd.Series(Counter(cluster_sizes)).sort_index().rename_axis('x').reset_index(name='count')
            df.to_csv('/shared/yasamin/' + 'S2_'+net+'_leiden'+r_str+'_i2_clustering_lfr/community_csizes.tsv')

        except Exception as e:
            print(str(e))
            continue

