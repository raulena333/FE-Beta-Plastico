import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import os

# Configuración de parámetros para mejorar la apariencia del gráfico
params = {
    'xtick.labelsize': 17,    
    'ytick.labelsize': 17,      
    'axes.titlesize': 18,
    'axes.labelsize': 18,
    'legend.fontsize': 16
}
pylab.rcParams.update(params) 

output_dir = './Resultados'
os.makedirs(output_dir, exist_ok=True) 

# Nombre del isótopo
name_nucleo = {"Cesio137", "Europio152", "Bario133", "Talio204"}

# Load background data
data_fondo_energy = np.loadtxt('./Data/Datos_Fondo_(keV).txt', skiprows=1)  
data_fondo_canales = np.loadtxt('./Data/Datos de fondo (canales).txt', skiprows=1) 

# Plot spectre
plt.figure(figsize=(10, 6))
plt.plot(data_fondo_energy, data_fondo_canales, color="black")

plt.xlabel("E (keV)")
plt.ylabel("Counts")
plt.savefig(os.path.join(output_dir, 'Fondo.pdf'))
plt.close()

# Extract energy and channels
energies = data_fondo_energy[:, 0]
channels = data_fondo_canales[:, 0]
counts_background = data_fondo_canales[:, 1]
    
for name in name_nucleo:
    data_nucleo_energy = np.loadtxt('./Datos/Datos ' + name + ' (keV).txt', skiprows=1) 
    counts_nucleus = data_nucleo_energy[:, 1]

    # Calculate real counts, as nucleus - background 
    real_counts = counts_nucleus - counts_background

    # Plot spectre
    plt.figure(figsize=(10, 6))
    plt.plot(energies, real_counts, label=name, color="black")

    plt.xlabel("E (keV)")
    plt.ylabel("Counts")
    
    plt.savefig(os.path.join(output_dir, name+ '.pdf'))
    plt.close()