import multiprocessing as mp
import subprocess
import sys
import json
import os
import pandas as pd

dataset_path = './'


if __name__ == '__main__':
    nets = ["oc", "cen", "orkut", "wiki_talk", "wiki_topcats", "cit_hepph", "cit_patents"]
    resolutions = ["0.0001", "0.001", "0.01", "0.1", "0.5", "modularity"]
    # S2_cit_hepph_leiden.0.5_i2_clustering_lfr
    df = pd.DataFrame()
    for net in nets:
        for r in resolutions:
            if r == "modularity":
                r_str = '_' + r
            else:
                r_str = '.' + r
            try:
                with open(dataset_path + 'S2_' + net+'_leiden'+r_str+'_i2_clustering.json') as f:
                    stats = json.load(f)
                df_stats = pd.json_normalize(stats)
                df_stats.insert(loc=0, column='name', value=net+'_leiden.'+r+'.tsv')
                df = df.append(df_stats, ignore_index=True)
            except Exception as e:
                print(str(e))
                continue

            try:
                with open(dataset_path + 'S2_' + net+'_leiden'+r_str+'_i2_clustering_lfr/community.dat.json') as f:
                    stats = json.load(f)
                df_stats = pd.json_normalize(stats)
                df_stats.insert(loc=0, column='name', value=net+'_lfr_gt.'+r+'.tsv')
                df = df.append(df_stats, ignore_index=True)
            except Exception as e:
                print(str(e))
                continue
    #df.to_csv('network_params.csv')
    df.to_csv('network_params_lfr.csv')

