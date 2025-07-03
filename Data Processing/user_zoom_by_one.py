# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:16:52 2025

@author: marigl
"""
import os
import matplotlib.pyplot as plt


"""
Interactive zoom and save function for subtracted spectral data.

Parameters:
    df_subtracted (pd.DataFrame): DataFrame with 'Wavenumbercm-1' and 'Intensity' columns.
    plt_name (str): Title for the plot.
    plot_path (str): File path (without extension) to save plots.
    default_xlim (tuple): Default x-axis limits.
    default_ylim (tuple): Default y-axis limits.
"""

def user_zoom_by_one(df_subtracted, plt_name, plot_path, color, xlim = (600, 4000), ylim = (-0.5, 1.7)):
    
    x_lims = xlim
    y_lims = ylim
    zoom = True
    counter = 0
    
    # Here new directories are created for zoomed in plots that get saved.
    zoom_dir = os.path.join(os.path.dirname(plot_path), "Zoomed")
    os.makedirs(zoom_dir, exist_ok=True)
    
    # We ask the user if they's like to set custom axis limits for their plots that they've just seen.
    while zoom:
        user_input = input("Do you wish to zoom into a region? (y/n): ").lower()

        if user_input in ["y", "yes"]:
            # x-axis
            which_region_x = input("Do you want to zoom in on the x-axis? (y/n): ").lower()
            if which_region_x in ["y", "yes"]:
                try:
                    x_bounds = input("Enter lower and upper x bounds separated by ', ': ")
                    x_lims = tuple(map(float, x_bounds.split(',')))
                except:
                    print(f"Invalid input. Using default x limits {xlim}.")
                    x_lims = xlim
            else:
                x_lims = xlim

            # y-axis
            which_region_y = input("Do you want to zoom in on the y-axis? (y/n): ").lower()
            if which_region_y in ["y", "yes"]:
                try:
                    y_bounds = input("Enter lower and upper y bounds separated by ', ': ")
                    y_lims = tuple(map(float, y_bounds.split(',')))
                except:
                    print(f"Invalid input. Using default y limits {ylim}.")
                    y_lims = ylim
            else:
                y_lims = ylim
        else:
            x_lims = xlim
            y_lims = ylim

        # This is where all the plotting parameters are kept.
        plt.figure()
        plt.plot(df_subtracted['Wavenumbercm-1'], df_subtracted['Intensity'], color=color)
        plt.title(f"{plt_name}")
        plt.xlabel("Wavenumber (cm⁻¹)")
        plt.ylabel("Δ Intensity (Sample - Solvent)")
        plt.xlim(*x_lims)
        plt.ylim(*y_lims)
        plt.tight_layout()
        plt.show()
        plt.close()

        # Here we ask the user if they want to zoom in again
        user_input = input("Do you want to zoom in further? (y/n): ").lower()

        #If they don't we save the last shown plot
        if user_input not in ["y", "yes"]:
            save_input = input("Save the last seen plot? (y/n): ").lower()
            
            #If they do we let them zoom in again and show them that plot, then ask them if they'd like to save it
            # This continues until the user is happy with the zoomed in version of their plot.
            if save_input in ["y", "yes"]:
                zoom_filename = f"{plt_name}_zoom_{counter}.jpg"
                zoom_path = os.path.join(zoom_dir, zoom_filename)
                plt.figure()
                plt.plot(df_subtracted['Wavenumbercm-1'], df_subtracted['Intensity'], color=color)
                plt.title(plt_name)
                plt.xlabel("Wavenumber (cm⁻¹)")
                plt.ylabel("Δ Intensity (Sample - Solvent)")
                plt.xlim(*x_lims)
                plt.ylim(*y_lims)
                plt.tight_layout()
                plt.savefig(zoom_path)
                print(f"Saved to {zoom_path}")
                plt.close()
            zoom = False

        counter += 1