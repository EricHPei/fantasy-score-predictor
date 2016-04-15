from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm
plt.style.use('ggplot')


def get_silhouette_score(X,nclust):
    '''
    calculate average silhouette score
    :param nclust: int, number of clusters
    :param X: numpy array, data set to cluster
    :return: float, average silhouette score
    '''
    km = KMeans(nclust, random_state=30)
    km.fit(X)
    sil_avg = silhouette_score(X, km.labels_)
    return sil_avg

def plot_silhouette(X,nrange):
    '''
    plot average silhouette score against the number of clusters
    :param nrange: int, indicates range of cluster numbers
    :param X: numpy array, data set to cluster
    :raise: plot
    '''
    sil_scores = [get_silhouette_score(X,i) for i in xrange(2,nrange)]
    plt.plot(range(2,nrange), sil_scores)
    plt.xlabel('K')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Score vs K')

def cluster_plot(X,n_clusters):
    '''
    plot silhouette and clusters
    :param x: numpy array
    :param nrange: int, range of cluster numbers
    :return: plots
    '''

    # Create a subplot with 1 row and 2 columns
    fig, ax1 = plt.subplots(1)
    fig.set_size_inches(7, 5)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
    ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
    ax1.set_ylim([0, len(X) + (n_clusters + 1) * 10])

    # Initialize the clusterer with n_clusters value and a random generator
    # seed of 10 for reproducibility.
    clusterer = KMeans(n_clusters=n_clusters, random_state=0)
    cluster_labels = clusterer.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    silhouette_avg = silhouette_score(X, cluster_labels)
    print("For n_clusters =", n_clusters,
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
    sample_silhouette_values = silhouette_samples(X, cluster_labels)

    y_lower = 10
    for i in range(n_clusters):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
        ith_cluster_silhouette_values = \
            sample_silhouette_values[cluster_labels == i]

        ith_cluster_silhouette_values.sort()

        size_cluster_i = ith_cluster_silhouette_values.shape[0]
        y_upper = y_lower + size_cluster_i

        color = cm.spectral(float(i) / n_clusters)
        ax1.fill_betweenx(np.arange(y_lower, y_upper),
                          0, ith_cluster_silhouette_values,
                          facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
        ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
        y_lower = y_upper + 10  # 10 for the 0 samples

    ax1.set_title("The silhouette plot for the various clusters (K = "+str(n_clusters)+")")
    ax1.set_xlabel("The silhouette coefficient values")
    ax1.set_ylabel("Cluster label")

    # The vertical line for average silhoutte score of all the values
    ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

    ax1.set_yticks([])  # Clear the yaxis labels / ticks
    ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])