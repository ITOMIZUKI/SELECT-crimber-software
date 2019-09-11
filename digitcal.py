import numpy as np 
import matplotlib.pyplot as plt 
import math
import sys

# the function to differentiate arr2 from arr1, able to set the minute range of differences of arr1 as range_diff
def rangediff(arr1, arr2, range_diff):

    arr = []
    arr_0 = []
    diff = []

    # require the two lists have same length
    if len(arr1) != len(arr2):
        print("each array has different number of elements. ")
        sys.exit()

    for index in range(len(arr1)):
        arr.append([arr1[index], arr2[index]])

    for num in range(int((int(arr[len(arr) - 1][0]) + 1) / range_diff)):
        arr_0.append([i for i in arr if (i[0] >= num * range_diff) and (i[0] < (num + 1) * range_diff)])

    for index in range(len(arr_0)):
        if arr_0[index] == []:
            diff.append([round((index + 0.5) * range_diff, 3), 0.0])
            continue

        diff_at = (arr_0[index][len(arr_0[index]) - 1][1] - arr_0[index][0][1]) / range_diff
        diff.append([round((index + 0.5) * range_diff, 3), diff_at])

    # return 2-dimensional list
    return diff