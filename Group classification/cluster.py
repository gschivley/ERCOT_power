import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabaz_score
from sklearn.preprocessing import StandardScaler

class Clusters():
    def __init__(self, path):
        """
        Load cluster data, filter out non-fossil plants
        
        inputs:
            path: path and filename of csv file to load
        """
        self.cluster_df = pd.read_csv(path)
        fossil_codes = ['SUB', 'LIG', 'NG', 'DFO', 'PC']
        self.fossil_df = self.cluster_df.loc[self.cluster_df['fuel_type'].isin(fossil_codes)]
        self.fossil_with_ramp = self.fossil_df.dropna()
        
    def make_clusters(self, n_clusters=range(5,11)):
        """
        Cluster data according to a range of k values
        
        inputs:
            n_clusters: list of integers to use as values for k
        """
        X = self.fossil_with_ramp[['capacity', 'capacity_factor', 'efficiency', 'ramp_rate']]
        self.X_scaled = StandardScaler().fit_transform(X)
        
        self.cluster_data = pd.DataFrame(index=range(3,15), columns=['n_clusters', 'score', 'silhouette'])
        self.cluster_labels = {}
        
        for k in n_clusters:
            self.cluster_data.loc[k, 'n_clusters'] = k
            clusterer = KMeans(n_clusters=k)

            self.cluster_labels[k] = clusterer.fit_predict(self.X_scaled)

            self.cluster_data.loc[k, 'score'] = calinski_harabaz_score(self.X_scaled, self.cluster_labels[k])

            self.cluster_data.loc[k, 'silhouette'] = silhouette_score(self.X_scaled, self.cluster_labels[k])
            
    def evaluate_clusters(self):
        """
        Plot the calinski harabaz score and silhouette score for each k
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,3))
        self.cluster_data.plot(y='score', ax=ax1)
        # ax1.plot(range(3,15), cluster_data['score'])
        ax1.set_title('Calinski Harabaz score\nHigher is better')
        self.cluster_data.plot(y='silhouette', ax=ax2)
        # ax2.plot(range(3,15), silhouette)
        ax2.set_title('Silhouette score\nLower is better')
        plt.show()
    
    def export_cluster_id(self, k):
        """
        Return the cluster label for each plant
        
        inputs:
            k: a single k value
            
        outputs:
            cluster_labels[k]: an array of cluster labels
        """
        return self.cluster_labels[k]
        
    def label_and_export(self, k):
        """
        Add cluster labels to the fossil power plant dataframe and return.
        
        inputs:
            k: a single k value
        outputs:
            labeled_plants: dataframe with year, plant_id, and cluster label
        """
        self.labeled_plants = self.fossil_with_ramp.copy()
        self.labeled_plants.loc[:,'cluster'] = self.cluster_labels[k]
        
        return self.labeled_plants.loc[:,['year', 'plant_id', 'cluster']]
            

            
    