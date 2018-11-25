# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 18:24:15 2018

@author: User
"""
import numpy as np
import pandas as pd
import sys, threading
sys.setrecursionlimit(800000)
threading.stack_size(67108864)


def main():
    # file = 'SCC_test.txt'
    # n = 15
    # file = 'SCC_test_class.txt'
    # n = 6
    file = 'SCC.txt'
    n = 875714
    # file = 'input_mostlyCycles_2_8.txt'
    # n = 10
    # file = 'input_mostlyCycles_22_200.txt'
    # n = 200
    # file = 'input_mostlyCycles_30_800.txt'
    # n = 800
    # file = 'input_mostlyCycles_42_6400.txt'
    # n = 6400
    # file = 'input_mostlyCycles_61_160000.txt'
    # n = 160000

    data = pd.read_csv(file, sep=' ', header=None, usecols=[0,1], 
                       names = ['tail', 'head'])

    # minus one to become compatible with Python's array ordering
    data = data - 1

    # Re-formate the data into dictionary
    G = {k:[] for k in range(n)}
    for i,p in data.iterrows():
        G[p['tail']].append(p['head'])

    G_rev = {k:[] for k in range(n)}
    for i,p in data.iterrows():
        G_rev[p['head']].append(p['tail'])

    def scc_pass(Graph, visit_order):
        # k-th element is finished in the k-th rank
        fini_time = np.array(range(0,n), dtype=int)
        source_scc = np.array(range(0,n), dtype=int)

        visited = np.array([False]*n)
        def dfs(Graph, s, source, count):
            if not visited[s]:
                visited[s] = True

                front = Graph[s]
                for i in front:
                    count = dfs(Graph, i, source, count)
                source_scc[s] = source
                fini_time[count] = s
                count += 1 # should increment the count, not decrease
            return count

        count = 0
        for s in visit_order[::-1]:
            print(s)
            count = dfs(Graph, s, s, count)

        return fini_time, source_scc


    # 1. Compute finishing time on the reverse graph.
    fini_time, _ = scc_pass(G_rev, np.array(range(0,n), dtype=int))

    # 2. Compute the strongly connected components.
    _, source_scc = scc_pass(G, fini_time)

    # 3. Print the strongly connected components.
    scc_ids = np.unique(source_scc)

    if (len(scc_ids) < 10):
        for x in scc_ids:
            scc = np.where(source_scc==x)[0]

            print('---------------------')
            print('SCC ' + str(x) + ' , length = ' + str(len(scc)) + ': ')
            # add one to revert from Python's array ordering to ordering starting from 1
            print(scc + 1)
    else:
        scc_sizes = pd.DataFrame(np.array([0] * len(scc_ids), dtype = int), 
                                 index = scc_ids, columns = ['Size'])
        for x in scc_ids:
            scc_sizes.loc[x, 'Size'] = np.sum(source_scc==x)
        scc_sizes.to_csv('output_SCC_counts.csv')

thread = threading.Thread(target=main)
thread.start()
thread.join()