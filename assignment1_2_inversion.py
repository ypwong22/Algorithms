# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 20:14:12 2018

@author: wangy

Calculate the number of inversions (increasing order) in a large array.
"""
import numpy as np


def Inversion(arr):
    if (len(arr) == 1):
        return 0, arr

    else:
        n = len(arr) // 2

        arr1 = arr[:n]
        arr2 = arr[n:]

        ##print(len(arr1))
        ##print(len(arr2))
        
        inversion_arr1, sorted_arr1 = Inversion(arr1)
        inversion_arr2, sorted_arr2 = Inversion(arr2)


        # the number of inversions on each side
        n_inversion = inversion_arr1 + inversion_arr2
        
        # add the cross-inversions
        i = 0
        j = 0
        sorted_arr = arr.copy()
        for r in range(len(arr)):
            if (i==len(sorted_arr1)):
                sorted_arr[r:] = sorted_arr2[j:]
                break

            if (j==len(sorted_arr2)):
                sorted_arr[r:] = sorted_arr1[i:]
                break

            if (sorted_arr1[i] < sorted_arr2[j]):
                sorted_arr[r] = sorted_arr1[i]
                i += 1
            else:
                sorted_arr[r] = sorted_arr2[j]

                if (sorted_arr1[i] == sorted_arr2[j]):
                    n_inversion += (n-i-1)
                else:
                    n_inversion += (n-i)
                j += 1

        return n_inversion, sorted_arr


arr = np.loadtxt('IntegerArray.txt')
n_inversion, sorted_arr = Inversion(arr)


print(n_inversion)

if (len(sorted_arr) < 10):
    print(sorted_arr)