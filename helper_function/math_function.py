import numpy as np
import itertools


def grid_pos(n, width):
    re = n // width, n % width

    return re


def strip_cover(stp_set_1, stp_set_2, freq=1):
    min_st = min([item[0] for item in stp_set_1] + [item[0] for item in stp_set_2])
    max_ed = max([item[1] for item in stp_set_1] + [item[1] for item in stp_set_2])
    rg = range(int(min_st), int(max_ed // freq + ((max_ed % freq) > 0)), freq)

    print(rg)


def crop(p11, p12, p21, p22):
    return max([min([p11, p12]), min([p21, p22])]), min([max([p11, p12]), max([p21, p22])])


def dir_crop(st1, ed1, st2, ed2):
    if (st1 - ed1) * (st2 - ed2) < 0:
        return None, None
    else:
        if ed1 >= st1:
            return max([st1, st2]), min([ed1, ed2])
        else:
            return min([st1, st2]), max([ed1, ed2])


def rest_rates_to_acc_rates(rest_rates: list):
    rest_rates = np.array(rest_rates)
    acc_rates = np.cumprod(1 - rest_rates)
    acc_rates = np.concatenate(([1], acc_rates[:-1])) * rest_rates

    return list(acc_rates)


def test_grid_pos():
    print(grid_pos(10, 3))


def test_strip_cover():
    stp1 = [[0.5, 1, 2], [2, 3, 4]]
    stp2 = [[0.5, 1, 2], [2, 3.5, 4]]
    strip_cover(stp1, stp2, freq=0.5)


def test_crop():
    print(crop(6, 1, 3, 2))


def test_rest_rates_to_acc_rates():
    rs = [0.5, 0.5, 1]
    print(rest_rates_to_acc_rates(rs))


def test_cartesian():
    l1 = [1, 2, 3, 4]
    l2 = ['a', 'b', 'c']
    l3 = [5, 6, 7]

    for item in itertools.product(l1, l2, l3):
        print(item)


if __name__ == '__main__':
    test_cartesian()
