import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os

# Set parameters for plot appearance
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params)

output_dir = './Resultados'
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

# Input file path
input_file = './TableValues.txt'
output_plot = './Results/BothKurieN(E)Plot.pdf'

# Load data from the file
try:
    data = np.loadtxt(input_file, skiprows=1)  # Skip the header row
    channel, N_E, W, P, G_ZW, value, energy_mev = data.T  # Transpose to extract columns
except Exception as e:
    print(f"Error loading data from {input_file}: {e}")
    exit()

# Define the datasets for Kurie and N(E)
values = {
    'Kurie': {'y_data': value, 'label': "Kurie Data", 'color': 'blue'},
    'N(E)': {'y_data': np.sqrt(N_E), 'label': r"$\sqrt{N(E)}$ Data", 'color': 'green'}
}

# Prepare the plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Create a second y-axis for the second dataset
ax2 = ax1.twinx()

# Initialize lists for the handles and labels of the legend
handles, labels = [], []

# Example linear adjustments for y_range (replace with your actual calculations)
y_range_kurie = values['Kurie']['y_data']  # Use Kurie data as an example
y_range_n_e = values['N(E)']['y_data']  # Use N(E) data as an example

# Plot the data and the adjustments
ax1.plot(energy_mev, y_range_kurie, color=values['Kurie']['color'], label=values['Kurie']['label'])
ax1.plot(energy_mev, y_range_kurie, color=values['Kurie']['color'], linestyle='--')  # Example dashed line for fit
ax2.plot(energy_mev, y_range_n_e, color=values['N(E)']['color'], label=values['N(E)']['label'])
ax2.plot(energy_mev, y_range_n_e, color=values['N(E)']['color'], linestyle='--')  # Example dashed line for fit

# Add legends for both plots
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Combine the handles and labels from both axes
handles.extend(handles2)
labels.extend(labels2)

# Add labels, legends, and grid
ax1.set_xlabel("Energy (MeV)", fontsize=18)
ax2.set_ylabel(r"$\frac{1}{W}\sqrt{\frac{N(E)}{G(Z,W)}}$", fontsize=18, color='blue')
ax1.set_ylabel(r"$\sqrt{N(E)}$", fontsize=18, color='green')

# Add a single legend for both axes
ax1.legend(handles, labels, loc='best')

# Adjust the layout and save the image
fig.tight_layout()  # Ensure everything fits without overlap
plt.savefig(output_plot)
plt.close()

print(f"Plot saved: {output_plot}")

