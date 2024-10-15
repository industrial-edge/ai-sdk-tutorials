# SPDX-FileCopyrightText: Copyright (C) Siemens AG 2021. All Rights Reserved. Confidential.
#
# SPDX-License-Identifier: MIT

import itertools
import numpy
import matplotlib.pylab as plt
from sklearn.metrics import confusion_matrix


def show_confusion(truth, predictions, labels):
    cm = confusion_matrix(y_true=truth.argmax(axis=1), y_pred=predictions.argmax(axis=1))
    show_confusion_matrix(cm, labels)


def show_confusion_matrix(cm, labels):
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion matrix")
    plt.colorbar()
    tick_marks = numpy.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black")
