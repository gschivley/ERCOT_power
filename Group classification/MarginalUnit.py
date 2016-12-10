from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import gzip
import cPickle as pickle

class Marginal_Unit():
    def __init__(self, ercotPath, epaPath, clusterPath, eiaPath, fuelPath):
        ercot = pd.read_csv(ercotPath, index_col=0)
        epaDict = self.load_zipped_pickle(epaPath)
        cluster_df = pd.read_csv('Cluster labels.csv')
        eia860Dict = pickle.load(open(eiaPath, "rb"))
        fuel_prices = pd.read_csv(fuelPath, index_col=0)
        
        ercot = self.process_ercot(ercot)
        allEPA = self.process_epa(epaDict)
        group_cluster = self.create_clusters(allEPA, cluster_df, ercot)
        
        groupCapacity = self.calc_group_capacity(eia860Dict, cluster_df)
        group_cluster = pd.merge(groupCapacity, group_cluster, on=['cluster_id_6', 'year'])

        group_cluster.loc[:,'Month'] = group_cluster.loc[:,'DATETIME'].apply(lambda x: x.month)
        group_cluster = group_cluster.rename(columns = {'year':'Year'})
        
        self.X = pd.merge(group_cluster, fuel_prices, on=['Year', 'Month'])
        self.y = self.X.loc[:,['DATETIME', 'cluster_id_6', 'Gen Change (MW)']]
        self.X.drop('Gen Change (MW)', axis=1, inplace=True)


    def plotClusters(self, clusterData):
        

    def getX(self):
        return self.X
        
    def getY(self):
        return self.y

    def process_ercot(self, ercot):
        ercot.loc[:,'Net Load (MW)'] = ercot.loc[:,'ERCOT Load, MW'] - ercot.loc[:,'Total Wind Output, MW']
        ercot.loc[1:,'Net Load Change (MW)'] = ercot.iloc[1:,-1].values - ercot.iloc[:-1,-1].values
        ercot.loc[:,'DATETIME'] = pd.to_datetime(ercot.index)        
        
        return ercot
        
        
    def process_epa(self, epaDict):
        allEPA = pd.concat(epaDict)
        allEPA.fillna(0, inplace=True)
        allEPA = self.plant_gen_delta(allEPA)
        allEPA.reset_index(drop=True, inplace=True)
        
        return allEPA
        
        
    def create_clusters(self, allEPA, cluster_df, ercot):
        merged_epa_cluster = pd.merge(allEPA, cluster_df, left_on=['PLANT_ID', 'YEAR'], 
                             right_on=['plant_id', 'year'])
                             
        grouped_clusters = merged_epa_cluster.loc[:,['Gen Change (MW)', 'GROSS LOAD (MW)', 'DATETIME', 'cluster_id_6']].groupby(['DATETIME', 'cluster_id_6']).sum()
        grouped_clusters.reset_index(inplace=True)
        
        grouped_clusters = pd.merge(grouped_clusters, ercot, on='DATETIME')
        grouped_clusters.loc[:,'year'] = grouped_clusters.loc[:,'DATETIME'].apply(lambda x: x.year)
        return grouped_clusters
                        
               
    def calc_group_capacity(self, eia860Dict, cluster_df):
        #Add year to as a column
        for k in eia860Dict.keys():
            eia860Dict[k]["Year"] = k
        
        #Flatten dictionary, rename columns, and do inner join 
        merged860 = pd.concat(eia860Dict)
        merged860.columns = ["plant_id", "nameplate_capacity", "year"]
        merged860 = cluster_df.merge(merged860, on=["plant_id", "year"])
        groupCapacity = merged860.loc[:,["cluster_id_6", "year", "nameplate_capacity"]].groupby(by=["cluster_id_6", "year"]).sum()
        groupCapacity.reset_index(inplace=True)
        
        return groupCapacity
        
        
    def load_zipped_pickle(self, filename):
        with gzip.open(filename, 'rb') as f:
            loaded_object = pickle.load(f)
            return loaded_object
            
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
            gen_change = temp.loc[:,'GROSS LOAD (MW)'].values - temp.loc[:,'GROSS LOAD (MW)'].shift(1).values
            temp.loc[:,'Gen Change (MW)'] = gen_change
            df_list.append(temp)
        return pd.concat(df_list)