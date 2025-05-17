# Public libraries
import numpy as np
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tabulate import tabulate

# Self developed libraries
import params as params
from trajectory import simulate, objective
import kinetics as sec
import mechanics as mt
from structural_object import *
import gui


#Replace material string with enum

# ============================
#    TRAJECTORY SIMULATION
# ============================

# Calculate the intital height at which the rocket is released
h_1 = params.h_0 - params.r_1*np.sin(np.deg2rad(params.θ_release))

# Optimizing release velocity to reach target altitude h_max with drag
result = minimize_scalar(lambda v_0: objective(v_0, h_1), bounds=(10, 500), method='bounded')
trajectory_data_drag = simulate(result.x, h_1, True, True) 

# Simulate trajectory for target altitude without drag
v_0_no_drag = np.sqrt(2*params.g*(params.h_max-h_1))/np.cos(np.deg2rad(params.θ_release)) #First estimate of release velocity
trajectory_data_no_drag = simulate(v_0_no_drag, h_1, False, True)

# Find critical values from simulation without drag
# Only parameters for trajectory are anaylzed for no drag condition other no drag variables are unimportant
t_max_no_drag = trajectory_data_no_drag["time"].max()
x_impact_no_drag  = trajectory_data_no_drag["x"].max()
y_max_no_drag  = trajectory_data_no_drag["y"].max()
apogee_index_no_drag  = np.argmax(trajectory_data_no_drag["y"])
t_apogee_no_drag = trajectory_data_no_drag["time"][apogee_index_no_drag ]

# Find critical values from simulation with drag
t_max_drag = trajectory_data_drag["time"].max()
x_impact_drag  = trajectory_data_drag["x"].max()
y_max_drag  = trajectory_data_drag["y"].max()
apogee_index_drag  = np.argmax(trajectory_data_drag["y"])
t_apogee_drag  = trajectory_data_drag["time"][apogee_index_drag ]

ω_0 = result.x / params.r_1  # [rad/s]
n_0_rps = ω_0 / (2 * np.pi)  # [rev/s]
n_0_rpm = n_0_rps * 60  # [rpm]

α = ω_0 / params.t_speed_up  # [rad/s^2]
a_t_rocket = α * params.r_1  # [m/s^2]
a_t_cw= α * params.r_cw  # [m/s^2]
a_n0 = result.x**2 / params.r_1  # [m/s^2]
n = a_n0 / params.g  # [g]




# ============================
#    STRUCTURAL ANALYSIS
# ============================
#Force through drag force on rocket
F_d_rocket = 1 / 2 * params.cd_rocket * params.ρ_air * params.A_rocket * result.x**2 / 10**6  # [N] 
F_d_cw = F_d_rocket #CHANGE → actual drag value of counterweight


# Torque calculations
T_d = F_d_rocket * params.r_1  # [Nm]
T_j = sec.J_total * α  # [Nm]
T = T_d + T_j  # [Nm]
P = T * ω_0  # [W]


rod_rocket = Tube(length=params.r_1, outer_diameter=params.D_rod*1e-3, inner_diameter=params.d_rod*1e-3, material_name="carbon_fibre")
rod_cw = Tube(length=params.r_cw, outer_diameter=params.D_rod_cw*1e-3, inner_diameter=params.d_rod_cw*1e-3, material_name="carbon_fibre")

# ============================
#   DIMENSIONING ROD-ROCKET 
# ============================

# Accelerations and forces for the rocket and rod
a_n0_rocket = ω_0**2 * params.r_1 # [m/s^2]
a_n0_rod = ω_0**2  * (params.r_1 / 2) # [m/s^2]

F_n_rocket = params.m_rocket * a_n0_rocket  # [N]
F_n_rod = sec.m_rod * a_n0_rod  # [N]

F_n_max_rod_rocket = F_n_rocket + F_n_rod  # [N]

# Tensile stress calculation
σ_rod_rocket_tensile = mt.axial_stress(F=F_n_max_rod_rocket, A=sec.A_rod)  # [MPa]

# Bending stress calculations 
# Calculate tangential forces on rod 
F_t_rocket = a_t_rocket * params.m_rocket  # [N] Force through acceleration of rocket mass
F_t_rod_rocket = (a_t_rocket / 2) * params.m_rocket  # [N] Force through acceleration of rod mass
F_t_max_rod_rocket = F_t_rocket + F_t_rod_rocket + F_d_rocket # [N] Total tangential force at attachment A
M_max_rod_rocket = F_d_rocket * params.r_1 + F_t_rocket * params.r_1 + F_t_rod_rocket * (params.r_1 / 2)  # [Nm] Total bending moment at attachment A

