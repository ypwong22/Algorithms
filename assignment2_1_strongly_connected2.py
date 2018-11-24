# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 18:24:15 2018

@author: User

Another version of the strongly connected components using stack instead of
recursion.
"""
import numpy as np
import pandas as pd


# file = 'SCC_test.txt'
# n = 15
file = 'SCC.txt'
n = 875714


data = pd.read_csv(file, sep=' ', header=None, usecols=[0,1], 
                   names = ['tail', 'head'])

# minus one to become compatible with Python's array ordering
data = data - 1


topo_order = np.array(range(0,n), dtype=int)
source_scc = np.array(range(0,n), dtype=int)

def scc_pass(tail, head, topo_order, source_scc):

    def dfs(tail, head, s, source, count):
        if not visited[s]:
            visited[s] = True

            front = head[np.where(tail==s)[0]]
            for i in front:
                count = dfs(tail, head, i, source, count)

            source_scc[s] = source
            topo_order[count] = s
            count -= 1
        return count


    count = n - 1
    visited = np.array([False]*n)
    for s in topo_order[::-1]:
        if not visited[s]:
            visited[s] = True

            front = head[np.where(tail==s)[0]]
            to_finish = front
            
            while to_finish:
                
            XXXXXXXXXXXXXXXx


    return topo_order, source_scc


# 1. Compute topological ordering on the reverse graph.
topo_order, _ = scc_pass(data['tail'], data['head'], topo_order, source_scc)


# 2. Compute the strongly connected components.
_, source_scc = scc_pass(data['tail'], data['head'], topo_order, source_scc)

# 3. Print the strongly connected components.
for x in np.unique(source_scc):
    scc = np.where(source_scc==x)[0]

    print('---------------------')
    print('SCC ' + str(x) + ' , length = ' + str(len(scc)) + ': ')
    # add one to revert from Python's array ordering to ordering starting from 1
    print(scc + 1)
