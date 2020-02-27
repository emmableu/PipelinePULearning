import numpy as np
import urllib.request
import os
import tarfile
import pickle
from sklearn.datasets import fetch_mldata
import sys
sys.path.append('my_module')
from save_load_pickle import *


def get_dataset():
    data = load_obj('unlabeled_games_one_hot_count', 'Data', "UnLabeled-SB3JsonFiles/pre_process-games1000")
    x = np.asarray(data.code.to_list())
    y = np.random.randint(2, size = 1000)
    x = np.reshape(x, (x.shape[0], 1, 13, 13))
    # x = np.reshape(x, (x.shape[0], 1, 28, 28)) / 255.
    # x_tr = np.asarray(x[:800], dtype=np.float32)
    # y_tr = np.asarray(y[:800], dtype=np.int32)
    # x_te = np.asarray(x[800:], dtype=np.float32)
    # y_te = np.asarray(y[800:], dtype=np.int32)

    x_tr = np.asarray(x[:10], dtype=np.float32)
    y_tr = np.asarray(y[:10], dtype=np.int32)
    x_te = np.asarray(x[10:20], dtype=np.float32)
    y_te = np.asarray(y[10:20], dtype=np.int32)
    return (x_tr, y_tr), (x_te, y_te)


def make_dataset(dataset, n_labeled, n_unlabeled):
    def make_pu_dataset_from_binary_dataset(x, y, labeled=n_labeled, unlabeled=n_unlabeled):
        labels = np.unique(y)
        positive, negative = labels[1], labels[0]
        x, y = np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.int32)
        assert(len(x) == len(y))
        perm = np.random.permutation(len(y))
        x, y = x[perm], y[perm]
        n_p = (y == positive).sum()
        n_lp = labeled
        n_n = (y == negative).sum()
        n_u = unlabeled
        if labeled + unlabeled == len(x):
            n_up = n_p - n_lp
        elif unlabeled == len(x):
            n_up = n_p
        else:
            raise ValueError("Only support |P|+|U|=|X| or |U|=|X|.")
        _prior = float(n_up) / float(n_u)
        xlp = x[y == positive][:n_lp]
        xup = np.concatenate((x[y == positive][n_lp:], xlp), axis=0)[:n_up]
        xun = x[y == negative]
        x = np.asarray(np.concatenate((xlp, xup, xun), axis=0), dtype=np.float32)
        print(x.shape)
        y = np.asarray(np.concatenate((np.ones(n_lp), -np.ones(n_u))), dtype=np.int32)
        perm = np.random.permutation(len(y))
        x, y = x[perm], y[perm]
        return x, y, _prior

    def make_pn_dataset_from_binary_dataset(x, y):
        labels = np.unique(y)
        positive, negative = labels[1], labels[0]
        X, Y = np.asarray(x, dtype=np.float32), np.asarray(y, dtype=np.int32)
        n_p = (Y == positive).sum()
        n_n = (Y == negative).sum()
        Xp = X[Y == positive][:n_p]
        Xn = X[Y == negative][:n_n]
        X = np.asarray(np.concatenate((Xp, Xn)), dtype=np.float32)
        Y = np.asarray(np.concatenate((np.ones(n_p), -np.ones(n_n))), dtype=np.int32)
        perm = np.random.permutation(len(Y))
        X, Y = X[perm], Y[perm]
        return X, Y

    (x_train, y_train), (x_test, y_test) = dataset
    x_train, y_train, prior = make_pu_dataset_from_binary_dataset(x_train, y_train)
    x_test, y_test = make_pn_dataset_from_binary_dataset(x_test, y_test)
    print("training:{}".format(x_train.shape))
    print("test:{}".format(x_test.shape))
    return list(zip(x_train, y_train)), list(zip(x_test, y_test)), prior


def load_dataset(n_labeled, n_unlabeled):
    (x_train, y_train), (x_test, y_test) = get_dataset()
    xy_train, xy_test, prior = make_dataset(((x_train, y_train), (x_test, y_test)), n_labeled, n_unlabeled)
    return xy_train, xy_test, prior
