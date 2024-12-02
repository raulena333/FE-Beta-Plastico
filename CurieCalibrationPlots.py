import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from scipy.optimize import curve_fit

# Update plot appearance
params = {
    'xtick.labelsize': 17,
    'ytick.labelsize': 17,
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params)

# Input file path
input_file = './TableValues.txt'
input_configuration = './Results/QBest_values.txt'

# Output plot path
output_plot = './Results/LinearFits_QValue.pdf'
output_results_file = './Results/Q_ValuesErrors.txt' 

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

# Read the best combinations from the file
try:
    best_combinations_data = np.loadtxt(input_configuration, dtype=str, delimiter='\t', skiprows=1)
    best_combinations = []
    for row in best_combinations_data:
        min_val, max_val, fit_type, q_value = row
        best_combinations.append((float(min_val), float(max_val), fit_type, float(q_value)))
except Exception as e:
    print(f"Error reading best combinations from {input_configuration}: {e}")
    exit()

# Define linear function for fitting
def linear_func(x, a, b):
    return a * x + b

# Define error propagation
def calculate_error(slope, slope_error, inter, inter_error):
    return np.sqrt((- 1 / slope * inter_error)**2 + (inter / slope**2 * slope_error)**2)

# Configuration for each plot using best combinations from the file
values = {
    'Kurie': {'y_data': value, 'min': best_combinations[0][0], 'max': best_combinations[0][1], 'label': "Kurie Data", 'color': 'blue', 'marker': 'o'},
    'N(E)': {'y_data': np.sqrt(N_E), 'min': best_combinations[1][0], 'max': best_combinations[1][1], 'label': r"$\sqrt{N(E)}$ Data", 'color': 'green', 'marker': 'v'}
}

# Prepare the plot
fig, ax1 = plt.subplots(figsize=(11.5, 6.85))

# Create the second y-axis
ax2 = ax1.twinx()

# Lists to store legend entries for both axes
handles, labels = [], []

# Perform fits and plot results
intersections = {}

for key, config in values.items():
    # Filter data within the range
    mask = (energy_mev >= config['min']) & (energy_mev <= config['max'])
    x_fit = energy_mev[mask]
    y_fit = config['y_data'][mask]

    # Perform linear fit
    popt, pcov = curve_fit(linear_func, x_fit, y_fit)
    slope, intercept = popt
    slope_err, intercept_err = np.sqrt(np.diag(pcov))

    # Calculate intersection with the x-axis (Q value)
    Q_value = -intercept / slope
    Q_error = calculate_error(slope, slope_err, intercept, intercept_err)

    intersections[key] = (Q_value, Q_error)

    # Generate fitted line
    x_range = np.linspace(x_fit.min(), x_fit.max(), 500)
    y_range = linear_func(x_range, slope, intercept)
    
    x_range_0 = np.linspace(0.9, x_fit.max(), 1000)
    y_range_0 = linear_func(x_range_0, slope, intercept)

    # Plot the data and fit
    if key == 'Kurie':
        ax1.plot(x_range, y_range, color=config['color'])
        ax1.plot(x_range_0, y_range_0, color=config['color'], linestyle = '--')
        ax1.scatter(x_fit, y_fit, color=config['color'], marker=config['marker'], s=10, label = config['label'])
    elif key == 'N(E)':
        ax2.plot(x_range, y_range, color=config['color'])
        ax2.plot(x_range_0, y_range_0, color=config['color'], linestyle = '--')
        ax2.scatter(x_fit, y_fit, color=config['color'], marker=config['marker'], s=10, label = config['label'])  

# Combine the handles and labels for the single legend
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Combine both sets of handles and labels
handles.extend(handles2)
labels.extend(labels2)

# Add labels, legends, and grid
ax1.set_xlabel("Energia (MeV)")
ax2.set_ylabel(r"$\frac{1}{W}\sqrt{\frac{N(E)}{G(Z,W)}}$", color='blue')
ax1.set_ylabel(r"$\sqrt{N(E)}$", color='green')

# Add a single legend for both axes
ax1.legend(handles, labels)

# Add horizontal line at y=0 to show where the fits intersect with the x-axis
ax1.hlines(0, 0.2, 0.9, linestyles="-", color="red")

plt.savefig(output_plot)
plt.close()

# Save the results in a text file
with open(output_results_file, 'w') as f:
    f.write("Key\tQ Value (MeV)\tQ Error (MeV)\n")
    for key, (q_value, q_error) in intersections.items():
        f.write(f"{key}\t{q_value:.4f}\t{q_error:.4f}\n")

# Print confirmation
print(f"Plot saved: {output_plot}")
print(f"Results saved to: {output_results_file}")