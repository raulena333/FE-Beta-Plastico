import numpy as np
import datetime
import os

# Definition of variables
initial_activity = 0.25e-6  # Initial activity in Curie (Ci), 0.25 µCi = 0.25e-6 Ci
t_1_2 = 30.08  # Half-life of Cs-137 in years

# File paths
area_file = "./Results/Cesio137_calculate_activity.txt" 

# Check if the file exists
if not os.path.exists(area_file):
    print(f"File {area_file} does not exist.")
    exit()

# Read the file and extract activity and its error
try:
    with open(area_file, 'r') as f:
        lines = f.readlines()
        # Loop through the lines to find the activity
        for line in lines:
            if "Activity" in line:
                # Extract activity and error from the line
                parts = line.split()
                activity = float(parts[1])  # Activity value
                activity_error = float(parts[3])  # Error value
                break
except Exception as e:
    print(f"Error reading activity from file: {e}")
    exit()

# Decay constant lambda
lambda_0 = np.log(2) / t_1_2
print(f"Decay constant λ₀: {lambda_0:.6e} years⁻¹")

# Calculate the time elapsed between February 2018 and October 2023
start_date = datetime.datetime(2018, 2, 15)  # Start date (February 2018)
end_date = datetime.datetime(2024, 10, 15) 

# Calculate the number of years between the two dates
time_elapsed_years = (end_date - start_date).days / 365.25

# Current activity using the formula A(t) = A₀ * e^(-λ₀ * t)
current_activity = initial_activity * np.exp(-lambda_0 * time_elapsed_years)

# Convert the activity to Bq (1 Ci = 3.7e10 Bq)
current_activity_bq = current_activity * 3.7e10
print(f"Current activity (in Bq): {current_activity_bq:.2e} Bq")

# Correction for geometry and detector efficiency (assuming 50% detection and 9.4% efficiency)
detection_efficiency = 0.5  # Correction for detector geometry (50%)
intensity_efficiency = 0.094  # Measured intensity in the range between 624 keV and 661 keV (9.4%)

# Activity measured by the detector
measured_activity_bq = current_activity_bq * detection_efficiency * intensity_efficiency
print(f"Theorical activity measured by the detector (in Bq): {measured_activity_bq:.2e} Bq")

print(f"Experimental activity measured by detector: {activity:.2e} +- {activity_error:.4f} counts/s")

# Calculate efficiency
efficiency = activity / measured_activity_bq
efficiency_error = np.sqrt((1 / measured_activity_bq * activity_error)**2)

print(f"Detector efficiency: {efficiency:.3f} +- {efficiency_error:.3f}")
