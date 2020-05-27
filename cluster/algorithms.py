import time
import numpy as np
import matplotlib.pyplot as plt
from data import get_colors


def distance(a):
    def distance(b):
        return np.sqrt(np.sum(np.square(a-b)))
    return distance


def silhouette_score(X, y, groups):
    num_groups = len(groups)
    scores = []
    for i, point in enumerate(X):
        dist_f = distance(point)
        cluster = y[i]
        cluster_points = X[groups[cluster]]

        a = np.mean(np.apply_along_axis(dist_f, 1, cluster_points))
        
        other_cluster_points = [X[groups[j]] for j in range(num_groups) if j != cluster]
        other_cluster_distances = [np.apply_along_axis(dist_f, 1, other_cluster) for other_cluster in other_cluster_points]
        b = min(np.mean(dist) for dist in other_cluster_distances)
        
        s = (b - a) / max(a, b)
        scores.append(s)
    #plt.figure(1000)
    #plt.plot(sorted(scores))
    #plt.show()
    return scores


def SSE(X, groups, centroids):
    dist_fs = [distance(c) for c in centroids]
    clusters = [X[cluster] for cluster in groups]
    score = sum(
        np.sum(np.apply_along_axis(f, 1, cluster)) 
        for f, cluster in zip(dist_fs, clusters)
    )
    return score


def SSB(groups, centroids):
    return sum( 
        groups[i].size * np.sum(np.square(m - mi)) 
        for i, m in enumerate(centroids) 
        for mi in centroids
    )


@np.vectorize
def color_scale(value):
    hex_val = hex(int(abs(value * 255)))
    if len(hex_val) == 3:
        hex_val += "0"
    if value > 0:  # b/w-scale
        color =  "#" + hex_val[2:]*3
    else:  # red scale
        color= "#" + hex_val[2:] + "0000"
    return color


def k_means(X):
    iterations = 12
    skip = 3
    k_min, k_max = 2, 6
    num_ks = num_plot_cols= k_max - k_min
    extra_plots = 1
    num_plot_rows = extra_plots + iterations//skip
    plot_num = 0

    for k in range(k_min, k_max):
        centroids = np.random.uniform(low=np.min(X), high=np.max(X), size=(k, 2))    # create and distribute centroids
        for iteration in range(iterations):     
            dist_funcs = (distance(c) for c in centroids)  # setup distance function for each centroid
            distances = np.array([np.apply_along_axis(f, 1, X) for f in dist_funcs])  # array of point distance from each centroid
            closest_centroid = np.argmin(distances, axis=0)  # each point's closest centroid 
            centroid_groups = [np.where(closest_centroid == i)[0] for i in range(k)]  # indices of points belonging each centroid
             
            # plotting
            if iteration % skip == 0:
                plot_num += 1
                colors = get_colors(closest_centroid)
                plt.subplot(num_plot_rows, num_plot_cols, (iteration//skip) * num_plot_cols + (k - k_min + 1))  # 
                plt.scatter(X[:, 0], X[:, 1], color=colors[closest_centroid], s=5)
                plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=15)
                
            # update centroids for every iteration but the last
            if iteration < (iterations - 1):
                centroids = np.nan_to_num(  # convert nan-values to 0s
                    np.array([np.nanmean(X[c_group], axis=0) for c_group in centroid_groups])
                )

        # calculate silhouette scores and mean SSE
        silhouette = silhouette_score(X, closest_centroid, centroid_groups)
        SSE_score = SSE(X, centroid_groups, centroids)
        SSB_score = SSB(centroid_groups, centroids)
        
        # plot silhouette coefficients
        plot_num += 1
        plt.subplot(num_plot_rows, num_plot_cols, (iterations//skip) * num_plot_cols + (k - k_min + 1))
        plt.scatter(X[:, 0], X[:, 1], color=color_scale(silhouette), s=5)
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=15)
        plt.xlabel(f"Silhouette score: {np.mean(silhouette):.2f}\nSSE: {SSE_score:.2f}\t SSB: {SSB_score:.2f}")

    
    plt.show()


def dbscan(X):
    pass


algorithms = (
    ('K-means', k_means),
    ('DBSCAN', dbscan),
)