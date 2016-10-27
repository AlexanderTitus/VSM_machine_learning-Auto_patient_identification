# Imports and setting up the workspace
import pandas as pd
from sklearn import cluster

from matplotlib import pyplot
import numpy as np
import scipy.spatial.distance as ssd
import vsm as vsm


########################
# Create hierarchical clusters
########################
def create_hier_clusters(new_data, k=15, model='LSI'):
    info = vsm.vsm_model(new_data, model=model)
    sims = info[0]
    documents = info[1]
    sim_DF = pd.DataFrame(sims)

    data = sim_DF.values
    hier = cluster.AgglomerativeClustering(n_clusters=k)

    hier.fit(data)

    labels = hier.labels_

    sets = [data[np.where(labels == i)] for i in range(k)]
    indicies = [np.where(labels == i)[0] for i in range(k)]
    doc_clusters = [[documents[index] for index in indicies[i]] for i in range(len(indicies))]

    return doc_clusters, sets, data, labels

########################
# Create the clusters to check against later
########################
def create_clusters(new_data, k=15, second_cluster=False, model='LSI'):

    info = vsm.vsm_model(new_data, model=model)
    sims = info[0]
    documents = info[1]
    sim_DF = pd.DataFrame(sims)

    data = sim_DF.values

    if not second_cluster:
        kmeans = cluster.KMeans(n_clusters=k, random_state=k)
    else:
        k2 = k * 100 + k
        kmeans = cluster.KMeans(n_clusters=k, random_state=k2)

    kmeans.fit(data)

    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    sets = [data[np.where(labels == i)] for i in range(k)]
    indicies = [np.where(labels == i)[0] for i in range(k)]
    doc_clusters = [[documents[index] for index in indicies[i]] for i in range(len(indicies))]

    return doc_clusters, sets, data, labels, centroids, sim_DF


########################
# K-means plotting
########################
def plot_clusters(k, data, labels, centroids):
    for i in range(k):
        # select only data observations with cluster label == i
        ds = data[np.where(labels == i)]
        # plot the data observations
        pyplot.plot(ds[:, 0], ds[:, 1], 'o')
        # plot the centroids
        lines = pyplot.plot(centroids[i, 0], centroids[i, 1], 'kx')
        pyplot.annotate(i, xy=(centroids[i, 0], centroids[i, 1]), textcoords='offset points')
        # make the centroid x's bigger
        pyplot.setp(lines, ms=15.0)
        pyplot.setp(lines, mew=2.0)
    pyplot.show()


########################
# Error plotting
########################
def plot_kmeans_error(k_start, k_end, data):
    # Calculate variance (http://www.slideshare.net/SarahGuido/kmeans-clustering-with-scikitlearn)
    k_range = range(k_start,k_end)
    k_means_var = [cluster.KMeans(n_clusters=k).fit(data) for k in k_range]
    centroids = [X.cluster_centers_ for X in k_means_var]
    k_euclid = [ssd.cdist(data, cent, 'euclidean') for cent in centroids]
    dist = [np.min(ke, axis=1) for ke in k_euclid]
    wcss = [sum(d**2) for d in dist]
    tss = sum(ssd.pdist(data)**2)/data.shape[0]
    bss = tss - wcss

    pyplot.plot(k_range, bss/tss)
    # pyplot.suptitle('variance v. clusters', fontsize=20)
    # pyplot.xlabel('# of clusters', fontsize=18)
    # pyplot.ylabel('% variance explained', fontsize=16)
    pyplot.show()


########################
# Classifying date-code clusters for K = 8
########################
def classify_cluster(cluster_number):
    cluster = 'Miscellaneous'
    code = 'cpt_rollup_code_99'
    if cluster_number == 0:
        cluster = cluster
        code = 'cpt_rollup_code_99'
    elif cluster_number == 1 or cluster_number == 2 or cluster_number == 4:
        cluster = 'Partial mastectomy/lymphadenectomy'
        code = 'cpt_rollup_code_1'
    elif cluster_number == 3 or cluster_number == 5:
        cluster = 'Simple complete mastectomy'
        code = 'cpt_rollup_code_2'
    elif cluster_number == 6:
        cluster = 'Biopsy'
        code = 'cpt_rollup_code_3'
    elif cluster == 7:
        cluster = 'Partial or Simple complete mastectomy'
        code = 'cpt_rollup_code_4'
    else:
        cluster = cluster
        code = 'cpt_rollup_code_99'

    return code, cluster


########################
# Check if a string group of codes is in one of the clusters and return the cluster
########################
def check_in_cluster(codes_string, clusters):
    for i, cluster in enumerate(clusters):
        if codes_string in cluster:
            classify = classify_cluster(i)
            return i, classify
    return i, classify_cluster(codes_string)

