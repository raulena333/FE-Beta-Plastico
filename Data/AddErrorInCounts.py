import numpy as np
import os

# Load background data
data_background = np.loadtxt('./Data/Datos_Fondo_(canales).txt', skiprows=1)
channel_number = data_background[:, 0]
counts_background = data_background[:, 1]

# Calculate errors as the square root of counts (Poisson error)
errors_background = np.sqrt(counts_background)

# Add errors as the third column
data_with_errors = np.column_stack((data_background, errors_background))

# Optionally, save the updated data to a new file
output_file = './Data/Data_Background_Errors_(channels).txt'
np.savetxt(output_file, data_with_errors, header="Channel Number\tCounts\tError", fmt='%.6f', delimiter='\t')