σ_rod_rocket_bending = mt.bending_stress(M = M_max_rod_rocket, y = (params.D_rod / 2), I = sec.I_rod)  # [MPa]

# Beam deflection (cantilever beam with force at A)
δ_rod_rocket_bending = mt.cantilever_beam_deflection(F = F_t_max_rod_rocket, L = params.r_1*1e3, E = params.materials["carbon_fibre"]["young_modulus"], I = sec.I_rod)  # [mm]

# Von Mises stress to determine failure critierion
σ_rod_rocket = mt.von_mises_stress(σx = σ_rod_rocket_tensile, σy = σ_rod_rocket_bending, τxy = 0)  # [MPa]

# Safety factor
safety_rod_rocket = params.materials["carbon_fibre"]["yield_strength"] / σ_rod_rocket


print(rod_rocket.axial_stress(F_n_max_rod_rocket)*1e-6)
print(rod_rocket.bending_stress(M_max_rod_rocket)*1e-6)
print(rod_rocket.beam_deflection(F_t_max_rod_rocket))

# ============================
#   DIMENSIONING ROD-CW
# ============================
# Accelerations and forces for the rocket and rod
a_n0_cw_tip = ω_0**2 * params.r_cw # [m/s^2]
a_n0_rod_cw = ω_0**2  * (params.r_cw / 2) # [m/s^2]

F_n_cw = params.m_cw * a_n0_cw_tip  # [N]
F_n_rod_cw = sec.m_rod_cw * a_n0_rod_cw  # [N]

F_n_max_rod_cw = F_n_cw + F_n_rod_cw  # [N]

# Tensile stress calculation
σ_rod_cw_tensile = mt.axial_stress(F=F_n_max_rod_cw, A=sec.A_rod_cw)  # [MPa]

# Bending stress calculations
F_t_cw = a_t_cw * params.m_cw # [N] Force through acceleration of rocket mass
F_t_rod_cw = (a_t_cw / 2) * params.m_cw  # [N] Force through acceleration of rod mass
F_t_max_rod_cw = F_t_cw + F_t_rod_cw + F_d_cw # [N] Total tangential force at attachment A with drag force
M_max_rod_cw = F_d_cw * params.r_cw + F_t_cw * params.r_cw + F_t_rod_cw * (params.r_cw / 2)  # [Nm] Total bending moment at attachment A
σ_rod_cw_bending = mt.bending_stress(M = M_max_rod_cw, y = (params.D_rod_cw / 2), I = sec.I_rod)  # [MPa]

# Beam deflection (cantilever beam with force at A)
δ_rod_cw_bending = mt.cantilever_beam_deflection(F = F_t_max_rod_cw, L = params.r_cw*1e3, E = params.materials["carbon_fibre"]["young_modulus"], I = sec.I_rod_cw)  # [mm]

# Von Mises stress to determine failure critierion
σ_rod_cw = mt.von_mises_stress(σx = σ_rod_cw_tensile, σy = σ_rod_cw_bending, τxy = 0)  # [MPa]

# Safety factor
safety_rod_cw = params.materials["carbon_fibre"]["yield_strength"] / σ_rod_cw



# ============================
#   DIMENSIONING BEARING
# ============================
F_cr = F_n_cw + F_n_rod_cw - F_n_rod # [N] Force that is acting on the bearing for half a revolution after the first payload has been deployed
F_drive = T * params.r_drive # [N] Driving force through chain / crank handle (mostly static)
F_grav = (sec.m_rod + sec.m_rod_cw + params.m_cw) * params.g # [N] Approximate gravitational force (static) for half a revolution after the first payload has been deployed
	
# Areas & tensions	
A_projy = params.D_bear * params.w_bear # [mm²] The projected area in Y (radial)	
A_projx = (params.d1_bear**2 - params.d_bear**2) * np.pi / 4 # [mm²] The projected area in X (axial)	


kinematic_data = [
    ["Actual Apogee", f"{y_max_drag:.2f} m", f"{y_max_no_drag:.2f} m"],
    ["Time to Apogee", f"{t_apogee_drag:.2f} m", f"{t_apogee_no_drag:.2f} m"],
    ["Horizontal Displacement", f"{x_impact_drag:.2f} m", f"{x_impact_no_drag:.2f} m"],
    ["Release Velocity", f"{result.x:.2f} m/s"],
    ["Release Angular Velocity", f"{ω_0:.2f} rad/s^2"],
    ["Turns per Second", f"{n_0_rps:.2f} /s"],
    ["Turns per Minute", f"{n_0_rpm:.2f} /min"],
    ["Tangential Acceleration @Rocket", f"{a_t_rocket:.2f} m/s^2"],
    ["Normal Acceleration @Rocket", f"{a_n0:.2f} m/s^2"],    
    ["G-Factor @Rocket", f"{n:.2f}"],
    ["Rocket Drag at Spinup", f"{F_d_rocket:.2f} N"],
    ["Torque at Spinup", f"{T:.2f} Nm"],
    ["Power at Spinup", f"{P:.2f} W"],
]

