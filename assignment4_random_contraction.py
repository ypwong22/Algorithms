"""
ypwong @ 2018-09-04
"""
import numpy as np
import random


class RdCtrn():
    def __init__(self, filename, seed, n_iter):
        # (constants)
        self.filename = filename
        self.seed = seed
        self.n_iter = n_iter

        # (modified during different calls to __read_adjacency_mat
        #  and __randomized_contraction)
        self._adj_mat = {}
        self._adj_mat_next = {}
        self._partition = {}
        self._n_minimum_cut = 9999999

        # (modified during calls to multiple_runs)
        self.adj_mat_final = {}
        self.partition_final = {}
        self.n_minimum_cut_final = 9999999

    def __read_adjacency_mat(self):
        f = open(self.filename)
        for line in f:
            v_all = [int(x) for x in line.split()]
            self._adj_mat[v_all[0]] = v_all[1:]
        f.close()
        self._adj_mat_next = self._adj_mat.copy()
        self._partition = dict([(x, set([x])) for x in list(self._adj_mat.keys())])

    def __randomized_contraction(self):
        while (len(self._adj_mat_next.keys()) > 2):
            ##print(self._adj_mat_next.keys())
            ##print(len(self._adj_mat_next))

            v1 = random.choice(list(self._adj_mat_next.keys()))
            v2 = random.choice(self._adj_mat_next[v1])

            # (merge v2 unto v1 in the record of groupped vertices)
            self._partition[v1] = self._partition[v1].union(self._partition[v2])
            self._partition.pop(v2)

            for k in self._adj_mat_next.keys():
                if (k != v1) and (k != v2):
                    for m in range(len(self._adj_mat_next[k])):
                        if (self._adj_mat_next[k][m] == v2):
                            # (merge the edge unto v1; do not remove duplicates)
                            self._adj_mat_next[k][m] = v1

            # (merge v1 and v2; do not remove duplicates)
            self._adj_mat_next[v1] = self._adj_mat_next[v1] + \
                                     self._adj_mat_next[v2]

            # (delete self loop)
            temp_copy = self._adj_mat_next[v1].copy()
            for m in temp_copy:
                if (m == v2) or (m == v1):
                    self._adj_mat_next[v1].remove(m)

            self._adj_mat_next.pop(v2)
            
        v1 = list(self._adj_mat_next.keys())[0]
        self._n_minimum_cut = len(self._adj_mat_next[v1])

        # De-bug checks
        # (1)
        v2 = list(self._adj_mat_next.keys())[1]
        n_minimum_cut2 = len(self._adj_mat_next[v2])
        if (self._n_minimum_cut != n_minimum_cut2):
            raise Exception('The final partition has unequal number of edges from one group to the other (' + str(n_minimum_cut2) + ' and ' + str(self._n_minimum_cut) + ').')
        # (2)
        temp = list(self._partition.values())
        if (temp[0].union(temp[1]) != self._adj_mat.keys()):
            raise Exception('The vertices in _partition differs from the original set of vertices in _adj_mat! Check these variables.')


    def multiple_runs(self):
        random.seed(self.seed)
        for n in range(n_iter):
            print('Iteration: ' + str(n))
            self.__read_adjacency_mat()
            self.__randomized_contraction()
            if (self._n_minimum_cut < self.n_minimum_cut_final):
                self.n_minimum_cut_final = self._n_minimum_cut
                self.partition_final = self._partition
                self.adj_mat_final = self._adj_mat_next

        # De-bug checks
        # (3) sanity check that _n_minimum_cut <= all the degrees
        v_degrees = []
        for k in self._adj_mat.keys():
            v_degrees.append(len(self._adj_mat[k]))
        min_degrees = min(v_degrees)
        if (self.n_minimum_cut_final > min_degrees):
            raise Exception('Did not find the minimum cut because n_minimum_cut_final = ' + str(self.n_minimum_cut_final) + ' while the minimum number of degrees = ' + str(min_degrees))

        return self.n_minimum_cut_final, self.partition_final, self.adj_mat_final


# Main
filename = 'kargerMinCut.txt'
n_iter = int(200 * 200 * np.ceil(np.log(200)))
##filename = 'kargerMinCut_test3.txt'
##n_iter = int(6 * 6 * np.ceil(np.log(6)))
r = RdCtrn(filename, 31267, n_iter)
n_minimum_cut, partition_final, adj_mat_final = r.multiple_runs()
print('Found minimum cut = ' + str(n_minimum_cut))
print('The corresponding partition: ', partition_final)