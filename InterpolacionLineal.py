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
filename = "Table.txt"

# Load data for interpolation and for isotope
data_interpolation = np.loadtxt("ValoresInterpolacion.txt", skiprows = 1)
p_value = data_interpolation[:, 0]
G_value = data_interpolation[:, 1]

data_Talio = np.loadtxt('./Datos/Datos ' + isotope_name+ ' (keV).txt', skiprows=1) 
energy = data_Talio[:, 0]
counts = data_Talio[:, 1]
data_background = np.loadtxt('./Datos/Datos de fondo (canales).txt', skiprows=1)
channel = data_background[:, 0]
counts_back = data_background[:, 1]

#Calculate values for W, P, (1/W)^{1/2}), E in units of m_ec^2. Divided by 511keV.
real_counts = np.maximum(counts - counts_back, 0)

W = energy/conversion_energy +  1
P = (W**2 - 1)**(1/2)

# Crear la función de interpolación cúbica
interpolacion_cubica = sc.interp1d(p_value, G_value, kind='cubic')
G = interpolacion_cubica(P)
value = 1 / W * (real_counts / G)**(1/2)

# Open the file in write mode
with open(filename, "w") as file:
    # Write the header line
    file.write("ChannelNumber\tN(E)\tW\tP\tG(Z,W)\tValue\tEnergy(MeV)\n")
    for i in range(len(value)):
        file.write(f"{channel[i]}\t{real_counts[i]}\t{W[i]}\t{P[i]}\t{G[i]}\t{value[i]}\t{energy[i] / 1000}\n")

# Load table
data_table = np.loadtxt("Table.txt", skiprows = 1)
Energy = data_table[:, 6]
Value = data_table[:, 5]

plt.figure(figsize=(10, 6))
plt.plot(Energy, Value, color = "black")
plt.plot(Energy, np.sqrt(real_counts), color = "red" )
plt.xlabel("E (MeV)")
plt.ylabel("Values")
plt.show()
