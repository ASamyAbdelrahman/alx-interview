#!/usr/bin/python3
'''A module for working with Pascal's triangle.
'''


def pascal_triangle(n):
    '''Creates a list of lists of integers representing
    the Pascal's triangle of a given integer.
    '''
    if type(n) is not int or n <= 0:
        return []
    res = [[1]]
    for i in range(n-1):
        n_lst = [1] * (len(res[i])+1)
        for j in range(len(res[i])-1):
            n_lst[j+1] = res[i][j]+res[i][j+1]
        res.append(n_lst)
    return res
