# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:38:34 2025

@author: marigl
"""

# Here we import all the already available python libraries

import os
import pandas as pd

# This is a custom defined set of hex code colours for the plots - you can replace with your own in the colours.py file
import colours as clr

# Here we import all the custom defined functions for the data processing
from setup_dirs import setup_directories, raw_csv_file
from raw_spectra_plotter import plot_raw_spectra
from solvent_subtracted import plot_solvent_subtracted
from user_zoom_mult import user_zoom_mult

from initial_final_scan_react import (
    plot_initial_scan, 
    plot_final_scan, 
    plot_product_scan
    )

from user_zoom_by_one import user_zoom_by_one

from peak_extractor import (
    subtract_solvent,
    extract_top_peaks,
    collect_exact_matches,
    save_dataframes_to_excel,
    save_dataframes_to_csv,
)

from vs_time_graphs import (
    plot_intensity_vs_time, 
    plot_all_peaks_combined
    )
# from peak_extractor import subtract_solvent, extract_top_peaks, collect_exact_matches, save_dataframes_to_excel, save_dataframes_to_csv

# from user_zoom import *
# from vs_time_graphs import *
# from initial_final_scan_react import *

if __name__ == "__main__":
    
    base_path = os.getcwd()
    

    # This sets up directories that will be used to save files and extract data to and from and plots
    dirs = setup_directories(base_path)

    # This returns a list of raw .csv files so that you can check you're plotting what you want
    input_csv_path = dirs["input_csvs"]
    print(f"\n The input csv files are stored in: {input_csv_path}")
    csv_files = raw_csv_file(input_csv_path)  # this now returns the list
    print(f"\n The raw csv files are: {csv_files}")

    # Generates full paths to the csvs used for plotting
    full_csv_paths = [os.path.join(input_csv_path, file) for file in csv_files]
    
    print('''\n We're going to look at some PRE-processing. 
          \n First, the raw spectra will be plotted and saved in Results>Plots>Raw Spectra. 
          \n After this you will have an opportunity to change the axes.
          \n The same will be done for solvent subtracted spectra.''')
#----------------------------------------------------------------------------------------------------------

    # Plots raw spectra files and collect results
    raw_results = plot_raw_spectra(full_csv_paths, dirs["raw_plot"])

    # Asks user if they want to zoom in on all raw spectra, if yes the zooming 'tool' is initiated.
    zoom_all_raw = input("\n Do you want to replot all RAW spectra with custom zoom limits? (y/n): ").lower()
    if zoom_all_raw in ["y", "yes"]:
        user_zoom_mult(raw_results, xlim=(600, 4000), ylim=(-0.5, 1.7))

#----------------------------------------------------------------------------------------------------------

    print('''\n Now, the solvent subtracted spectra will be plotted and saved in Results>Plots>Solvent Subtracted Spectra. 
          \n After this you will have an opportunity to change the axes.''')

    # Plots solvent subtracted spectra and collect results
    solv_results = plot_solvent_subtracted(full_csv_paths, dirs["solv_minus_plot"])
    
    # Asks user if they want to zoom in on all solvent subtracted spectra, if yes the zooming 'tool' is initiated.
    zoom_all_subtracted = input("\n Do you want to replot all SUBTRACTED spectra with custom zoom limits? (y/n): ").lower()
    if zoom_all_subtracted in ["y", "yes"]:
        user_zoom_mult(solv_results, xlim=(600, 4000), ylim=(-0.015, 0.015))

#----------------------------------------------------------------------------------------------------------
    print('''\n We're now going to do some POST-processing. 
          \n First, we're going to identify the reactant and product peaks.
          \n We'll do this by subtracting the solvent from the first scan with reagents and also subtracting the first scan from the last scan to identify the products.
          \n As with last time - you'll get a chance to adjust the axis limits. You may need to close the plot window to continue.''')
    
    # Plots initial reaction scan (aka one that is just showing rectants (solvent subtracted))
    # And asks user if they wish to adjust the axes
    initial_scan = plot_initial_scan(full_csv_paths, dirs['data_proc_plots'])    
    print("\n You've just seen the INITIAL (MAX REACTANT) rxn scan")
    user_zoom_by_one(*initial_scan)
    
    # Plots final reaction scan (aka one that is just showing any left over reactants and products (solvent subtracted))
    # And asks user if they wish to adjust the axes
    final_scan = plot_final_scan(full_csv_paths, dirs['data_proc_plots'])
    print("\n You've just seen the FINAL rxn scan")
    user_zoom_by_one(*final_scan)
    
    # Plots product reaction scan (aka one that is just products rectants (reactant subtracted))
    # And asks user if they wish to adjust the axes
    product_scan = plot_product_scan(full_csv_paths, dirs['data_proc_plots'])
    print("\n You've just seen the MAX PRODUCT rxn scan")
    user_zoom_by_one(*product_scan)

#----------------------------------------------------------------------------------------------------------
    print('''\n We're now going to extract the max reactnat peaks and product peaks into csv files. 
          \n The generated csvs and xls files will be found in the "csvs" folder.''') 
          
    # Settings for the file processing to extract the desired reactant and product maxima
    reactant_indices = (0, 1)  # solvent, first scan
    product_index = -1 #last scan
    num_peaks = 6 #number of peaks you want to identify in reacts and prods
    
#----------------------------------------------------------------------------------------------------------
    
    # Reactant Peak Processing 
    df_solvent = pd.read_csv(full_csv_paths[reactant_indices[0]])
    df_first = pd.read_csv(full_csv_paths[reactant_indices[1]])
    
    subtracted_react = subtract_solvent(df_first, df_solvent)
    target_peaks_react = extract_top_peaks(df_solvent.iloc[:, 0], subtracted_react)

    dfs_react = collect_exact_matches(target_peaks_react, full_csv_paths)
    save_dataframes_to_excel(dfs_react, target_peaks_react, dirs['csv_reacts'])
    save_dataframes_to_csv(dfs_react, target_peaks_react, dirs['csv_reacts'])
    
    print(f"The extracted max peaks for reactants was successfully saved in {dirs['csv_reacts']}")
    
#----------------------------------------------------------------------------------------------------------

    # Product Peak Processing 
    df_last_scan = pd.read_csv(full_csv_paths[product_index])
    subtracted_prod = subtract_solvent(df_last_scan, df_first)
    target_peaks_prod = extract_top_peaks(df_last_scan.iloc[:, 0], subtracted_prod)

    dfs_prod = collect_exact_matches(target_peaks_prod, full_csv_paths)
    save_dataframes_to_excel(dfs_prod, target_peaks_prod, dirs['csv_prods'])
    save_dataframes_to_csv(dfs_prod, target_peaks_prod, dirs['csv_prods'])
              
    print(f"The extracted max peaks for products was successfully saved in {dirs['csv_prods']}")
    
#----------------------------------------------------------------------------------------------------------
    print('''\n Let's now plot the extracted maxima with time and fit some trendlines to the data. 
          \n The generated plots will be found in the "Processed Data Plots" folder.''')

    #Plots the extrcated peak intensities over time for both reacts and prods as individual plots
    plot_intensity_vs_time(dirs['csv_reacts'], clr.max_colours_react, dirs["data_proc_plots"])
    plot_intensity_vs_time(dirs['csv_prods'], clr.max_colours_prod, dirs["data_proc_plots"])
    
    #Plots the extrcated peak intensities over time for both reacts and prods on the same plot
    plot_all_peaks_combined(dirs['csv_reacts'], clr.max_colours_react, dirs["data_proc_plots"], title="Combined Peak Intensities - Reactants")
    plot_all_peaks_combined(dirs['csv_prods'], clr.max_colours_prod, dirs["data_proc_plots"], title="Combined Peak Intensities - Products")








