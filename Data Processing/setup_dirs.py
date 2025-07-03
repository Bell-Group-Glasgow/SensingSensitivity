# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 10:17:53 2025

@author: marigl
"""
import os

# Function sets up all required output directories for processing and saving files

def setup_directories(base_path):
    
    # Dictionary of key directory paths based on the given base directory which 
    # is where your raw csv files should be stored and where you should be running the script from
    dirs = {
        'output': os.path.join(base_path, "Results"),
        'csvs': os.path.join(base_path, "Results", "csvs"),
        'csv_reacts': os.path.join(base_path, "Results", "csvs", "Reactants"),
        'csv_prods': os.path.join(base_path, "Results", "csvs", "Products"),
        'plot': os.path.join(base_path, "Results", "plots"),
        'raw_plot': os.path.join(base_path, "Results", "plots", "Raw Spectra"),
        'solv_minus_plot': os.path.join(base_path, "Results", "plots", "Solvent Subtarcted Spectra"),
        'data_proc_plots': os.path.join(base_path, "Results", "plots", "Data Processing Plots")
    }
    
    #Ensures each directory is created if it doesn't already exist
    for path in dirs.values():
        os.makedirs(path, exist_ok=True)
        
    # Returns a dictionary of directory paths for use in the main.py script
    return dirs

# Function returns a list of all .csv files that you want to process in the relevant working folder
def raw_csv_file(base_path):
    
    # Here we list all files in the folder you're working in 
    raw_files = os.listdir(base_path)

    # Filter out the csv files.
    # Dw if you have .CSV files (a quirk of the iCIR Software) the .lower() takes care of that.
    raw_csv_files = [file for file in raw_files if file.lower().endswith('.csv')]
    
    # The csvs are printed just so that you can check you're processing the right thing
    # Tehy are also returned as a list so that they can be called later.
    print(raw_csv_files)
    return raw_csv_files
