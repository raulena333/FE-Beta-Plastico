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

use_log_scale = True  # True for log scale, False for linear scale

# Names of nucleus isotopes
nucleus_name = "Bario133"

# Output directory
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Function to plot channel spectrum
def plot_spectrum(name, energy_number, net_counts, annotations):
    plt.figure(figsize=(10, 6))
    plt.plot(energy_number, net_counts, label=name, color="black", linewidth=2)
    
    # # Plot the fitted curve only if it exists
    # if fitted_curve is not None and energy_in_region is not None:
    #     plt.plot(energy_in_region, fitted_curve, label="Fit", color="red", linestyle="--", linewidth=2)
    
    plt.xlabel("Energia (keV)")
    plt.ylabel("Número de cuentas")
    plt.xlim(0, 1600)
    plt.legend()
    
    # Add annotations
    for energy_value, label in annotations:
        # Find the index of the energy closest to the specified value
        idx = (np.abs(energy_number - energy_value)).argmin()
        
        # Get the actual count value at that energy
        y_value = net_counts[idx]
        
        # Annotate with arrow pointing to the specified positions
        plt.annotate(
            label,
            xy=(energy_value, y_value),  # Arrow ends here
            xytext=(energy_value + 50, y_value + 1000),  # Arrow starts here
            arrowprops=dict(
                arrowstyle="->",  # Arrow style
                color="blue",
                connectionstyle="arc3,rad=0.2"  # Slightly curved arrow
            ),
            fontsize=14,
            color='blue'
        )

    if use_log_scale:
        plt.semilogy()
        suffix = '_EnergySpectreBario133AnnotationsLog.pdf'
    else:
        suffix = '_EnergySpectreBario133Annotations.pdf'
    
    plt.savefig(os.path.join(output_dir, name + suffix))
    plt.close()

# Annotations: (energy_value, "label")
annotations = [
    (320, r"Conversion interna"),
    (30.85, "Rayos X"),    
    (44.5, "Conversión interna"),
]

# Process Spectrum for Bario133
file_path = f'./Data/Data_{nucleus_name}_WithErrors_energy.txt'

# Load data for the nucleus
data_nucleus = np.loadtxt(file_path, skiprows=1)
energy = data_nucleus[:, 3]
counts = data_nucleus[:, 1]

plot_spectrum(nucleus_name, energy, counts, annotations)
    
# # Fit function: Gaussian with linear background
# def gaussian(x, a, b, c, xc, s): 
#     return a + b * x + c * np.exp(-(x - xc)**2 / (2 * s**2))

# # Define energy ranges for fitting
# energy_beta_X = {
#     #'Rayos X': {'Energy': 30.85, 'min': 15, 'max': 55},
#     'Conversion Interna': {'Energy': 320, 'min': 280, 'max': 370},
# }

# param_file = f'./Results/{nucleus_name}_fitted_parameters.txt'

# # Open the file in append mode to avoid overwriting
# with open(param_file, 'w') as f:
#     f.write(f"Fitted parameters for {nucleus_name}:\n")
#     f.write("------------------------------------------------\n")

# # Process each energy range for fitting
# for name, props in energy_beta_X.items():
#     min_channel = props['min']
#     max_channel = props['max']

#     # Select data within the region of interest (from min to max)
#     region = (energy >= min_channel) & (energy <= max_channel)
#     energy_in_region = energy[region]
#     counts_in_region = counts[region]

#     # Fit the model (Gaussian + Linear background) to the data
#     initial_guess = [-10., -10., 3e3, 110, 15]
#     try:
#         popt, pcov = curve_fit(
#             gaussian, 
#             energy_in_region, 
#             counts_in_region, 
#             p0=initial_guess, 
#         )
#         # Calculate parameter errors as the square root of the diagonal of the covariance matrix
#         perr = np.sqrt(np.diag(pcov))
#     except RuntimeError as e:
#         print(f"Curve fitting failed for {name}: {e}. Skipping this energy.")
#         continue

#     # Extract fitted parameters and their errors
#     a, b, c, xc, s = popt
#     a_err, b_err, c_err, xc_err, s_err = perr

#     # Generate the fitted curve
#     fitted_curve = gaussian(energy_in_region, *popt)

#     # Save the fitted parameters and errors to a text file
#     with open(param_file, 'a') as f:
#         f.write(f"\n{name}:\n")
#         f.write(f"a (offset): {a:.4f} +- {a_err:.4f}\n")
#         f.write(f"b (background slope): {b:.4f} +- {b_err:.4f}\n")
#         f.write(f"c (peak height): {c:.4f} +- {c_err:.4f}\n")
#         f.write(f"xc (peak center): {xc:.4f} +- {xc_err:.4f} channel\n")
#         f.write(f"s (peak width): {s:.4f} +- {s_err:.4f} channel\n")
#         f.write("------------------------------------------------\n")
#         f.write(f"Gaussian peak energy: {props['Energy']} keV\n")
#     print(f"Fitted parameters and errors for {name} saved to {param_file}")

#     # Plot the spectrum with the fitted Gaussian and background in the same figure
#     plot_spectrum(nucleus_name, energy, counts, annotations, fitted_curve=fitted_curve, energy_in_region=energy_in_region)
#     print(f"Plot saved for {name} as {os.path.join(output_dir, nucleus_name + '_EnergySpectreBario133Annotations.pdf')}")
