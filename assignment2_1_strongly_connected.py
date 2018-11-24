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
    file = 'SCC.txt'
    n = 875714
    # file = 'input_mostlyCycles_30_800.txt'
    # n = 800
    # file = 'input_mostlyCycles_2_8.txt'
    # n = 8
    # file = 'input_mostlyCycles_22_200.txt'
    # n = 200

    data = pd.read_csv(file, sep=' ', header=None, usecols=[0,1], 
                       names = ['tail', 'head'])

    # minus one to become compatible with Python's array ordering
    data = data - 1

    # Re-formate the data into dictionary
    G = {}
    for i in range(n):
        G[i] = []
    for i,p in data.iterrows():
        G[p['tail']].append(p['head'])

    G_rev = {}
    for i in range(n):
        G_rev[i] = []
    for i,p in data.iterrows():
        G_rev[p['head']].append(p['tail'])


    def scc_pass(Graph, visit_order):
        topo_order = np.array(range(0,n), dtype=int)
        source_scc = np.array(range(0,n), dtype=int)

        visited = np.array([False]*n)
        def dfs(Graph, s, source, count):
            if not visited[s]:
                visited[s] = True

                front = Graph[s]
                for i in front:
                    count = dfs(Graph, i, source, count)
                source_scc[s] = source
                topo_order[count] = s
                count -= 1
            return count

        count = n - 1
        for s in visit_order[::-1]:
            print(s)
            count = dfs(Graph, visit_order[s], visit_order[s], count)

        return topo_order, source_scc


    # 1. Compute topological ordering on the reverse graph.
    topo_order, _ = scc_pass(G, np.array(range(0,n), dtype=int))

    # 2. Compute the strongly connected components.
    _, source_scc = scc_pass(G_rev, topo_order)

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