import multiprocessing as mp
import subprocess
import sys
import json
import os
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1], low_memory=False)[:-1]
    print('mean normalized connectivity:', df['connectivity_normalized'].mean())
    print(df['connectivity_normalized'][df['connectivity_normalized'] >= 1.0].count())
    print(df['connectivity_normalized'].count())
    print('proportion well-connected clusters:', (df['connectivity_normalized'][df['connectivity_normalized'] >= 1.0].count())/df['connectivity_normalized'].count())
    df_filtered = df[df['n']>10]
    print(len(df), len(df_filtered))
    print('proportion well-connected clusters (>10):',
          (df_filtered['connectivity_normalized'][df_filtered['connectivity_normalized'] >= 1.0].count()) / df_filtered[
              'connectivity_normalized'].count())
    print('proportion small (<= 10) clusters:',(df['n'][df['n'] <= 10].count()) / df['n'].count())
    print('proportion disconnected:', (df['connectivity_normalized'][df['connectivity_normalized'] == 0].count())/df['connectivity_normalized'].count())
    print(df)
    print(df_filtered['n'].sum(), df['n'].sum())
    print(df_filtered['n'])
    print(df['n'])
    print('node coverage (>10)', df_filtered['n'].sum() / df['n'].sum())
    #print(len(df['connectivity_normalized']) / )