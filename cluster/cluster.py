# https://scikit-learn.org/stable/auto_examples/cluster/plot_linkage_comparison.html#sphx-glr-auto-examples-cluster-plot-linkage-comparison-py
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

from data import *
from algorithms import k_means

# Set up cluster parameters
# plt.figure(figsize=(9 * 1.3 + 2, 14.5))
# plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05, hspace=.01)

default_base = {'n_neighbors': 10,
                'n_clusters': 3}

for i_dataset, (dataset, algo_params) in enumerate(datasets):
    # update parameters with dataset-specific values
    params = default_base.copy()
    params.update(algo_params)

    X, y = dataset
    # normalize dataset for easier parameter selection
    X = StandardScaler().fit_transform(X)

    # plt.subplot(len(datasets), 1, i_dataset + 1)
    # plt.scatter(X[:, 0], X[:, 1], s=10)

    k_means(X)


# plt.show()


