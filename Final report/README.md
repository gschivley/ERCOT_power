**GROUP MEMBERS**: 
Nikhil Agarwal - nikhilba   
Greg Schivley - gschivle  
Tim Tau - ttau

**HOW TO RUN CODE**: 
The notebook "Final report.ipynb" is set up so that it can be run in a linear fashion from start to end so long as all data files and supporting scripts are present. The easiest way to ensure that all required files are present is to clone the repository at https://github.com/gschivley/ERCOT_power.

Once the repository is cloned, the final report notebook is present in the `Final report` folder.

Most libraries and functions used in the notebook should be included in the Anaconda distribution or are referenced from local scripts. The major exception is XGBoost, which is used to show learning and validation curves for the boosted gradient regression tree method. The model score and residual plot are included using `GradientBoostingRegressor` from scikit-learn.

**nbviewer link**: 
http://nbviewer.jupyter.org/github/gschivley/ERCOT_power/blob/master/Final%20report/Final%20Report.ipynb

**Large files**: 
The notebook imports over 1GB of data from a range of files. All data are available at the GitHub repository. The final report notebook has been written so that all data files are in the same folder as the notebook (https://github.com/gschivley/ERCOT_power/tree/master/Final%20report).
