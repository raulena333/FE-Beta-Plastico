import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os
from scipy.optimize import curve_fit

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

# Names of nucleus isotopes and their excitation energies
energy_beta = {
    'Cesio137': {'Energy': 630, 'min': 180 , 'max': 240},
    #'Europio152': {'Energy': 38, 'max': , 'min': },
    #'Bario133': {'Energy': 38, 'max': , 'min': },
    #'Talio204': {'Energy': 38, 'max': , 'min': }
}

# Load background data
data_background = np.loadtxt('./Data/Datos_Fondo_(canales).txt', skiprows=1)
channel_number = data_background[:, 0]
counts_background = data_background[:, 1]

# Output directory
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Define a Gaussian with background linear term for fitting
def gaussian(x, a, b, c, xc, s): 
    return a + b * x + c * np.exp(-(x - xc)**2 / (2 * s**2))

# Function to plot channel spectrum with calibration
def plot_spectrum(name, channel_number, net_counts, max, min, fitted_curve=None):
    plt.figure(figsize=(10, 6))
    plt.plot(channel_number, net_counts, label=name, color="black")
    
    if fitted_curve is not None:
        plt.plot(channel_number, fitted_curve, label="Fitted Model", color="red", linestyle="--")
    
    plt.xlabel("Canal")
    plt.ylabel("Número de eventos")
    plt.xlim(min - 20, max + 20)
    plt.legend()

    if use_log_scale:
        plt.semilogy()
        suffix = '_ChannelSpectreLog.pdf'
    else:
        suffix = '_ChannelSpectre.pdf'
    
    plt.savefig(os.path.join(output_dir, name + suffix))
    plt.close()

# Process each nucleus
for name in energy_beta:
    min_channel = energy_beta[name]['min']
    max_channel = energy_beta[name]['max']

    # Load data for the nucleus
    file_path = f'./Data/Datos_{name}_(canales).txt'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping {name}.")
        continue

    data_nucleus = np.loadtxt(file_path, skiprows=1)
    nucleus_counts = data_nucleus[:, 1]

    # Calculate net counts
    net_counts = np.maximum(nucleus_counts - counts_background, 0)

    # Select data within the region of interest (from min to max)
    region = (channel_number >= min_channel) & (channel_number <= max_channel)
    channels_in_region = channel_number[region]
    net_counts_in_region = net_counts[region]

    # Fit the model (Gaussian + Linear background) to the data
    initial_guess = [min(net_counts_in_region), 0, max(net_counts_in_region), (min_channel + max_channel) / 2, 10]
    popt, _ = curve_fit(gaussian, channels_in_region, net_counts_in_region, p0=initial_guess)

    # Extract fitted parameters
    fitted_curve = gaussian(channels_in_region, *popt)

    # Plot the spectrum with the fitted Gaussian and background
    plot_spectrum(name, channel_number, net_counts, max_channel, min_channel, fitted_curve=fitted_curve)