# Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.

"""
Building blocks for scikit-learn pipelines.

To train the classifier in such a pipeline, the input data must be fed through the preprocessing steps during the training process.
Therefore, this processing pipeline has to be defined before the training, as part of data preparation. This is where the building
blocks in the AI SDK come into play.

These building blocks are based on the widely used machine learning Python package scikit-learn. Scikit-learn provides a framework to
define pipelines, which lets you combine data transformers with classifiers or other kinds of estimators. The building blocks are
located in module `simaticai.pipeline`. The essential ones are:

- `WindowTransformer`, which transforms a series of input rows into a series of windows of rows and

- `FeatureTransformer`, which transforms a window of rows into a feature value according to user defined functions.

In addition to these transformers, there is a transformer named `FillMissingValues` which performs input data correction for simple cases. For more advanced
cases, you should use a more sophisticated imputer to fix your input.

For more details and concrete examples, please refer to the training notebooks in the State Identifier project template.
We also recommend studying the documentation of scikit-learn if you would like to understand in-depth how scikit-learn
works or want to implement your own transformers.
"""

import numpy
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute._base import _BaseImputer
from sklearn.pipeline import Pipeline
import pandas as pd


class FeatureTransformer(BaseEstimator, TransformerMixin):
    """
    The `FeatureTransformer` calculates aggregated features from a window of data.
    The functions and weights in `function_list` will be used to extract features with the given multiplicity.

    The example code below illustrates the behavior.
    ```python
    function_list = [
        (2, [numpy.mean]),
        (1, [numpy.min, numpy.max]),
    ]
    feature_transformer = FeatureTransformer(function_list)

    windowed_data = [
            # windowed data with 1 variable and 4 data points
            [  # variable 1
               [10, 20, 10, 20],  # window 1 with 4 data points
               [30, 40, 30, 40],  # window 2 with 4 data points
               [50, 60, 50, 60]   # window 3 with 4 data points
            ]
    ]

    result = feature_transformer.transform(windowed_data)

    array([[15., 15., 10., 20.],   # mean, mean, min, max values from the first window
           [35., 35., 30., 40.],   # mean, mean, min, max values from the second window
           [55., 55., 50., 60.]])  # mean, mean, min, max values from the third window
    ```

    Args:
        function_list (list of tuples (_weight_, _functions_)): _weight_ is how many times the extracted features will be repeated and _functions_ is a list of functions to calculate the features from a window of data
    """
    _func_list = []

    def __init__(self, function_list=None):
        """
        Args:
            function_list (list of tuples (_weight_, _functions_)): where _weight_ is how many times the extracted features will be repeated and _functions_ is a list of functions to calculate the features from a window of data
        """
        self._set_funcs(function_list)

    @property
    def function_list(self):
        return self._func_list

    @function_list.setter
    def function_list(self, function_list):
        self._set_funcs(function_list)

    def _set_funcs(self, func_list):
        _func_list = []
        if func_list is not None:
            for weight, block in func_list:
                _func_list.extend(block * weight)
        self._func_list = _func_list

    def fit(self, X, y=None):
        """
        A no-operation, as feature extractors are stateless functions and independent of input data.
        """
        return self

    def transform(self, X):
        """
        Transforms a 3D array of windowed data indexed by variable x window x timestamp to a 2D array indexed by window x feature*variable.
        If the input array contains multiple variables, that is, the first dimension is greater than 1, the feature values in a window
        will be concatenated to a single flat list, starting with the features extracted from the first variable, followed by the ones for
        the second variable, and so on.

        Params:
            X (numpy.array): Windowed data in 3D array, indexed by variable x window x timestamp

        Returns:
            numpy.array: 2D array of extracted feature values window by window, indexed by window x feature*variable
        """
        agg_data_list = []
        for feature_grid in X:
            agg_data_list.append(numpy.hstack([numpy.apply_along_axis(func, 1, feature_grid).reshape((-1, 1)) for func in self._func_list]))
        return numpy.hstack(agg_data_list)


