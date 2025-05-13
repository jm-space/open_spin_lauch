import params as params
import kinetics as sec
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize_scalar
from trajectory import simulate, objective
import mechanics as mt

# Calculate the intital height at which the rocket is released
h_1 = params.h_0 - params.r_1*np.sin(np.deg2rad(params.θ_release))

# Optimizing release velocity to reach target altitude h_max with drag
result = minimize_scalar(lambda v_0: objective(v_0, h_1), bounds=(10, 200), method='bounded')
trajectory_data_drag = simulate(result.x, h_1, True, True) 

# Simulate trajectory for target altitude without drag
v_0 = np.sqrt(2*params.g*(params.h_max-h_1))/np.cos(np.deg2rad(params.θ_release)) #First estimate of release velocity
trajectory_data_no_drag = simulate(v_0, h_1, False, True)

# Find critical values 
t_max = trajectory_data_drag["time"].max()
x_impact = trajectory_data_drag["x"].max()
y_max = trajectory_data_drag["y"].max()
apogee_index = np.argmax(trajectory_data_drag["y"])
t_apogee = trajectory_data_drag["time"][apogee_index]

ω_0 = result.x / params.r_1  # [rad/s]
n_0_rps = ω_0 / (2 * np.pi)  # [rev/s]
n_0_rpm = n_0_rps * 60  # [rpm]

α = ω_0 / params.t_speed_up  # [rad/s^2]
a_t = α * params.r_1  # [m/s^2]
a_n0 = result.x**2 / params.r_1  # [m/s^2]
n = a_n0 / params.g  # [g]

# Calculate forces, including drag force
F_d_rocket = 1 / 2 * params.cd_rocket * params.ρ_air * params.A_rocket * result.x**2 / 10**6  # [N]

# Torque calculations
T_d = F_d_rocket * params.r_1  # [Nm]
T_j = sec.J_total * α  # [Nm]
T = T_d + T_j  # [Nm]
P = T * ω_0  # [W]

# Accelerations and forces for the rocket and rod
a_n0_tip = ω_0**2 * params.r_1 # [m/s^2]
a_n0_rod = ω_0**2  * (params.r_1 / 2) # [m/s^2]

F_n_rocket = params.m_rocket * a_n0_tip  # [N]
F_n_rod = sec.m_rod * a_n0_rod  # [N]

F_max = F_n_rocket + F_n_rod  # [N]
# Tensile stress calculation
σ_rod_tensile = mt.axial_stress(F=F_max, A=sec.A_rod)  # [MPa]

# Bending stress calculations
F_t_rocket = a_t * params.r_1  # [N]
F_t_rod = a_t * (params.r_1 / 2)  # [N]
F_A = F_t_rocket + F_t_rod  # [N]
M_A = F_d_rocket * params.r_1 + F_t_rocket * params.r_1 + F_t_rod * (params.r_1 / 2)  # [Nm]
σ_rod_bending = mt.bending_stress(M=M_A, y=(params.d_rod / 2), I=sec.I_rod)  # [MPa]

print(F_A)
print(M_A)

# Beam deflection (cantilever beam with force at A)
δ_rod_bending = mt.cantilever_beam_deflection(F=F_A, L=params.r_1*1e3, E=params.materials["carbon_fibre"]["young_modulus"], I = sec.I_rod)  # [mm]

# Von Mises stress
σ_rod = mt.von_mises_stress(σx=σ_rod_tensile, σy=σ_rod_bending, τxy=0)  # [MPa]

# Safety factor
safety_rod = params.materials["carbon_fibre"]["yield_strength"]/σ_rod

# Output results
print(f"Axial stress: {σ_rod_tensile:.2f} MPa")
print(f"Bending stress: {σ_rod_bending:.2f} MPa")
print(f"Cantilever beam deflection: {δ_rod_bending:.2f} mm")
print(f"Von Mises stress: {σ_rod:.2f} MPa")
print(f"Safety factor: {safety_rod:.2f}")


# f-string text block
text = f"""=== Main Rod ===
A = {sec.A_rod:.2f} mm²
V = {sec.V_rod:.0f} mm³
I = {sec.I_rod:.0f} mm^4
m = {sec.m_rod:.4f} kg
J = {sec.J_rod:.3f} kg·m²

=== Counterweight Rod ===
A = {sec.A_rod_cw:.2f} mm²
V = {sec.V_rod_cw:.0f} mm³
I = {sec.I_rod_cw:.0f} mm^4
m = {sec.m_rod_cw:.4f} kg
J = {sec.J_rod_cw:.3f} kg·m²

=== Attached Masses ===
J_rocket = {sec.J_rocket:.3f} kg·m²
J_cw = {sec.J_cw:.3f} kg·m²

=== Total ===
J_total = {sec.J_total:.3f} kg·m²"""

text2 = f"""
α  = {α:0.2f} rad/s^2
a_t = {a_t:0.2f} m/s^2
a_n0 = {a_n0:0.2f} m/s^2
n = {n:0.2f} g

F_d_rocket = {F_d_rocket:0.2f} N


T_d = {T_d:0.2f} Nm
T_j = {T_j:0.2f} Nm
T = {T:0.2f} Nm
P = {P:0.2f} W"""

# Create a figure with custom layout using gridspec
fig = plt.figure(figsize=(6, 10))

# Define gridspec with 2 rows and 1 column
gs = fig.add_gridspec(2, 1, height_ratios=[0.4, 0.6])  # Top part for text, bottom for plot

# Top part for the text
ax_text = fig.add_subplot(gs[0])  # Create an axis for the text
ax_text.set_axis_off()  # Hide the axis for the text

# Add multiline text in the top-left corner
ax_text.text(0.01, 0.99, text, fontsize=12, va='top', ha='left', family='monospace')
ax_text.text(0.5, 0.99, text2, fontsize=12, va='top', ha='left', family='monospace')

# Bottom part for the plot
ax_plot = fig.add_subplot(gs[1])  # Create another axis for the plot

# Plotting the trajectory
ax_plot.plot(trajectory_data_drag["x"], trajectory_data_drag["y"], label="Rocket Trajectory", color='b', linestyle='-')
ax_plot.plot(trajectory_data_no_drag["x"], trajectory_data_no_drag["y"], label="No Drag", color='r', linestyle='--')
ax_plot.set_xlabel('X (m)', fontsize=12)
ax_plot.set_ylabel('Y (m)', fontsize=12)
ax_plot.set_title('Rocket Flight Trajectory', fontsize=14)  # Add a title
ax_plot.grid(True)  # Adds a grid to the plot
ax_plot.legend(loc='best')  # Add a legend to label the plot at the best position

# Adjust layout and display the figure
plt.tight_layout()
plt.show()

import tkinter as tk
from tkinter import ttk

# === Example data ===
structural_data = {
    "Main Rod": {
        "Area (A)": "502.65 mm²",
        "Volume (V)": "150000 mm³",
        "Mass (m)": "0.1500 kg",
        "Inertia (I)": "0.123 kg·m²"
    },
    "Counterweight Rod": {
        "Area (A)": "400.00 mm²",
        "Volume (V)": "100000 mm³",
        "Mass (m)": "0.1200 kg",
        "Inertia (I)": "0.089 kg·m²"
    },
    "Attached Masses": {
        "Rocket Inertia": "0.450 kg·m²",
        "Counterweight Inertia": "0.300 kg·m²"
    }
}