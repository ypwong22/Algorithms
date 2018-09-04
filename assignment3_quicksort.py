# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 21:39:11 2018

@author: wangy

Implement QuickSort and count the number of comparisons when the pivot element
    was chosen in one of three ways:
    (1) 1st element
    (2) last element
    (3) median of the 1st, middle, and last element
"""

import numpy as np

def QuickSort(arr, pivot, n_compare):
    if (len(arr) == 1):
        return arr, n_compare

    else:
        # arr: input array
        # pivot: which element to pivot at (0, -1, 'median')
        if isinstance(pivot, str):
            # ---- find the median between 1st, last, and middle element
            a = arr[0]
            b = arr[-1]
            c = arr[(len(arr) - 1) // 2]

            if (a > b):
                if (b > c):
                    pivot2 = -1
                else:
                    if (a > c):
                        pivot2 = (len(arr) - 1) // 2
                    else:
                        pivot2 = 0
            else:
                if (b > c):
                    if (a > c):
                        pivot2 = 0
                    else:
                        pivot2 = (len(arr) - 1) // 2
                else:
                    pivot2 = -1
                             
            ##print(a, b, c, '      ', pivot2)
        else:
            pivot2 = pivot

        key = arr[pivot2] # note: seems to be automatic copying
    
        # move key to the beginning of array
        temp = arr[0]
        arr[0] = key
        arr[pivot2] = temp

        i = 1 # first element of arr larger than key
        j = 0 # last element of arr larger than key (before the unscanned section)
    
        for n in range(1, len(arr)):
            if (arr[n] > key):
                j += 1
            else:
                temp = arr[n]
                arr[n] = arr[i]
                arr[i] = temp
                i += 1
                j += 1
        temp = arr[i-1]
        arr[i-1] = key
        arr[0] = temp

        n_compare += (len(arr) - 1)

        if (i > 1):
            arr1, n_compare = QuickSort(arr[:(i-1)], pivot, n_compare)
            arr[:(i-1)] = arr1

        if (i < len(arr)):
            arr2, n_compare = QuickSort(arr[i:], pivot, n_compare)
            arr[i:] = arr2

        return arr, n_compare



##arr = np.loadtxt('QuickSort_test.txt')
arr = np.loadtxt('QuickSort.txt')
sorted_arr, n_inversion = QuickSort(arr, 0, 0)
print(sorted_arr, n_inversion)

##arr = np.loadtxt('QuickSort_test.txt')
arr = np.loadtxt('QuickSort.txt')
sorted_arr, n_inversion = QuickSort(arr, -1, 0)
print(sorted_arr, n_inversion)

##arr = np.loadtxt('QuickSort_test.txt')
##arr = [2, 20, 1, 15, 3, 11, 13, 6, 16, 10, 19, 5, 4, 9, 8, 14, 18, 17, 7, 12]
#total count: 55
arr = np.loadtxt('QuickSort.txt')
sorted_arr, n_inversion = QuickSort(arr, 'median', 0)
print(sorted_arr, n_inversion)