class WindowTransformer(BaseEstimator, TransformerMixin):
    """
    A class for creating windows from incoming data, given a window size and an offset between windows.
    If no offset is defined, the window size is used, so windows will be adjacent but not overlap.

    The example code below illustrates the behavior.
    ```python
    X = numpy.array([
        [11, 12, 13], # Variable values for first timestamp
        [21, 22, 23], # Variable values for second timestamp
        [31, 32, 33], # ...
        [41, 42, 43],
        [51, 52, 53],
        [61, 62, 63],
        [71, 72, 73],
        [81, 82, 83],
        [91, 92, 93]])

    win3_stepN = WindowTransformer(3).transform(X)
    win4_stepN = WindowTransformer(4, None).transform(X)
    win3_step3 = WindowTransformer(3, 3).transform(X)
    win4_step3 = WindowTransformer(4, 3).transform(X)

    win3_step3 = win3_stepN

    win3_stepN = [
        [[11, 21, 31], # Values of first variable for timestamps in the first window
         [41, 51, 61], # Values of first variable for timestamps in the second window
         [71, 81, 91]],
        [[12, 22, 32], # Values of second variable for timestamps in the first window
         [42, 52, 62], # Values of second variable for timestamps in the second window
         [72, 82, 92]],
        [[13, 23, 33],
         [43, 53, 63],
         [73, 83, 93]]])

    win4_stepN = [
        [[11, 21, 31, 41],
         [51, 61, 71, 81]],
        [[12, 22, 32, 42],
         [52, 62, 72, 82]],
        [[13, 23, 33, 43],
         [53, 63, 73, 83]]])

    win4_step3 = [
        [[11, 21, 31, 41],
         [41, 51, 61, 71]],
        [[12, 22, 32, 42],
         [42, 52, 62, 72]],
        [[13, 23, 33, 43],
         [43, 53, 63, 73]]])
    ```
    Args:
        window_size: Number of values in a window.
        window_step: Number of values by which the subsequent window is offset. Defaults to `window_size`.
    """

    def __init__(self, window_size, window_step=None):
        """
        Args:
            window_size: Number of values in a window.
            window_step: Number of values by which the subsequent window is offset. Defaults to `window_size`.
        """
        if window_size < 1:
            raise ValueError("window_size must be > 0")
        if window_step is None:
            window_step = window_size
        if window_step < 1:
            raise ValueError("window_step must be > 0")
        self.window_size = window_size
        self.window_step = window_step

    def fit(self, X, y=None):
        """
        A no-operation, as feature extractors are stateless functions and independent of input data.
        """
        return self

    def transform(self, X):
        """
        Transforms a 2D array containing data rows indexed by timestamp x variable to a 3D array containing windows, indexed by variable x window x timestamp.
        """
        col_data_list = []
        for column in X.T:
            col_data_list.append(self._windowing(column.reshape((-1, 1))))
        return numpy.stack(col_data_list)

    def _windowing(self, X):
        # https://stackoverflow.com/a/15722507
        n = X.shape[0]  # needs at least 2 dimensions
        return numpy.hstack([X[i:1 + n + i - self.window_size:self.window_step] for i in range(0, self.window_size)])


class FillMissingValues(_BaseImputer):
    """
    Fills missing values column-wise in a dataset.

    The example code below illustrates the behavior.
    ```python
    X = [[1, 10,   None, 1000],
         [2, None, None, None],
         [3, None, 300,  3000]]

    Xv = FillMissingValues(3.14159).transform(X)
    Xf = FillMissingValues('ffill').transform(X)
    Xb = FillMissingValues('bfill').transform(X)

    Xv = [[1, 10,      3.14159, 1000   ],
          [2, 3.14159, 3.14159, 3.14159],
          [3, 3.14159, 300,     3000   ]]

    Xf = [[1, 10, np.NaN, 1000],
          [2, 10, np.NaN, 1000],
          [3, 10, 300,    3000]]

    Xb = [[1, 10,        300, 1000],
          [2, numpy.NaN, 300, 3000],
          [3, numpy.NaN, 300, 3000]]
    ```
    Args:
        value (string or number): If this argument is a number,
                then the missing values will be filled with the given constant.
                If it is a string, it must be either `bfill` or `ffill`.
                With `bfill` the next valid value will be used for filling.
                With `ffill` the previous valid value will be used for filling.
    """

    def __init__(self, value=None):
        """
        Args:
            value (string or number): If this argument is a number,
                then the missing values will be filled with the given constant.
                If it is a string, it must be either `bfill` or `ffill`.
                With `bfill` the next valid value will be used for filling.
                With `ffill` the previous valid value will be used for filling.
        """
        if isinstance(value, (int, float)) or value == 'ffill' or value == 'bfill':
            self.value = value
        else:
            raise ValueError('self.value must be a number or "bfill" or "ffill"')

    def fit(self, X):
        """
        A no-operation, as feature extractors are stateless functions and independent of input data.
        """
        return self

    def transform(self, X):
        """
        Transforms the given array by filling missing values.
        """
        df = pd.DataFrame(X)
        if ('bfill' == self.value) or ('ffill' == self.value):
            df = df.fillna(value=None, method=self.value)
        elif isinstance(self.value, (int, float)):
            df = df.fillna(value=self.value, method=None)
        else:
            raise ValueError('self.value must be a number or "bfill" or "ffill"')

        return df.to_numpy()


def back_propagate_labels(data_frame: pd.DataFrame, pipeline: Pipeline, x_classes, result: str = 'class'):
    """
    Augments a data frame with labels defined per window.
    Maps a label for each window in `x_classes` to the corresponding data points in `data_frame` according to the window
    definition in `pipeline`. The results are stored in a column named according to the `result` parameter.

    Params:
        data_frame (pandas.DataFrame): Data frame to be labelled
        pipeline (sklearn.pipeline.Pipeline): Pipeline containing a step named `windowing` with parameters `window_step` and `window_size`
        x_classes (list): Labels per window
        result (str): Target column name for labels
    Returns:
        pandas.DataFrame: input parameter `data_frame`
    """

    window_step = pipeline["windowing"].window_step
    window_size = pipeline["windowing"].window_size

    result_iterator = enumerate(x_classes)
    data_frame[result] = -1  # adding a new column with default value -1

    for i, value in result_iterator:
        start = (i+1) * window_step
        end = (i+1) * window_step + window_size
        data_frame.loc[start:end, 'class'] = value

    return data_frame
