# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:39:33 2025

@author: marigl
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors


# Adds a trendline with its equation and R² shown on the plot to the individually plotted peaks over time
def add_trendline_single(x_vals, y_vals, color, alpha=0.6, linestyle="--"):

    # Fits a straight line through the x and y values
    z = np.polyfit(x_vals, y_vals, 1)
    p = np.poly1d(z)
    y_pred = p(x_vals)

    # Calculates R² value
    residuals = y_vals - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_vals - np.mean(y_vals)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # Plots the trendline
    plt.plot(x_vals, y_pred, linestyle=linestyle, color=color, alpha=alpha)

    # Calculates the midpoint for label positioning
    x_mid = (x_vals.iloc[0] + x_vals.iloc[-1]) / 2
    y_mid = p(x_mid)

    # Generates the pale version of line color for the line eqn box
    base_rgb = np.array(mcolors.to_rgb(color))
    pale_rgb = base_rgb + (1.0 - base_rgb) * 0.6
    pale_color = mcolors.to_hex(pale_rgb)

    # Prepares a clean vesion of the eqn text
    slope = z[0]
    intercept = z[1]
    sign = "+" if intercept >= 0 else "−"
    eqn_text = f"$y = {slope:.3f}x {sign} {abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$"

    # Creates the line annotation at the midpoint of the line, slightly above and offset to the LHS
    plt.annotate(
        eqn_text,
        xy=(x_mid, y_mid),
        xytext=(-5, 45),  # offset in points
        textcoords="offset points",
        ha="center",
        fontsize=9,
        bbox=dict(
            boxstyle="round,pad=0.4",
            fc=pale_color,
            ec=color,
            lw=1.2,
            alpha=0.9,
        ),
    )


# -------------------------------------------------------------------------------------------------------


# Plots individual peak intensity vs time from the csvs
def plot_intensity_vs_time(folder_path, color_list, data_proc_plot_dir):

    # This enables custon colour setting for each file
    # You can set your own colour scheme by altering the colours.py file :)
    colour_index = 0

    for file in os.listdir(folder_path):
        if file.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            try:
                df = pd.read_csv(file_path)

                # Skips files that don’t have enough data columns
                # In theory shouldn't happen as previous scripts would've flagged that error
                if df.shape[1] < 4:
                    print(f"Skipping {file}: not enough columns.")
                    continue

                # Extracts time and intensity values but miss out
                # the first row which is usually the value extracted from the solvent run
                timestamps_raw = df.iloc[1:, 2]
                intensities = df.iloc[1:, 1]

                # Converts timestamps to elapsed minutes
                time_deltas = pd.to_timedelta(timestamps_raw)
                elapsed_minutes = (
                    time_deltas - time_deltas.min()
                ).dt.total_seconds() / 60

                # This extracts the wavenumber from the file name later used for the legend
                try:
                    peak_pos = round(float(os.path.splitext(file)[0]))
                except ValueError:
                    peak_pos = os.path.splitext(file)[0]

                color = color_list[colour_index % len(color_list)]
                plt_name = f"Peak Intensity at {peak_pos} cm⁻¹ over Time"

                plt.figure()
                plt.scatter(elapsed_minutes, intensities, color=color)
                add_trendline_single(elapsed_minutes, intensities, color)
                plt.xlabel("Time Elapsed (min)")
                plt.ylabel("Intensity")
                plt.title(plt_name)
                plt.tight_layout()
                plt.xticks(rotation=45)

                plot_path = os.path.join(data_proc_plot_dir, f"{plt_name}.jpg")
                plt.savefig(plot_path)
                # plt.show()

                colour_index += 1

            # This prevents a cheeky wee crash if one of the plots is having a crashout
            except Exception as e:
                print(f"Error processing {file}: {e}")


# ---------------------------------------------------------------------------------------------------------


# Adds trendline to a plot that includes all of the peaks that were extracted
def add_trendline_multi(x_vals, y_vals, color, alpha=0.6, linestyle="--"):

    # Fits a straight line through the x and y values
    z = np.polyfit(x_vals, y_vals, 1)
    p = np.poly1d(z)
    y_pred = p(x_vals)

    # Calculates R²
    residuals = y_vals - y_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_vals - np.mean(y_vals)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    # We format the label here
    slope = z[0]
    intercept = z[1]
    sign = "+" if intercept >= 0 else "−"
    label = f"$y = {slope:.3f}x {sign} {abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$"

    # Plot and return the trendline with label
    (line,) = plt.plot(
        x_vals,
        y_pred,
        linestyle=linestyle,
        color=color,
        alpha=alpha,
        label=label,
    )
    return line


# -----------------------------------------------------------------------------------------------------------


# This has the same logic as the above funciton plot_intensity_vs_time() but uses a different colour index
def plot_all_peaks_combined(
    folder_path, color_list, data_proc_plot_dir, title
):
    colour_index = 0
    plt.figure(figsize=(12, 6))

    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            try:
                df = pd.read_csv(file_path)

                if df.shape[1] < 4:
                    print(f"Skipping {file}: not enough columns.")
                    continue

                intensities = df.iloc[1:, 1]
                timestamps_raw = df.iloc[1:, 2]
                time_deltas = pd.to_timedelta(timestamps_raw)
                elapsed_minutes = (
                    time_deltas - time_deltas.min()
                ).dt.total_seconds() / 60

                try:
                    peak_label = (
                        f"{round(float(os.path.splitext(file)[0]))} cm⁻¹"
                    )
                except ValueError:
                    peak_label = os.path.splitext(file)[0]

                color = color_list[colour_index % len(color_list)]
                plt.scatter(
                    elapsed_minutes, intensities, label=peak_label, color=color
                )
                add_trendline_multi(elapsed_minutes, intensities, color)
                colour_index += 1

            # This prevents a cheeky wee crash if one of the plots is having a crashout
            except Exception as e:
                print(f"Error processing {file}: {e}")

    plt.xlabel("Time Elapsed (min)")
    plt.ylabel("Intensity")
    plt.title(title)

    # Move legend to the right outside the plot and position centrally relative to the graphing box
    plt.legend(
        loc="center left",
        bbox_to_anchor=(1.01, 0.5),
        title="Wavenumber",
        frameon=True,
        borderaxespad=0.5,
    )

    # Adjusts layout to make room on the right
    plt.tight_layout(
        rect=[0, 0, 0.75, 1]
    )  # 0.75 = reserves 25% of width for legend

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45)

    # Save and show the created plot
    plot_path = os.path.join(data_proc_plot_dir, f"{title}.jpg")
    plt.savefig(plot_path, bbox_inches="tight")
    # plt.show()
