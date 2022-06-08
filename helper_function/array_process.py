import pandas as pd
import numpy as np
import copy


def value_change_and_change_to_merge(a_change, a_change_to, init_value=0):
    if len(a_change) != len(a_change_to):
        print('change length %s is not = change_to length %s' % (len(a_change), len(a_change_to)))
        raise ValueError

    v0 = copy.copy(init_value)
    re_a_change = []
    re_a_change_to = []
    for index, item in enumerate(a_change):
        if pd.isna(item):
            if pd.isna(a_change_to[index]):
                print('missing value at index %s' % str(index))
                raise ValueError
            else:
                re_a_change.append(a_change_to[index] - v0)
                re_a_change_to.append(a_change_to[index])
                v0 = copy.copy(a_change_to[index])
        else:
            v0 += item
            re_a_change.append(item)
            re_a_change_to.append(v0)

    return re_a_change, re_a_change_to


def test_value_change_and_change_to_merge():
    a_c = [1, 2, pd.NaT, 4, 5, 6]
    a_c_t = [pd.NaT, pd.NaT, 10, pd.NaT, pd.NaT, pd.NaT]

    print(value_change_and_change_to_merge(a_c, a_c_t, init_value=0))


if __name__ == '__main__':
    test_value_change_and_change_to_merge()