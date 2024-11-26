import numpy as np
import os

# Names of nucleus isotopes
nucleus_names = {"Cesio137", "Europio152", "Bario133", "Talio204"}

# Load background data
data_background = np.loadtxt('./Data/Datos_Fondo_(canales).txt', skiprows=1)
channel_number = data_background[:, 0]
counts_background = data_background[:, 1]

# Calculate errors as the square root of counts (Poisson error)
errors_background = np.sqrt(counts_background)

# Add errors as the third column to the background data
data_with_errors = np.column_stack((data_background, errors_background))

# Save the updated background data with errors to a new file
output_file = './Data/Data_Background_WithErrors_channel.txt'
np.savetxt(output_file, data_with_errors, header="Channel Number\tCounts\tError", fmt=['%.0f', '%.0f', '%.4f'], delimiter='\t')

# Process each nucleus
for name in nucleus_names:
    file_path = f'./Data/Datos_{name}_(canales).txt'
    
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Skipping {name}.")
        continue

    # Load data for the nucleus
    data_nucleus = np.loadtxt(file_path, skiprows=1)
    channel = data_nucleus[:, 0]
    nucleus_counts = data_nucleus[:, 1]

    # Calculate net counts (subtracting background counts)
    net_counts = np.maximum(nucleus_counts - counts_background, 0)

    # Calculate errors
    error_counts = np.sqrt(nucleus_counts)  # Error in nucleus counts (Poisson error)
    error = np.sqrt(error_counts**2 + errors_background**2)  # Combined error for net counts

    # Add errors as the third column to the nucleus data
    data_error = np.column_stack((channel, net_counts, error))

    # Save the updated nucleus data with errors to a new file
    output_file = f'./Data/Data_{name}_WithErrors_channel.txt'
    np.savetxt(output_file, data_error, header="Channel Number\tNet Counts\tError", fmt=['%.0f', '%.0f', '%.4f'], delimiter='\t')

    print(f"File for {name} with errors saved as {output_file}")


