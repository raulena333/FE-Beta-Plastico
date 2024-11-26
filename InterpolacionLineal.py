import numpy as np
import scipy.interpolate as sc
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params) 

isotope_name = "Talio204"   #Isotope name
conversion_energy = 511     #Units keV/c^2
filename = "TableValues.txt"

# Load data for interpolation and for isotope
data_interpolation = np.loadtxt("ValoresInterpolacion.txt", skiprows = 1)
p_value = data_interpolation[:, 0]
G_value = data_interpolation[:, 1]

data_Talio = np.loadtxt('./Data/Data_' + isotope_name+ '_WithErrors_energy.txt', skiprows=1)
channel = data_Talio[:, 0]
counts = data_Talio[:, 1]
energy = data_Talio[:, 3]

W = energy/conversion_energy +  1
P = (W**2 - 1)**(1/2)

# Crear la función de interpolación cúbica
interpolacion_cubica = sc.interp1d(p_value, G_value, kind='cubic')
G = interpolacion_cubica(P)
value = 1 / W * (counts / G)**(1/2)

# Open the file in write mode
with open(filename, "w") as file:
    # Write the header line
    file.write("ChannelNumber\tN(E)\tW\tP\tG(Z,W)\tValue\tEnergy(MeV)\n")
    for i in range(len(value)):
        file.write(f"{channel[i]}\t{counts[i]}\t{W[i]}\t{P[i]}\t{G[i]}\t{value[i]}\t{energy[i] / 1000}\n")

# Load table
data_table = np.loadtxt(filename, skiprows = 1)
Energy = data_table[:, 6]
Value = data_table[:, 5]

plt.figure(figsize=(10, 6))
plt.plot(Energy, Value, color = "black")
plt.plot(Energy, np.sqrt(counts), color = "red" )
plt.xlabel("E (MeV)")
plt.ylabel("Values")
plt.show()
