# https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html#sphx-glr-auto-examples-cluster-plot-linkage-comparison-py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from data import *
from algorithms import k_means, dbscan


default_base = {'n_neighbors': 10,
                'n_clusters': 3}

for i_dataset, (dataset, algo_params) in enumerate(datasets):
    # update parameters with dataset-specific values
    params = default_base.copy()
    params.update(algo_params)

    X, y = dataset
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    # k_means(X)
    dbscan(X)

# plt.show()


