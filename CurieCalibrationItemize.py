import os
import numpy as np
from scipy.optimize import curve_fit

# Input file path
input_file = './TableValues.txt'

# Output results file path
output_results_file = './Results/QBest_Values.txt'

# Target Q value
target_Q = 0.8

# Check if input file exists
if not os.path.exists(input_file):
    print(f"Input file {input_file} does not exist.")
    exit()

# Load data from the file
try:
    data = np.loadtxt(input_file, skiprows=1)  # Skip header row
    channel, N_E, W, P, G_ZW, value, energy_mev = data.T  # Transpose to extract columns
except Exception as e:
    print(f"Error loading data from {input_file}: {e}")
    exit()

# Define linear function for fitting
def linear_func(x, a, b):
    return a * x + b

# Configuration for each plot
values = {
    'Kurie': {'y_data': value, 'min_range': (0.1, 0.3), 'max_range': (0.4, 0.8), 'min_step': 0.01, 'max_step': 0.01},
    'N(E)': {'y_data': np.sqrt(N_E), 'min_range': (0.2, 0.4), 'max_range': (0.5, 0.7), 'min_step': 0.01, 'max_step': 0.01}
}

# Best combinations for each fit type
best_combinations = {'Kurie': None, 'N(E)': None}
best_errors = {'Kurie': float('inf'), 'N(E)': float('inf')}
best_slope_errors = {'Kurie': float('inf'), 'N(E)': float('inf')}

# List to store the results
q_values = []

# Perform fits for each energy range
for key, config in values.items():
    # Iterate over the min and max values with the specified step sizes
    for min_val in np.arange(config['min_range'][0], config['min_range'][1] + config['min_step'], config['min_step']):
        for max_val in np.arange(config['max_range'][0], config['max_range'][1] + config['max_step'], config['max_step']):

            # Filter data within the current energy range
            mask = (energy_mev >= min_val) & (energy_mev <= max_val)
            x_fit = energy_mev[mask]
            y_fit = config['y_data'][mask]

            # Perform linear fit
            popt, pcov = curve_fit(linear_func, x_fit, y_fit)
            slope, intercept = popt
            slope_err, intercept_err = np.sqrt(np.diag(pcov))

            # Calculate intersection with the x-axis (Q value)
            Q_value = -intercept / slope

            # Calculate the error: the absolute difference from the target Q value (0.8 MeV)
            Q_error = abs(Q_value - target_Q)

            # Compare the errors and find the best combination
            if Q_error < best_errors[key] or (Q_error == best_errors[key] and slope_err < best_slope_errors[key]):
                best_errors[key] = Q_error
                best_slope_errors[key] = slope_err
                best_combinations[key] = (min_val, max_val, Q_value, slope_err)

            # Append to the results for later saving
            q_values.append((min_val, max_val, key, Q_value))

# Print the best combinations for Kurie and N(E)
for fit_type in ['Kurie', 'N(E)']:
    if best_combinations[fit_type]:
        min_val, max_val, Q_value, slope_err = best_combinations[fit_type]
        print(f"\nBest combination for {fit_type}:")
        print(f"Min Energy: {min_val:.2f} MeV")
        print(f"Max Energy: {max_val:.2f} MeV")
        print(f"Q Value: {Q_value:.4f} MeV")
        print(f"Slope Error: {slope_err:.4f}")
        print(f"Error from target Q: {best_errors[fit_type]:.4f} MeV")
    else:
        print(f"\nNo valid combination found for {fit_type}.")

# Save the results to a text file
with open(output_results_file, 'w') as f:
    f.write("Min Energy (MeV)\tMax Energy (MeV)\tFit Type\n")
    for fit_type in ['Kurie', 'N(E)']:
        min_val, max_val, Q_value, slope_err = best_combinations[fit_type]
        f.write(f"{min_val:.2f}\t{max_val:.2f}\t{fit_type}\t{Q_value:.4f}\n")