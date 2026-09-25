import multiprocessing as mp
import time
import sys

sys.setrecursionlimit(999999999)

array = [n for n in range(20000, 0, -1)]


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Функция {func.__name__} выполнилась за {end - start:.6f} сек\n")
        return result
    return wrapper


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


@timer
def parallel_quick_sort(array, low, high, num_threads, N=10000):
    if low >= high:
        return array
    if high - low > N and num_threads > 1:
        pi = divide(array, low, high)

        left = array[low:pi]
        right = array[pi + 1:high + 1]

        with mp.Pool(processes=2) as pool:
            left_res, right_res = pool.starmap(
                quick_sort,
                [
                    (left, 0, len(left) - 1),
                    (right, 0, len(right) - 1)
                ]
            )

        array[low:pi] = left_res
        array[pi + 1:high + 1] = right_res

    else:
        quick_sort(array, low, high)

    return array


if __name__ == "__main__":
    mp.freeze_support()

    result = parallel_quick_sort(
        array,
        0,
        len(array) - 1,
        8,
        10000
    )

    print(result[:10])
