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
nucleus_name = "Talio204"

# Output directory
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Function to plot channel spectrum
def plot_spectrum(name, energy_number, net_counts, annotations):
    plt.figure(figsize=(10, 6))
    plt.plot(energy_number, net_counts, label=name, color="black", linewidth=2)
    
    # Plot the fitted curve only if it exists
    # if fitted_curve is not None and energy_in_region is not None:
    #    plt.plot(energy_in_region, fitted_curve, label="Fit", color="red", linestyle="--", linewidth=2)
    
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
    plt.show()
    plt.close()

# Annotations: (energy_value, "label")
annotations = [   
    (350, r"$\beta-$"),
]

# Process Spectrum for Bario133
file_path = f'./Data/Data_{nucleus_name}_WithErrors_energy.txt'

# Load data for the nucleus
data_nucleus = np.loadtxt(file_path, skiprows=1)
energy = data_nucleus[:, 3]
counts = data_nucleus[:, 1]

plot_spectrum(nucleus_name, energy, counts, annotations)

energy_ranges = {
    'beta-': {'Energy': 350, 'min': 54, 'max': 690}, 
}

# Total counts
total_counts = np.sum(counts)

# List to store the results for each component
results = []  

# Count the number of counts within each energy range and calculate the intensity
for component, values in energy_ranges.items():
    # Find the minimum and maximum energy for the current component
    min_energy = values['min']
    max_energy = values['max']
    
    # Mask to find the indices of energies within the range of the current component
    mask = (energy >= min_energy) & (energy <= max_energy)
    
    # Count the number of counts within the specified energy range
    counts_in_range = np.sum(counts[mask])
    
    # Calculate the intensity: the ratio of counts in the range to the total counts
    intensity = counts_in_range / total_counts
    
    # Store the result: component name, energy value, and calculated intensity
    results.append([component, values['Energy'], intensity])

# Save the results to a text file
output_file = os.path.join(output_dir, f"{nucleus_name}_IntensityResults.txt")
header = "Component\tEnergy (keV)\tIntensity"  # Header for the file

# Open the file for writing
with open(output_file, 'w') as f:
    f.write(header + "\n")  # Write the header line
    for result in results:
        f.write(f"{result[0]}\t{result[1]}\t{result[2]:.6f}\n")  # Write each result

# Print the path of the saved results file
print(f"Results saved to {output_file}")



