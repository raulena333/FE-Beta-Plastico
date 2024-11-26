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

# Linear function definition
def linear_func(x, m, c):
    return m * x + c

# Input and output file paths
input_file = './Results/Cesio137_fitted_parameters.txt'
output_plot = './Results/energy_calibration.pdf'

# Function to read the xc, its error, and energy from the file
def read_parameters(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    xc = None
    xc_err = None
    energy = None

    # Parse lines to extract values
    for line in lines:
        if "xc (peak center)" in line:
            xc = float(line.split(':')[1].split('+-')[0].strip())
            xc_err = float(line.split('+-')[1].split()[0].strip())
        if "Gaussian peak energy" in line:
            energy = float(line.split(':')[1].split()[0])
    
    # Check for missing values
    if xc is None or xc_err is None or energy is None:
        raise ValueError("Failed to extract xc, xc_err, or energy from the file.")
    
    return xc, xc_err, energy

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} does not exist.")
else:
    try:
        # Extract xc, its error, and energy
        xc, xc_error, energy = read_parameters(input_file)

        # Include the origin (0, 0) in the calibration
        channels = np.array([0, xc])  # Channels: [0, xc]
        energies = np.array([0, energy])  # Energies: [0, energy]
        errors = np.array([0, xc_error])  # Errors: [0, xc_error]

        # Perform linear fit
        popt, pcov = curve_fit(linear_func, channels, energies)
        slope, intercept = popt
        slope_err, intercept_err = np.sqrt(np.diag(pcov))

        # Generate fitted line for plotting
        channel_range = np.linspace(0, xc * 1.5, 500)  # Generate a range of channels
        fitted_energies = linear_func(channel_range, slope, intercept)

        # Plot the calibration
        plt.figure(figsize=(10, 6))
        plt.errorbar(channels, energies, yerr=errors, fmt='.', markersize=6, color="#074936", 
                     elinewidth=1.5, ecolor="#000000", label="Data", capsize=3)
        plt.plot(channel_range, fitted_energies, color="#AD3628", linewidth=2, linestyle="solid", label="Ajuste Lineal")

        # Labels and legend
        plt.xlabel("Canal")
        plt.ylabel("Energia (keV)")
        plt.legend()

        # Save the plot
        plt.savefig(output_plot)
        plt.close()
        print(f"Energy calibration plot saved as {output_plot}")

        # Save the fitted slope and intercept with errors to a text file
        param_file = './Results/Slope_fitted_parameters.txt'
        with open(param_file, 'w') as f:
            f.write(f"Fitted parameters for slope:\n")
            f.write("------------------------------------------------\n")
            f.write(f"Slope (keV/channel): {slope:.4f}\n")
            f.write("------------------------------------------------\n")
        print(f"Fitted slope parameters saved to {param_file}")

    except ValueError as e:
        print(f"Error while processing the file: {e}")
