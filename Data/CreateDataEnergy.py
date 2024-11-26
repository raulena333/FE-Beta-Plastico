import numpy as np
import os

# Names of nucleus isotopes
nucleus_names = {"Cesio137", "Europio152", "Bario133", "Talio204"}

# Path to the slope parameters file
slope_file = './Results/Slope_fitted_parameters.txt'

# Function to read the slope from the text file
def read_slope(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    slope = None
    for line in lines:
        if "Slope (keV/channel):" in line:
            slope = float(line.split(':')[1].strip())
            break
    
    if slope is None:
        raise ValueError("Failed to extract slope from the file.")
    
    return slope

try:
    slope = read_slope(slope_file)
except ValueError as e:
    print(f"Error reading slope: {e}")
    exit()

# Process each nucleus
for name in nucleus_names:
    file_path = f'./Data/Data_{name}_WithErrors_channel.txt'
    output_file = f'./Data/Data_{name}_WithErrors_energy.txt'
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping {name}.")
        continue

    # Load data for the nucleus
    data_nucleus = np.loadtxt(file_path, skiprows=1)
    channel = data_nucleus[:, 0]
    nucleus_counts = data_nucleus[:, 1]
    error = data_nucleus[:, 2]

    # Transform channels to energy
    energy = slope * channel

    # Combine original data with the energy column
    data_with_energy = np.column_stack((data_nucleus, energy))

    # Save the new data to a file
    header = "Channel\tCounts\tError\tEnergy (keV)"
    np.savetxt(output_file, data_with_energy, header=header, fmt=['%.0f', '%.0f', '%.4f', '%.3f'], delimiter='\t')
    print(f"File with energy column saved: {output_file}")
