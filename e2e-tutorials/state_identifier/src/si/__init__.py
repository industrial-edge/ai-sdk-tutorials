# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

import numpy as np

from itertools import chain, combinations


def get_combinations(item_list, min_items=1):
    return list(chain.from_iterable([combinations(item_list, i) for i in range(min_items, len(item_list)+1)]))


def windowing(X, window_size, step_size):
    # https://stackoverflow.com/a/15722507
    n = X.shape[0]  # needs at least 2 dimensions
    return np.hstack(X[i:1+n+i-window_size:step_size] for i in range(0, window_size))
