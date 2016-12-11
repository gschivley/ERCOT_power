import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_residuals(y_pr, y_va):
    """
    Plot residuals of predicted results, faceted by cluster.
    
    inputs:
        y_pr: numpy array of predicted values
        y_va: pandas dataframe of true validation results, with columns 'Gen Change (MW)' and 'cluster'
        
    """
        
    y_residuals = pd.DataFrame(columns=['y_pr', 'y_va', 'Residuals', 'Cluster'])
    y_residuals.loc[:,'Predicted value'] = y_pr
    y_residuals.loc[:,'y_va'] = y_va.loc[:,'Gen Change (MW)'].values
    y_residuals.loc[:,'Cluster'] = y_va.loc[:,'cluster'].values
    y_residuals.loc[:,'Residuals'] = y_pr - y_va.loc[:,'Gen Change (MW)'].values
    
    g = sns.FacetGrid(y_residuals, hue='Cluster', col='Cluster', col_wrap=3)
    g.map(plt.scatter, 'Predicted value', 'Residuals')
    g.add_legend()
    plt.show()