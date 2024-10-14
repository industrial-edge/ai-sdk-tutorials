# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

import numpy as np
import pandas
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute._base import _BaseImputer

class FillMissingValues(_BaseImputer):
    def __init__(self, value=None):
        if isinstance(value, (int, float)) or value == 'ffill' or value == 'bfill':
            self.value = value
        else:
            raise ValueError('self.value must be a number or "bfill" or "ffill"')

    def fit(self, X):
        return self

    def transform(self, X):
        if X.ndim == 2:
            return self._transform2D(X)
        else:
            _filled = []
            for x in X:
                _filled.append(self._transform2D(x))
            return np.array(_filled)
        
    def _transform2D(self, X):
        df = pandas.DataFrame(X)
        if ('bfill' == self.value) or ('ffill' == self.value):
            df = df.bfill(axis=0) if self.value == 'bfill' else df.ffill(axis=0)
        elif isinstance(self.value, (int, float)):
            df = df.fillna(value=self.value, method=None)
        else:
            raise ValueError('self.value must be a number or "bfill" or "ffill"')

        return df.to_numpy()
        
class SumColumnsTransformer(BaseEstimator, TransformerMixin):        
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        if X.ndim == 2:
            return self._transform2D(X)
        else:
            _filled = []
            for x in X:
                _filled.append(self._transform2D(x))
            frames, rows, cols = np.array(_filled).shape
            return np.array(_filled).reshape((cols,frames,rows))
            # return np.array(_filled).reshape((1,140,300))

    def _transform2D(self, X):
        numRows = X.shape[0]
        return (X[:,0]+X[:,1]+X[:,2]).reshape(numRows,1)


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
