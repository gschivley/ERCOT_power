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
        
    def plot_clusters(self, ercot, allEPA, cluster_df):
        merged_epa_cluster = pd.merge(allEPA, cluster_df, left_on=['PLANT_ID', 'YEAR'], 
                             right_on=['plant_id', 'year'])
        grouped_clusters = merged_epa_cluster.loc[:,['Gen Change (MW)', 'GROSS LOAD (MW)', 'DATETIME', 'cluster']].groupby(['DATETIME', 'cluster']).sum()
        grouped_clusters.reset_index(inplace=True)
        grouped_clusters['DATETIME'] = pd.to_datetime(grouped_clusters['DATETIME'])
        grouped_clusters_ercot = pd.merge(grouped_clusters, ercot, on='DATETIME')
        grouped_clusters_ercot.loc[:,'year'] = grouped_clusters_ercot.loc[:,'DATETIME'].apply(lambda x: x.year)
        
        filtered_data = grouped_clusters_ercot.loc[grouped_clusters_ercot['year'].isin([2007, 2011, 2015])]

        plot = sns.lmplot('Net Load Change (MW)', 'Gen Change (MW)', data=filtered_data,
                   col='year', row='cluster', hue='cluster', robust=True, ci=None)
           
        return plot
        
    def plant_gen_delta(self, df):
        """
        For every plant in the input df, calculate the change in gross load (MW)
        from the previous hour.
    
        input:
            df: dataframe of EPA clean air markets data
        return:
            df: concatanated list of dataframes
        """
        df_list = []
        for plant in df['PLANT_ID'].unique():
            temp = df.loc[df['PLANT_ID'] == plant,:]
            temp.loc[:,'Gen Change (MW)'] = temp.loc[:,'GROSS LOAD (MW)'].values - temp.loc[:,'GROSS LOAD (MW)'].shift(1).values
            df_list.append(temp)
        return pd.concat(df_list)