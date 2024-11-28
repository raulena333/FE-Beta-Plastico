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
    'Cesio137': {'Energy': 630, 'min': 175, 'max': 230},
}

# Output directory for results and plots
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Define a Gaussian with background linear term for fitting
def gaussian(x, a, b, c, xc, s): 
    return a + b * x + c * np.exp(-(x - xc)**2 / (2 * s**2))

# Process each nucleus
for name, props in energy_beta.items():
    min_channel = props['min']
    max_channel = props['max']

    # Load data for the nucleus
    file_path = f'./Data/Data_{name}_WithErrors_channel.txt'
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping {name}.")
        continue

    data_nucleus = np.loadtxt(file_path, skiprows=1)
    channel = data_nucleus[:, 0]
    counts = data_nucleus[:, 1]
    error = data_nucleus[:, 2]

    # Select data within the region of interest (from min to max)
    region = (channel >= min_channel) & (channel <= max_channel)
    channels_in_region = channel[region]
    counts_in_region = counts[region]
    error_in_region = error[region]

    # Fit the model (Gaussian + Linear background) to the data
    initial_guess = [-1., -3., 3e3, 210, 5]
    try:
        popt, pcov = curve_fit(
            gaussian, 
            channels_in_region, 
            counts_in_region, 
            p0=initial_guess, 
            sigma=error_in_region
        )
        # Calculate parameter errors as the square root of the diagonal of the covariance matrix
        perr = np.sqrt(np.diag(pcov))
    except RuntimeError as e:
        print(f"Curve fitting failed for {name}: {e}. Skipping this nucleus.")
        continue

    # Extract fitted parameters and their errors
    a, b, c, xc, s = popt
    a_err, b_err, c_err, xc_err, s_err = perr

    # Generate the fitted curve
    fitted_curve = gaussian(channels_in_region, *popt)

    # Save the fitted parameters and errors to a text file
    param_file = f'./Results/{name}_fitted_parameters.txt'
    with open(param_file, 'w') as f:
        f.write(f"Fitted parameters for {name}:\n")
        f.write("------------------------------------------------\n")
        f.write(f"a (offset): {a:.4f} +- {a_err:.4f}\n")
        f.write(f"b (background slope): {b:.4f} +- {b_err:.4f}\n")
        f.write(f"c (peak height): {c:.4f} +- {c_err:.4f}\n")
        f.write(f"xc (peak center): {xc:.4f} +- {xc_err:.4f} channel\n")
        f.write(f"s (peak width): {s:.4f} +- {s_err:.4f} channel\n")
        f.write("------------------------------------------------\n")
        f.write(f"Gaussian peak energy: {props['Energy']} keV\n")
    print(f"Fitted parameters and errors for {name} saved to {param_file}")

    # Plot the spectrum with the fitted Gaussian and background
    plt.figure(figsize=(10, 6))
    plt.plot(channel, counts, label=f"{name} Data", color="black")
    plt.plot(channels_in_region, fitted_curve, label=f"{name} Fit", color="red", linestyle='--', linewidth = 2)
    plt.xlabel("Canal")
    plt.xlim(0,512)
    plt.ylabel("Numero de cuentas")
    plt.legend()

    # Apply log scale if specified
    if use_log_scale:
        plt.semilogy()
        suffix = '_FitLog.pdf'
    else:
        suffix = '_Fit.pdf'

    # Save the plot to the specified directory
    plot_file_path = os.path.join(output_dir, name + suffix)
    plt.savefig(plot_file_path)
    plt.close()
    print(f"Plot saved for {name} as {plot_file_path}")

# Calculate are of gaussian
def gaussian_area(c, c_error, s, s_error):
    area = c * np.sqrt(2 * np.pi) * s
    error = np.sqrt((np.sqrt(2 * np.pi) * s * c_error)**2 + (c * np.sqrt(2 * np.pi) * s_error)**2)
    return area, error

# Calculate counts under gaussian
area, error = gaussian_area(c, c_err, s, s_err)

# Calculate activity
time = 10 # min
activity = area / (time * 60)
error_activity = np.sqrt((1/(time * 60) * error)**2)

# Save the calculate are parameters and errors to a text file
param_file_1 = f'./Results/{name}_calculate_activity.txt'
with open(param_file_1, 'w') as f:
    f.write(f"Calculated area for {name}:\n")
    f.write("------------------------------------------------\n")
    f.write(f"Area: {area:.4f} +- {error:.4f}\n")
    f.write(f"Time: {time * 60} s \n")
    f.write(f"Activity {activity:.4f} +- {error_activity:.4f}\n")
    f.write("------------------------------------------------\n")
    f.write(f"Gaussian peak energy: {props['Energy']} keV\n")
print(f"Calculate area and errors for {name} saved to {param_file_1}")