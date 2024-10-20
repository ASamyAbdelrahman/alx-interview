#!/usr/bin/python3
'''The minimum operations coding challenge.
'''

import math


def minOperations(n):
    '''Computes the fewest number of operations needed to result
    in exactly n H characters.
    '''
    if not isinstance(n, int):
        return 0
    if n <= 0:
        return 0
    res = 0
    while (n % 2 == 0):
        res = res + 2
        n = n / 2
    for i in range(3, int(math.sqrt(n))+1, 2):
        while (n % i == 0):
            res = res + i
            n = n / i
    if (n > 2):
        res = res + n
    return int(res)
