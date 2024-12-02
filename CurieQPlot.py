import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import scipy.interpolate as sc
import os

# Plot appearance settings
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params) 

# Paths
input_file = './Tablevalues.txt'
q_values_file = "./Results/Q_ValuesErrors.txt"
output_file = "./Results/QCuriePlot.png"
input_fermi = "./Fermi_204Tl.txt"

# Read Q values
try:
    data_q = np.loadtxt(q_values_file, dtype=str, delimiter='\t', skiprows=1)
    Q = float(data_q[0, 1])  
    Q_error = float(data_q[0, 2])
except Exception as e:
    print(f"Error reading Q values file: {e}")
    exit()

# Check if input file exists
if not os.path.exists(input_file):
    print(f"File {input_file} does not exist.")
    exit()

# Load main data
try:
    data = np.loadtxt(input_file, skiprows=1)
    channel, N_E, W, P, G_ZW, value, energy_mev = data.T  
except Exception as e:
    print(f"Error loading data from {input_file}: {e}")
    exit()   

# Load Fermi function data
try:
    data_fermi = np.loadtxt(input_fermi, skiprows=2)
    T = data_fermi[:, 0]
    F_Z_P = data_fermi[:, 1] 
except Exception as e:
    print(f"Error loading Fermi data from {input_fermi}: {e}")
    exit()

# Interpolation for Fermi function
fermi_interpolation = sc.interp1d(T, F_Z_P, kind='cubic', bounds_error=False, fill_value="extrapolate")

# Calculate N(p) = N(E) * (p * c^2) 
N_p = N_E * P / energy_mev # MeV to keV
F_Z_T = fermi_interpolation(energy_mev)
left = np.sqrt(N_p / (P**2 * F_Z_T))

right = (Q - energy_mev)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Left axis (for right-hand side, proportionality factor)
ax1.plot(energy_mev, right, label=r"$\sqrt{\frac{N(p)}{p^2 F(Z, T)}}$", color='blue', linestyle='--', linewidth=1.5)
ax1.set_xlabel(r"$T$ (MeV)", fontsize=18)
ax1.set_ylabel(r"$\sqrt{\frac{N(p)}{p^2 F(Z, T)}}$ $(MeV\cdot c)^{-1}$", fontsize=18, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_yscale("log")  # Set logarithmic scale for the left y-axis

# Right axis (for left-hand side, theoretical line)
ax2 = ax1.twinx()
ax2.plot(energy_mev, left, label=r"$(Q - T)$", color='green', linestyle='--', linewidth=1.5)
ax2.set_ylabel(r"$(Q - T)$ (MeV)", fontsize=18, color='green')
ax2.tick_params(axis='y', labelcolor='green')
ax2.set_yscale("log")  # Set logarithmic scale for the right y-axis

# Combine legends from both axes
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
handles = handles1 + handles2
labels = labels1 + labels2
ax1.legend(handles, labels)

# Add zoomed inset
zoom_ax = inset_axes(ax1, width="40%", height="30%", loc="center right")  # Position inset
zoom_range = (0.1, 0.5)  # Define zoom range on x-axis
zoom_mask = (energy_mev >= zoom_range[0]) & (energy_mev <= zoom_range[1])

# Plot the zoomed region
zoom_ax.plot(energy_mev[zoom_mask], right[zoom_mask], color='blue', linestyle='--', linewidth=1.5)
zoom_ax.plot(energy_mev[zoom_mask], left[zoom_mask], color='green', linestyle='--', linewidth=1.5)
zoom_ax.set_title("", fontsize=10)
zoom_ax.set_yscale("log")
zoom_ax.grid()

# Highlight the zoomed area in the main plot
ax1.axvspan(zoom_range[0], zoom_range[1], color="lightgray", alpha=0.2, label="Zoomed Region")

# Adjust layout and save
fig.tight_layout()
plt.savefig(output_file)
plt.show()

