import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os

params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params) 

# Input file path
input_file = './Tablevalues.txt'

# Output plot paths
output_plot1 = './Results/Kurie_Energy.pdf'
output_plot2 = './Results/SqrtN(E)_Energy.pdf'

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

# Calculate sqrt(N(E))
sqrt_N_E = np.sqrt(N_E)

# Plot 1: Value vs. Energy (MeV)
plt.figure(figsize=(10, 6))
plt.plot(energy_mev, value, linestyle='-', color='black')
plt.xlabel("Energia (MeV)")
plt.ylabel(r"$\frac{1}{W}\sqrt{\frac{N(E)}{G(Z,W)}}$")
plt.xlim(0,1.6)
plt.savefig(output_plot1)
plt.close()
print(f"Plot saved: {output_plot1}")

# Plot 2: sqrt(N(E)) vs. Energy (MeV)
plt.figure(figsize=(10, 6))
plt.plot(energy_mev, sqrt_N_E, linestyle='-', color='black')
plt.xlabel("Energia (MeV)")
plt.ylabel(r"$\sqrt{N(E)}$")
plt.xlim(0,1.6)
plt.savefig(output_plot2)
plt.close()
print(f"Plot saved: {output_plot2}")
