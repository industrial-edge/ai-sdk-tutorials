# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class SumColumnsTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        num_rows = X.shape[0]
        return (X[:, 0] + X[:, 1]+X[:, 2]).reshape(num_rows, 1)


class ClfWindowTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, window_size, step_size):
        self.window_size = window_size
        self.step_size = step_size

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        col_data_list = []
        for column in X.T:
            col_data_list.append(self._windowing(column.reshape((-1, 1))))
        return np.hstack(col_data_list)

    def _windowing(self, X):
        # https://stackoverflow.com/a/15722507
        n = X.shape[0]  # needs at least 2 dimensions
        return np.hstack(X[i:1+n+i-self.window_size:self.step_size] for i in range(0, self.window_size))


class DownsamplingTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, nbr_items, agg_func):
        self.nbr_items = nbr_items
        self.agg_func = agg_func

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        col_data_list = []
        for column in X.T:
            col_data_list.append(np.apply_along_axis(self.agg_func, 1, self._rolling_window(column, self.nbr_items)).reshape((-1, 1)))
        return np.hstack(col_data_list)

    @staticmethod
    def _rolling_window(X, window):
        shape = X.shape[:-1] + (X.shape[-1] - window + 1, window)
        strides = X.strides + (X.strides[-1],)
        return np.lib.stride_tricks.as_strided(X, shape=shape, strides=strides)


def positive_sum_of_changes(x):
    """
    Returns the sum over the positive value of consecutive changes in the series x

    Args:
        x (one dimensional numpy array): the time series to calculate the feature of

    Returns:
        float: the value of this feature
    """
    return np.sum(np.clip(np.diff(x), a_min=0, a_max=None))


def negative_sum_of_changes(x):
    """
    Returns the sum over the negative value of consecutive changes in the series x

    Args:
        x (one dimensional numpy array): the time series to calculate the feature of

    Returns:
        float: the value of this feature
    """
    return np.sum(np.clip(np.diff(x), a_min=None, a_max=0))
