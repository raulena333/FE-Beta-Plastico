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
nucleus_name = "Cesio137"

# Output directory
output_dir = './Results'
os.makedirs(output_dir, exist_ok=True)

# Function to plot channel spectrum
def plot_spectrum(name, energy_number, net_counts, annotations):
    plt.figure(figsize=(10, 6))
    plt.plot(energy_number, net_counts, label=name, color="black")
    plt.xlabel("Energia (keV)")
    plt.ylabel("Número de cuentas")
    plt.xlim(0, 1600)
    plt.legend()
    #plt.title(f"Spectre for {name}")
    
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
        suffix = '_EnergySpectreCsAnnotationsLog.pdf'
    else:
        suffix = '_EnergySpectreCsAnnotations.pdf'
    plt.savefig(os.path.join(output_dir, name + suffix))
    plt.close()

# Annotations: (energy_value, "label")
annotations = [
    (330, r"Radiación $\beta$"),
    (32, "Rayos X"),
    (630, "Conversión interna")
]
# Process Spectrum Cs137
file_path = f'./Data/Data_{nucleus_name}_WithErrors_energy.txt'

# Load data for the nucleus
data_nucleus = np.loadtxt(file_path, skiprows=1)
energy = data_nucleus[:, 3]
counts = data_nucleus[:, 1]
    
# Plot spectrum
plot_spectrum(nucleus_name, energy, counts, annotations)
