# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 11:34:21 2025

@author: marigl
"""

import pandas as pd
import os
import matplotlib.pyplot as plt


def plot_solvent_subtracted(
    csv_files, output_dir, xlim=(600, 4000), ylim=(-0.5, 1.7)
):

    # Reads the first file as the solvent spectrum (baseline), and extracts the
    # wavenumber and intensity columns
    df_solvent = pd.read_csv(csv_files[0])
    wav_solvent = df_solvent.iloc[:, 0]
    int_solvent = df_solvent.iloc[:, 1]

    # This creates an empty list to store function outputs for use by the zooming funciton
    results = []

    # This section ensures that we iterate through all other spectra files except for the solvent
    for file in csv_files[1:]:
        df = pd.read_csv(file)

        # Validates the expected no of columns in the csv file that iCIR spits out for you
        if df.shape[1] != 2:
            print(f"Skipping {file}: unexpected number of columns.")
            continue

        # Extracts timestamp from the second column's name and cleans it up for use later in the plot name
        timestamp = df.columns[1]
        timestamp_clean = timestamp.replace(":", "-")
        color = "#ADD45C"

        # Extracts sample spectrum data
        wav_sample = df.iloc[:, 0]
        int_sample = df.iloc[:, 1]

        # Here we subtract the solvent spectrum from the sample spectrum and save it as dataframe
        # for use later in the zoom feature in main.py
        subtracted = int_sample - int_solvent

        df_subtracted = pd.DataFrame(
            {"Wavenumbercm-1": wav_sample, "Intensity": subtracted}
        )

        # Creates a plot title and filename
        base_name = os.path.basename(file)
        name_without_ext = os.path.splitext(base_name)[0]
        plt_name = f"{name_without_ext}_{timestamp_clean}"
        plot_path = os.path.join(output_dir, f"{plt_name}.jpg")

        # Plotting parameters of the raw spectra
        plt.figure()
        plt.plot(wav_sample, subtracted, color=color)
        plt.title(f"{plt_name}")
        plt.xlabel("Wavenumber (cm⁻¹)")
        plt.ylabel("Δ Intensity (Sample - Solvent)")
        plt.xlim(*xlim)
        plt.ylim(*ylim)
        plt.tight_layout()

        # This is where the graph is saved and shown
        plt.savefig(plot_path)
        # plt.show()
        plt.close()

        # Stores plot data for batch zooming later
        results.append((df_subtracted, plt_name, plot_path, color))

    return results