print(tabulate(
    kinematic_data,
    headers=["Quantity", "Drag", "No Drag"],
    tablefmt="fancy_grid"
))

strucutal_data = [
    ["Axial Force", f"{F_n_max_rod_rocket:.2f} N", f"{F_n_max_rod_cw:.2f} N"],
    ["Axial Stress", f"{σ_rod_rocket_tensile:.2f} MPa", f"{σ_rod_cw_tensile:.2f} MPa"],
    ["Bending Stress", f"{σ_rod_rocket_bending:.2f} MPa", f"{σ_rod_cw_bending:.2f} MPa"],
    ["Tangential Force", f"{F_t_max_rod_rocket:.2f} N", f"{F_t_max_rod_cw:.2f} N"],
    ["Beam Deflection", f"{δ_rod_rocket_bending:.2f} mm", f"{δ_rod_cw_bending:.2f} mm"],
    ["Von Mises Stress", f"{σ_rod_rocket:.2f} MPa", f"{σ_rod_cw:.2f} MPa"],
    ["Safety Factor", f"{safety_rod_rocket:.2f}", f"{safety_rod_cw:.2f}"],
]

print(tabulate(
    strucutal_data,
    headers=["Quantity", "Rocket Side", "Counterweight Side"],
    tablefmt="fancy_grid"
))




# ============================
#       VISUALIZATION
# ============================

# f-string text block
text = f"""Main Rod:
A = {sec.A_rod:.2f} mm²
V = {sec.V_rod:.0f} mm³
I = {sec.I_rod:.0f} mm^4
m = {sec.m_rod:.4f} kg
J = {sec.J_rod:.3f} kg·m²

Counterweight Rod:
A = {sec.A_rod_cw:.2f} mm²
V = {sec.V_rod_cw:.0f} mm³
I = {sec.I_rod_cw:.0f} mm^4
m = {sec.m_rod_cw:.4f} kg
J = {sec.J_rod_cw:.3f} kg·m²

Attached Masses:
J_rocket = {sec.J_rocket:.3f} kg·m²
J_cw = {sec.J_cw:.3f} kg·m²

Total:
J_total = {sec.J_total:.3f} kg·m²"""

text2 = f"""
α  = {α:0.2f} rad/s^2
a_t = {a_t_rocket:0.2f} m/s^2
a_n0 = {a_n0:0.2f} m/s^2
n = {n:0.2f} g

F_d_rocket = {F_d_rocket:0.2f} N


T_d = {T_d:0.2f} Nm
T_j = {T_j:0.2f} Nm
T = {T:0.2f} Nm
P = {P:0.2f} W"""

# Create a simple figure and axes
fig, ax = plt.subplots(figsize=(6, 6))

# Plot your rocket data
ax.plot(trajectory_data_drag["x"], trajectory_data_drag["y"], label="Rocket Trajectory", color='b')
ax.plot(trajectory_data_no_drag["x"], trajectory_data_no_drag["y"], label="No Drag", color='r', linestyle='--')

# Axis labels and style
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_title("Rocket Flight Trajectory")
ax.grid(True)
ax.legend()



# Create a white figure
fig, ax = plt.subplots(figsize=(6, 8))
ax.set_axis_off()

# Add multiline text in top-left corner
ax.text(0.01, 0.99, text, fontsize=12, va='top', ha='left', family='monospace')
ax.text(0.5, 0.99, text2, fontsize=12, va='top', ha='left', family='monospace')

plt.tight_layout()
plt.show()


# Plotting the trajectory
plt.figure(figsize=(6, 6))  # Set a larger figure size
plt.plot(trajectory_data_drag["x"], trajectory_data_drag["y"], label="Rocket Trajectory", color='b', linestyle='-')
plt.plot(trajectory_data_no_drag["x"], trajectory_data_no_drag["y"], label="No Drag", color='r', linestyle='--')
plt.xlabel('X (m)', fontsize=12)
plt.ylabel('Y (m)', fontsize=12)
plt.title('Rocket Flight Trajectory', fontsize=14) # Add a title
plt.grid(True) # Adds a grid to the plot
plt.legend(loc='best') # Add a legend to label the plot at the best positio
plt.show() # Display the plot

#gui.MyGUI()