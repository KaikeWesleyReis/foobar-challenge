# -*- coding: utf-8 -*-

import numpy as np

def solution(area_total):
    results = list()
    possibles_squares = np.array([])
    v = 1
    while (True):
        v2 = np.power(v, 2)
        if v2 > area_total:
            break
        else:
            possibles_squares = np.append(possibles_squares, [v2])
            v += 1
    results.append(int(possibles_squares[possibles_squares.size-1]))
    area_left = area_total - results[0]
    while (area_left != 0):
        for i in range(0, possibles_squares.size):
            if possibles_squares[i] == area_left:
                new_area = possibles_squares[i]
                results.append(int(new_area))
                break
            elif possibles_squares[i] > area_left:
                new_area = possibles_squares[i-1]
                results.append(int(new_area))
                break 
        area_left -= new_area
    return results 