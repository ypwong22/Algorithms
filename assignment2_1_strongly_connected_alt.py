# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 18:24:15 2018

@author: User

Another version of the strongly connected components using stack instead of
recursion.

Unfinished.
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


G = {k:[] for k in range(n)}
for i,p in data.iterrows():
    G[p['tail']].append(p['head'])

G_rev = {k:[] for k in range(n)}
for i,p in data.iterrows():
    G_rev[p['head']].append(p['tail'])


###############################################################################
# 1. Compute topological ordering on the reverse graph.
###############################################################################
# value at the k-th position is the visit time of node k
# I believe that finish time is in the reverse order of visit time

# =============================================================================
# DFS(source):
#   s <- new stack
#   visited <- {} // empty set
#   s.push(source)
#   while (s is not empty):
#     current <- s.pop()
#     if (current is in visited):
#         continue
#     visited.add(current)
#     // do something with current
#     for each node v such that (current,v) is an edge:
#         s.push(v)
# =============================================================================

visi_time = np.array([0]*n, dtype=int)
visited = np.array([False]*n)
count = 0
for s in range(0,n):
    if not visited[s]:
        visited[s] = True
        visi_time[s] = count

        stk_s = [s]
        while stk_s:
            current = stk_s.pop()
            if not visited[current]:
                visited[current] = True
                visi_time[current] = count
                for i in G_rev[current]:
                    stk_s.append(i)
                count += 1

# value at the k-th position is the 'finish time' of node k
fini_time = n-1 - visi_time
# ---- revert fini_time such that fini_time[k] = s means that the 'finish
#      time' of s is k
fini_time2 = {fini_time[s]: s for s in range(len(fini_time))}


###############################################################################
# 2. Compute the strongly connected components.
###############################################################################

XXXXXXXXXXXX

source_scc = np.array([0]*n, dtype=int)
visited = np.array([False]*n)
count = 0
for s in range(0,n):
    if not visited[s]:
        visited[s] = True
        visi_time[s] = count

        stk_s = [s]
        while stk_s:
            current = stk_s.pop()
            if not visited[current]:
                visited[current] = True
                visi_time[current] = count
                for i in G[current]:
                    stk_s.append(i)
                count += 1
fini_time = n-1 - visi_time

