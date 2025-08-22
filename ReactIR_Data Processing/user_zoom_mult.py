# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 13:32:49 2025

@author: marigl
"""

import os
import matplotlib.pyplot as plt

"""
Zoom into multiple spectra based on user-defined limits and save them in a separate folder.

Args:
    results (list): List of tuples containing (df_subtracted, plt_name, plot_path, color).
    xlim (tuple): Default X-axis limits for the plots.
    ylim (tuple): Default Y-axis limits for the plots.
    zoom_dir_name (str): Directory name to store the zoomed-in plots.
"""


def user_zoom_mult(
    results, xlim=(600, 4000), ylim=(-0.015, 0.015), zoom_dir_name="Zoomed"
):

    # This checks to see if your spectra (raw or solvent subtracted) have already been plotted.
    # Uses the values rturned by those respective functions to populate the rest of the zoom function.
    if not results:
        print("No results to zoom.")
        return

    # Here we make a "Zoomed" subfolder in the directory where the plots are being saved from first result
    plot_path = results[0][2]
    zoom_dir = os.path.join(os.path.dirname(plot_path), zoom_dir_name)
    os.makedirs(zoom_dir, exist_ok=True)

    # We set initial zoom limits to default values
    x_lims = xlim
    y_lims = ylim

    # This begin the interractive zoom loop
    while True:

        # We ask the user to set zoom limits for all plots
        # You will have seen what the plots look initially so can fine tune the region you want to look in
        # The logic is straight forward, the except segement ensures that you can
        # still get a plot even if you type nonsense into the command line

        # You'll be asked to zoom in until you say no
        user_input = input(
            "Do you want to zoom in to a region on the spectrum? (y/n): "
        ).lower()
        if user_input in ["y", "yes"]:
            # x-axis
            which_region_x = input(
                "Do you want to zoom in on the x-axis? (y/n): "
            ).lower()
            if which_region_x in ["y", "yes"]:
                try:
                    x_bounds = input(
                        "Enter lower and upper x bounds separated by ', ': "
                    )
                    x_lims = tuple(map(float, x_bounds.split(",")))
                except Exception:
                    print(f"Invalid input. Using default x limits {xlim}.")
                    x_lims = xlim
            elif which_region_x in ["n", "no"]:
                x_lims = xlim

            # y-axis
            which_region_y = input(
                "Do you want to zoom in on the y-axis? (y/n): "
            ).lower()
            if which_region_y in ["y", "yes"]:
                try:
                    y_bounds = input(
                        "Enter lower and upper y bounds separated by ', ': "
                    )
                    y_lims = tuple(map(float, y_bounds.split(",")))
                except Exception:
                    print(f"Invalid input. Using default y limits {ylim}.")
                    y_lims = ylim
            elif which_region_y in ["n", "no"]:
                y_lims = ylim
        # If user doesn't want to change the limits or has mis-clicked it will plot with the default limits
        else:
            x_lims = xlim
            y_lims = ylim

        # Plots all spectra with current zoom settings but doesn't save them - you will be asked that separetely :)
        for df_subtracted, plt_name, plot_path, color in results:
            plt.figure()
            plt.plot(
                df_subtracted["Wavenumbercm-1"],
                df_subtracted["Intensity"],
                color=color,
            )
            plt.title(plt_name)
            plt.xlabel("Wavenumber (cm⁻¹)")
            plt.ylabel("Δ Intensity (Sample - Solvent)")
            plt.xlim(*x_lims)
            plt.ylim(*y_lims)
            plt.tight_layout()
            zoom_filename = f"{plt_name}_zoom.jpg"
            zoom_path = os.path.join(zoom_dir, zoom_filename)
            plt.savefig(zoom_path)
            # plt.show()
            plt.close()

        # Asks the user if further zooming is needed
        user_input = input("Do you want to zoom in further? (y/n): ").lower()
        if user_input not in ["y", "yes"]:

            # If the user says no, then plots are saved with the last implemented limits that were shown
            for df_subtracted, plt_name, plot_path, color in results:
                plt.figure()
                plt.plot(
                    df_subtracted["Wavenumbercm-1"],
                    df_subtracted["Intensity"],
                    color=color,
                )
                plt.title(plt_name)
                plt.xlabel("Wavenumber (cm⁻¹)")
                plt.ylabel("Δ Intensity (Sample - Solvent)")
                plt.xlim(*x_lims)
                plt.ylim(*y_lims)
                plt.tight_layout()
                zoom_filename = f"{plt_name}_zoom.jpg"
                zoom_path = os.path.join(zoom_dir, zoom_filename)
                plt.savefig(zoom_path)
                plt.close()
            break  # Exit zoom loop

    print(f"\nAll zoomed plots saved to: {zoom_dir}")
