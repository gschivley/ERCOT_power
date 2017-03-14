# ERCOT Power (Electric Reliability Council of Texas)

## CONTRIBUTORS
- Greg Schivley - gschivle
- Nikhil Agarwal - nikhilba
- Tim Tau - ttau

## INTRODUCTION

This repository contains the process and results of a data science project to predict the increases or decreases in electricity generation at fossil power plants in Texas. It begins with data collection and processing, and shows how the data are combined. The data fall into two general groups: 1) average operating characteristics of power plants over the course of a year, and 2) the state of the ERCOT grid at a given point in time (t) and the hour directly preceding t. We use the first set of data to group power plants into clusters, and the second set of data to predict the behavior of each cluster

## HOW TO RUN CODE

The notebook "Final report.ipynb" is set up so that it can be run in a linear fashion from start to end so long as all data files and supporting scripts are present. The easiest way to ensure that all required files are present is to clone the repository at https://github.com/gschivley/ERCOT_power.

Most libraries and functions used in the notebook should be included in the Anaconda distribution or are referenced from local scripts. The major exception is XGBoost, which is used to show learning and validation curves for the boosted gradient regression tree method. The model score and residual plot are included using `GradientBoostingRegressor` from scikit-learn.

## Final Report
Once the repository is cloned, the final report notebook is present in the `Final report` folder.
The final report can also be viewed at this [nbviewer link](http://nbviewer.jupyter.org/github/gschivley/ERCOT_power/blob/master/Final%20report/Final%20Report%20-%20clean.ipynb)
