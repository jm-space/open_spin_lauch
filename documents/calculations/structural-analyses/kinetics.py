import numpy as np
import params as params
import matplotlib.pyplot as plt

# Rod to Rocket
A_rod = (params.D_rod**2 - params.d_rod**2) * np.pi / 4  # [mm^2]
V_rod = A_rod * params.r_1 * 1000  # [mm^3]
m_rod = (V_rod / 1e9) * params.materials["carbon_fibre"]["density"]  # [kg]
I_rod = (params.D_rod**4 - params.d_rod**4) * np.pi/64 # [mm^4]
J_rod = (1/3) * m_rod * params.r_1**2  # [kg*m^2] - rod rotating about one end

# Rod to Counterweight
A_rod_cw = (params.D_rod_cw**2 - params.d_rod_cw**2) * np.pi / 4  # [mm^2]
V_rod_cw = A_rod_cw * params.r_cw * 1000  # [mm^3]
m_rod_cw = (V_rod_cw / 1e9) * params.materials["carbon_fibre"]["density"]  # [kg]
I_rod_cw = (params.D_rod_cw**4 - params.d_rod_cw**4) * np.pi/64 # [mm^4]
J_rod_cw = (1/3) * m_rod_cw * params.r_cw**2  # [kg*m^2] - same logic

# Attached Masses
J_rocket = params.m_rocket * params.r_1**2  # [kg*m^2]
J_cw = params.m_cw * params.r_cw**2         # [kg*m^2]

# Total 
J_total = J_rod + J_rod_cw + J_rocket + J_cw # [kg*m^2]

print(f"Main Rod: A = {A_rod:.2f} mm² | V = {V_rod:.0f} mm³ | m = {m_rod:.4f} kg | I = {J_rod:.3f} kg·m²")
print(f"Counterweight Rod: A = {A_rod_cw:.2f} mm² | V = {V_rod_cw:.0f} mm³ | m = {m_rod_cw:.4f} kg | I = {J_rod_cw:.3f} kg·m²")
print(f"Attached Masses: I_rocket = {J_rocket:.3f} kg·m² | I_cw = {J_cw:.3f} kg·m²")