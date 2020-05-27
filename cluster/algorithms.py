import numpy as np
import matplotlib.pyplot as plt
from data import get_colors


def distance(a):
    def distance(b):
        return np.sqrt(np.sum(np.square(a-b)))
    return distance


def k_means(X):
    np.ptp(X, axis=1)
    iterations = 4
    k = 5  # for k in range(2, 5)
    centroids = np.random.rand(k, 2)  # create and distribute centroids

    
    for iteration in range(iterations):        
        dist_funcs = (distance(c) for c in centroids)  # setup distance function for each centroid
        distances = np.array([np.apply_along_axis(f, 1, X) for f in dist_funcs])  # array of point distance from each centroid
        closest_centroid = np.argmin(distances, axis=0)  # each point's closest centroid     
        centroid_groups = [np.where(closest_centroid == i)[0] for i in range(k)]  # indices of points belonging each centroid
        
        # plotting
        colors = get_colors(closest_centroid)
        plt.subplot(iterations+1, 1, iteration + 1)
        plt.scatter(X[:, 0], X[:, 1], color=colors[closest_centroid], s=3)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=10)
        
        # update centroids
        centroids = np.nan_to_num(  # convert nan-values to 0s
            np.array([np.nanmean(X[c_group], axis=0) for c_group in centroid_groups])
        )

    plt.show()


def dbscan(X):
    pass


algorithms = (
    ('K-means', k_means),
    ('DBSCAN', dbscan),
)