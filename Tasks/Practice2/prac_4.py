import multiprocessing as mp
import sys
sys.setrecursionlimit(1000000)

def divide(array, low, high):
    pivot = array[high]
    i = low - 1
    for j in range(low, high):
        if array[j] <= pivot:
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

def quick_sort(array, low, high):
    if low < high:
        pi = divide(array, low, high)
        quick_sort(array, low, pi - 1)
        quick_sort(array, pi + 1, high)
    return array

def parallel_quick_sort(array, low, high, num_threads, N=10000):
    if low < high and high - low > N and num_threads > 1:
        pi = divide(array, low, high)
        left, right = array[low:pi], array[pi + 1:high + 1]
        
        with mp.Pool(processes=2) as pool:
            left_res, right_res = pool.map(
                lambda args: parallel_quick_sort(*args),
                [(left, 0, len(left) - 1, num_threads // 2, N),
                 (right, 0, len(right) - 1, num_threads // 2, N)]
            )
        
        array[low:pi], array[pi + 1:high + 1] = left_res, right_res
    elif low < high:
        pi = divide(array, low, high)
        parallel_quick_sort(array, low, pi - 1, num_threads, N)
        parallel_quick_sort(array, pi + 1, high, num_threads, N)
    
    return array

target = [i for i in range(20000, 0, -1)]

#shell(target)
quick_sort(target, 0, len(target)-1)

