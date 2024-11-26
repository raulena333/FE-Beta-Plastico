import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os

# Configure parameters for plot appearance
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params)

use_log_scale = False  # True for log scale, False for linear scale

# Names of nucleus isotopes
nucleus_names = {"Cesio137", "Europio152", "Bario133", "Talio204"}

# Load background data
data_background = np.loadtxt('./Data/Datos_Fondo_(canales).txt', skiprows=1)
channel_number = data_background[:, 0]
counts_background = data_background[:, 1]

# Output directory
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Function to plot channel spectrum
def plot_spectrum(name, channel_number, net_counts):
    plt.figure(figsize=(10, 6))
    plt.plot(channel_number, net_counts, label=name, color="black")
    plt.xlabel("Canal")
    plt.ylabel("Número de eventos")
    plt.xlim(0, 520)
    plt.legend()
    #plt.title(f"Spectre for {name}")

    if use_log_scale:
        plt.semilogy()
        suffix = '_ChannelSpectreLog.pdf'
    else:
        suffix = '_ChannelSpectre.pdf'
    plt.savefig(os.path.join(output_dir, name + suffix))
    plt.close()

# Process each nucleus
for name in nucleus_names:
    file_path = f'./Data/Datos_{name}_(canales).txt'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping {name}.")
        continue

    # Load data for the nucleus
    data_nucleus = np.loadtxt(file_path, skiprows=1)
    nucleus_counts = data_nucleus[:, 1]

    # Calculate net counts
    net_counts = np.maximum(nucleus_counts - counts_background, 0)

    # Plot spectrum
    plot_spectrum(name, channel_number, net_counts)
