# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 10:35:39 2025

@author: marigl
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------------------------------------
# INITIAL RXN SCAN


def plot_initial_scan(csv_files, data_proc_plot_dir):

    # Here we extrcat the solvent and first reaction scan
    df_solvent_run = pd.read_csv(csv_files[0])
    df_first_scan = pd.read_csv(csv_files[1])

    # Subtracts the solvent intensity from the first scan, saves as a list
    subtracted = df_first_scan.iloc[:, 1] - df_solvent_run.iloc[:, 1]

    # Creates a new dataframe with wavenumbers as the first column and the subtracted intensity as column 2
    df_subtracted = pd.DataFrame(
        {"Wavenumbercm-1": df_solvent_run.iloc[:, 0], "Intensity": subtracted}
    )

    plt_name = "Initial Reaction Scan"
    color = "#7C7CB4"

    plt.figure()
    plt.plot(
        df_subtracted["Wavenumbercm-1"],
        df_subtracted["Intensity"],
        color=color,
    )
    plt.title(f"{plt_name}")
    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Δ Intensity (Sample - Solvent)")
    plt.ylim(-0.5, 1.7)
    plt.xlim(600, 4000)
    plt.tight_layout()

    plot_path = os.path.join(data_proc_plot_dir, f"{plt_name}.jpg")
    plt.savefig(plot_path)

    plt.show()

    plt.close()

    return df_subtracted, plt_name, plot_path, color


# ----------------------------------------------------------------------------------------------------------
# FINAL RXN SCAN


def plot_final_scan(csv_files, data_proc_plot_dir):
    last_scan_num = len(csv_files) - 1

    df_last_scan = pd.read_csv(csv_files[last_scan_num])
    df_solvent_run = pd.read_csv(csv_files[0])

    # Subtracts the solvent intensity from the first scan, saves as a list
    subtracted_final = df_last_scan.iloc[:, 1] - df_solvent_run.iloc[:, 1]

    # Creates a new dataframe with wavenumbers as the first column and the subtracted intensity as column 2
    df_subtracted_final = pd.DataFrame(
        {
            "Wavenumbercm-1": df_solvent_run.iloc[:, 0],
            "Intensity": subtracted_final,
        }
    )

    plt_name_final = "Final Reaction Scan"
    color = "#7C7CB4"

    plt.figure()
    plt.plot(
        df_subtracted_final["Wavenumbercm-1"],
        df_subtracted_final["Intensity"],
        color=color,
    )
    plt.title(f"{plt_name_final}")
    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Δ Intensity (Sample - Solvent)")
    plt.ylim(-0.5, 1.7)
    plt.xlim(600, 4000)
    plt.tight_layout()

    plot_path = os.path.join(data_proc_plot_dir, f"{plt_name_final}.jpg")
    plt.savefig(plot_path)

    plt.show()

    plt.close()

    return df_subtracted_final, plt_name_final, plot_path, color


# ----------------------------------------------------------------------------------------------------------
# PRODUCT RXN SCAN


def plot_product_scan(csv_files, data_proc_plot_dir):

    last_scan_num = len(csv_files) - 1

    df_last_scan = pd.read_csv(csv_files[last_scan_num])
    df_solvent_run = pd.read_csv(csv_files[0])
    df_first_scan = pd.read_csv(csv_files[1])
    # Subtracts the solvent intensity from the first scan, saves as a list
    subtracted_prod = df_last_scan.iloc[:, 1] - df_first_scan.iloc[:, 1]

    # Creates a new dataframe with wavenumbers as the first column and the subtracted intensity as column 2
    df_subtracted_prod = pd.DataFrame(
        {
            "Wavenumbercm-1": df_solvent_run.iloc[:, 0],
            "Intensity": subtracted_prod,
        }
    )

    plt_name_prod = "Max Product in Reaction Scan"
    color = "#7C7CB4"

    plt.figure()
    plt.plot(
        df_subtracted_prod["Wavenumbercm-1"],
        df_subtracted_prod["Intensity"],
        color=color,
    )
    plt.title(f"{plt_name_prod}")
    plt.xlabel("Wavenumber (cm⁻¹)")
    plt.ylabel("Δ Intensity (Inital Scan - Final Scan)")
    plt.ylim(-0.5, 1.7)
    plt.xlim(600, 4000)
    plt.tight_layout()

    plot_path = os.path.join(data_proc_plot_dir, f"{plt_name_prod}.jpg")
    plt.savefig(plot_path)

    plt.show()

    plt.close()

    return df_subtracted_prod, plt_name_prod, plot_path, color
