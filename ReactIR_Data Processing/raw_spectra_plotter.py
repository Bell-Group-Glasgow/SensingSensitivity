# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:16:52 2025

@author: marigl
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_raw_spectra(
    csv_files, output_dir, xlim=(600, 4000), ylim=(-0.5, 1.7)
):

    # This creates an empty list to store function outputs for use by the zooming funciton
    results = []

    # Loop is set up to plot and collect data from all the raw csvs
    for file in csv_files:
        df = pd.read_csv(file)

        # Here we extract the timestampand clean off the file name to extract the plot name
        timestamp = df.columns[1]
        base_name = os.path.basename(file)
        plt_name = os.path.splitext(base_name)[0]
        color = "#EF3B80"

        # Plotting parameters of the raw spectra
        plt.figure()
        plt.plot(df["Wavenumbercm-1"], df.iloc[:, 1], color=color)
        plt.title(f"{plt_name} - {timestamp}")
        plt.xlabel("Wavenumber (cm⁻¹)")
        plt.ylabel("Intensity")
        plt.ylim(*ylim)
        plt.xlim(*xlim)
        plt.tight_layout()

        # This is where the graph is saved and shown
        plot_path = os.path.join(output_dir, f"{plt_name}.jpg")
        plt.savefig(plot_path)
        # plt.show()
        plt.close()

        # Prepares data for zooming in feature later
        df_plot = df[["Wavenumbercm-1", df.columns[1]]].copy()
        df_plot.columns = ["Wavenumbercm-1", "Intensity"]
        results.append((df_plot, plt_name, plot_path, color))

    return results
