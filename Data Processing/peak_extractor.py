# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:16:52 2025

@author: marigl
"""

import os
import pandas as pd


# This function subtracts the solvent intensity from a given scan
def subtract_solvent(df_scan, df_solvent):
    
    # Returns the delta intensity of the scan and the solvent
    return df_scan.iloc[:, 1] - df_solvent.iloc[:, 1]

#----------------------------------------------------------------------------------------------------------

# Extracts the top N peaks (highest intensity) below 1900 cm⁻¹ from the spectrum
# N == 6 automatically, but can be changed in the main.py script
def extract_top_peaks(wavenumbers, intensity_series, num_peaks=6):
    
    # Creates a temporary DataFrame for wavenumbers and intensities
    df_temp = pd.DataFrame({
        'Wavenumbercm-1': wavenumbers,
        'Intensity': intensity_series
    })
    
    # Filters to only include peaks below 1900 cm⁻¹ to avoid the diamond region of the probe
    df_filtered = df_temp[df_temp['Wavenumbercm-1'] < 1900]
    
    # Return the wavenumbers of the top N peaks of highest intensity
    return df_filtered.nlargest(num_peaks, 'Intensity')['Wavenumbercm-1'].tolist()

#----------------------------------------------------------------------------------------------------------

# Searches through all the csv files to find exact matches of given target wavenumbers
# (of the intensities extracted initially) in all the raw csvs and pulls them out for saving later
def collect_exact_matches(targets, file_list):
    
    # Prepares an empty list of lists to hold matches for each target peak
    collected = [[] for _ in targets]
    
    
    for file in file_list:
        
        # Read the csv file for each spectrum
        df = pd.read_csv(file)
        
        # extracts timestamp and renames columns for consistency
        timestamp = df.columns[1]
        df.columns = ['Wavenumber', 'Intensity']
        
        # Here we look for exact matches for each target wavenumber
        for i, target in enumerate(targets):
            matches = df[df['Wavenumber'] == target].copy()
            
            # this adds the data to matched rows
            if not matches.empty:
                matches['Timestamp'] = timestamp
                matches['SourceFile'] = file
                
                # here we append the collected targets 
                collected[i].extend(matches.to_dict('records'))
            else:
                print(f"No match for {target} in {file}")
                
    # Converts everything to DataFrames (one per peak)
    return [pd.DataFrame(c).reset_index(drop=True) for c in collected]

#----------------------------------------------------------------------------------------------------------

# Saves each DataFrame (one per target peak) to an individual Excel file
def save_dataframes_to_excel(dfs, targets, output_dir):
    for df, target in zip(dfs, targets):
        sheet_name = f"{target}"
        book_name = os.path.join(output_dir, f"{target}.xlsx")
        df.to_excel(book_name, index=False, header=True, sheet_name=sheet_name)
        
#----------------------------------------------------------------------------------------------------------

# Saves each DataFrame (one per target peak) to individual csv files which will be used for the plotting later on
def save_dataframes_to_csv(dfs, targets, output_dir):
    for df, target in zip(dfs, targets):
        file_path = os.path.join(output_dir, f"{target}.csv")
        df.to_csv(file_path, index=False)