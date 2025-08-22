# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 14:39:33 2025

@author: marigl
"""
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

max_colours = ['#f4ea94ff', '#59f7eaff', '#f47dabff']

max_colours_react = ['#B82300', '#BB4E00', '#BF9200', '#E2BD21', '#89B430', '#389C60']

max_colours_prod = ['#A30726', '#6C092F', '#75254B', '#2E2E50', '#27626C', '#008B82']

react_csv_dir = rf"{os.getcwd()}\Results\csvs\Reactants"
prod_csv_dir = rf"{os.getcwd()}\Results\csvs\Products"
data_proc_plot_dir = rf"{os.getcwd()}\Results\plots\Data_Processing_Plots" 

if os.path.exists(prod_csv_dir):
    pass
else:
    os.makedirs(prod_csv_dir)

if os.path.exists(react_csv_dir):
    pass
else:
    os.makedirs(react_csv_dir)
    
if os.path.exists(data_proc_plot_dir):
    pass
else:
    os.makedirs(data_proc_plot_dir)
    
def add_trendline_with_stats(x_vals, y_vals, color, label_offset=(10, -30)):
    """Plots a linear trendline and annotates equation and R²."""
    z = np.polyfit(x_vals, y_vals, 1)
    p = np.poly1d(z)
    trendline = p(x_vals)

    # Compute R²
    residuals = y_vals - trendline
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_vals - np.mean(y_vals))**2)
    r_squared = 1 - (ss_res / ss_tot)

    # Plot trendline
    plt.plot(x_vals, trendline, linestyle='--', color=color, alpha=0.6)

    # Equation text
    a, b = z
    eqn_text = f"y = {a:.3f}x + {b:.3f}\n$R^2$ = {r_squared:.3f}"

    # Annotate at middle x position
    xpos = x_vals.iloc[len(x_vals) // 2]
    ypos = trendline[len(trendline) // 2]
    plt.annotate(eqn_text, xy=(xpos, ypos), xycoords='data',
                 textcoords='offset points', xytext=label_offset,
                 fontsize=8, color=color,
                 bbox=dict(boxstyle="round,pad=0.3", alpha=0.15, facecolor=color))
    

def plot_intensity_vs_time(folder_path, color_list, group_title):
    colour_index = 0

    for file in os.listdir(folder_path):
        if file.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            try:
                df = pd.read_csv(file_path)

                if df.shape[1] < 4:
                    print(f"Skipping {file}: not enough columns.")
                    continue

                timestamps_raw = df.iloc[:, 2]
                intensities = df.iloc[:, 1]

                time_deltas = pd.to_timedelta(timestamps_raw)
                elapsed_minutes = (time_deltas - time_deltas.min()).dt.total_seconds() / 60

                try:
                    peak_pos = round(float(os.path.splitext(file)[0]))
                except ValueError:
                    peak_pos = os.path.splitext(file)[0]

                color = color_list[colour_index % len(color_list)]
                plt_name = f"Peak Intensity at {peak_pos} cm⁻¹ over Time"

                # Compute trendline and R²
                z = np.polyfit(elapsed_minutes, intensities, 1)
                p = np.poly1d(z)
                trendline = p(elapsed_minutes)

                residuals = intensities - trendline
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((intensities - np.mean(intensities))**2)
                r_squared = 1 - (ss_res / ss_tot)

                eqn_text = f"y = {z[0]:.3f}x + {z[1]:.3f}\n$R^2$ = {r_squared:.3f}"

                # Plot
                plt.figure()
                plt.scatter(elapsed_minutes, intensities, color=color, label="Data")
                plt.plot(elapsed_minutes, trendline, color=color, linestyle='--', label="Trendline")

                plt.xlabel("Time Elapsed (min)")
                plt.ylabel("Intensity")
                plt.title(plt_name)
                plt.xticks(rotation=45)
                plt.tight_layout()

                # Annotate trendline equation
                x_mid = elapsed_minutes.iloc[len(elapsed_minutes) // 2]
                y_mid = trendline[len(trendline) // 2]
                plt.annotate(eqn_text, xy=(x_mid, y_mid), xytext=(20, -40),
                             textcoords='offset points', fontsize=8,
                             bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.15))

                # Save plot
                plot_path = os.path.join(data_proc_plot_dir, f"{plt_name}.jpg")
                plt.savefig(plot_path)
                plt.show()

                colour_index += 1

            except Exception as e:
                print(f"Error processing {file}: {e}")


plot_intensity_vs_time(react_csv_dir, max_colours_react, "Reactants")
plot_intensity_vs_time(prod_csv_dir, max_colours_prod, "Products")

def plot_all_peaks_combined(folder_path, color_list, title):
    colour_index = 0
    plt.figure(figsize=(10, 6))

    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(".csv"):
            file_path = os.path.join(folder_path, file)

            try:
                df = pd.read_csv(file_path)

                if df.shape[1] < 4:
                    print(f"Skipping {file}: not enough columns.")
                    continue

                intensities = df.iloc[:, 1]
                timestamps_raw = df.iloc[:, 2]

                # Convert to elapsed minutes
                time_deltas = pd.to_timedelta(timestamps_raw)
                elapsed_minutes = (time_deltas - time_deltas.min()).dt.total_seconds() / 60

                try:
                    peak_label = f"{round(float(os.path.splitext(file)[0]))} cm⁻¹"
                except ValueError:
                    peak_label = os.path.splitext(file)[0]

                color = color_list[colour_index % len(color_list)]

                plt.scatter(elapsed_minutes, intensities, label=peak_label, color=color)
                
                offset_y = -30 - 40 * colour_index
                add_trendline_with_stats(elapsed_minutes, intensities, color, label_offset=(10, offset_y))
                
                colour_index += 1

            except Exception as e:
                print(f"Error processing {file}: {e}")
    
    plt_name = title

    plt.xlabel("Time Elapsed (min)")
    plt.ylabel("Intensity")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    
    plot_path = os.path.join(data_proc_plot_dir , f"{plt_name}.jpg")
    plt.savefig(plot_path)
    
    plt.show()
    
plot_all_peaks_combined(react_csv_dir, max_colours_react, title="Combined Peak Intensities - Reactants w Linear Trends")
plot_all_peaks_combined(prod_csv_dir, max_colours_prod, title="Combined Peak Intensities - Products w Linear Trends")