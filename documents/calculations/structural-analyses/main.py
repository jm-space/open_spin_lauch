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
from structural_object import *
from params import Material
import gui

print("0 ... Carbon Fibre Rod D25 d20")
print("1 ... Aluminium Tube 30x30x3")
print("2 ... Aluminium Tube 40x40x4")
print("3 ... Aluminium Tube 50x50x4")
print("4 ... Aluminium Tube 60x40x4")
choice = int(input("Tube or Rod?"))

if choice == 0:
    rod_rocket = CircularTube(length=params.r_1, outer_diameter=params.D_rod*1e-3, inner_diameter=params.d_rod*1e-3, material_type=Material.CARBON_FIBRE)
    rod_cw = CircularTube(length=params.r_cw, outer_diameter=params.D_rod_cw*1e-3, inner_diameter=params.d_rod_cw*1e-3, material_type=Material.CARBON_FIBRE)
elif choice == 1:
    rod_rocket = RectangularTube(length=params.r_1, outer_width=30e-3, outer_height=30e-3, thickness=3e-3, material_type=Material.ALUMINIUM_6060)
    rod_cw = rod_rocket
elif choice == 2:
    rod_rocket = RectangularTube(length=params.r_1, outer_width=40e-3, outer_height=40e-3, thickness=4e-3, material_type=Material.ALUMINIUM_6060)
    rod_cw = rod_rocket
elif choice == 3:
    rod_rocket = RectangularTube(length=params.r_1, outer_width=50e-3, outer_height=50e-3, thickness=4e-3, material_type=Material.ALUMINIUM_6060)
    rod_cw = rod_rocket
elif choice == 4:
    rod_rocket = RectangularTube(length=params.r_1, outer_width=40e-3, outer_height=60e-3, thickness=4e-3, material_type=Material.ALUMINIUM_6060)
    rod_cw = rod_rocket


# ============================
#    TRAJECTORY SIMULATION
# ============================

# Calculate the intital height at which the rocket is released
h_1 = params.h_0 - rod_rocket.length*np.sin(np.deg2rad(params.θ_release))

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

# Find state variables required to achieve target trajectory with drag
ω_0 = result.x / rod_rocket.length  # [rad/s]
n_0_rps = ω_0 / (2 * np.pi)  # [rev/s]
n_0_rpm = n_0_rps * 60  # [rpm]

α = ω_0 / params.t_speed_up  # [rad/s^2]
a_t_rocket = α * rod_rocket.length  # [m/s^2]
a_t_cw= α * rod_cw.length  # [m/s^2]
a_n0 = result.x**2 / rod_rocket.length  # [m/s^2]
n = a_n0 / params.g  # [g]


# ============================
#    STRUCTURAL ANALYSIS
# ============================
#Force and torque through drag force on rocket
F_d_rocket = 1 / 2 * params.cd_rocket * params.ρ_air * params.A_rocket * result.x**2 / 10**6  # [N] 
F_d_cw = F_d_rocket #CHANGE → actual drag value of counterweight
T_d = F_d_rocket * rod_rocket.length  # [Nm]

# Torque through total mass moment of inertia of the system
J_rocket = params.m_rocket * rod_rocket.length**2  # [kg*m^2]
J_cw = params.m_cw * rod_cw.length**2         # [kg*m^2]
J_total = rod_rocket.J_end + rod_cw.J_end + J_rocket + J_cw # [kg*m^2]
T_j = J_total * α  # [Nm] 

# Total torque and required power
T = T_d + T_j  # [Nm]
P = T * ω_0  # [W]


# ============================
#   DIMENSIONING ROD-ROCKET 
# ============================

# Accelerations and forces for the rocket and rod
a_n0_rocket = ω_0**2 * rod_rocket.length # [m/s^2]
a_n0_rod = ω_0**2  * (rod_rocket.length / 2) # [m/s^2]

F_n_rocket = params.m_rocket * a_n0_rocket  # [N]
F_n_rod = rod_rocket.mass * a_n0_rod  # [N]

F_n_max_rod_rocket = F_n_rocket + F_n_rod  # [N]

# Tensile stress calculation
σ_rod_rocket_tensile = rod_rocket.axial_stress(F_n_max_rod_rocket)

# Bending stress calculations 
# Calculate tangential forces on rod 
F_t_rocket = a_t_rocket * params.m_rocket  # [N] Force through acceleration of rocket mass
F_t_rod_rocket = (a_t_rocket / 2) * rod_rocket.mass  # [N] Force through acceleration of rod mass
F_t_max_rod_rocket = F_t_rocket + F_t_rod_rocket + F_d_rocket # [N] Total tangential force at attachment A
M_max_rod_rocket = F_d_rocket * rod_rocket.length + F_t_rocket * rod_rocket.length + F_t_rod_rocket * (rod_rocket.length / 2)  # [Nm] Total bending moment at attachment A

σ_rod_rocket_bending = rod_rocket.bending_stress(M_max_rod_rocket)
δ_rod_rocket_bending = rod_rocket.beam_deflection(F_t_max_rod_rocket)
τ_rod_rocket_shear = rod_rocket.transverse_shear(F_t_max_rod_rocket)
σ_rod_rocket_total = rod_rocket.von_mises_stress(σ_rod_rocket_tensile, σ_rod_rocket_bending, τ_rod_rocket_shear)
safety_factor_rod_rocket = rod_rocket.safety_factor(σ_rod_rocket_total)

# ============================
#   DIMENSIONING ROD-CW
# ============================
# Accelerations and forces for the rocket and rod
a_n0_cw_tip = ω_0**2 * rod_cw.length # [m/s^2]
a_n0_rod_cw = ω_0**2  * (rod_cw.length / 2) # [m/s^2]

F_n_cw = params.m_cw * a_n0_cw_tip  # [N]
F_n_rod_cw = rod_cw.mass * a_n0_rod_cw  # [N]

F_n_max_rod_cw = F_n_cw + F_n_rod_cw  # [N]

# Tensile stress calculation
σ_rod_cw_tensile = rod_cw.axial_stress(F_n_max_rod_cw) 

# Bending stress calculations
F_t_cw = a_t_cw * params.m_cw # [N] Force through acceleration of rocket mass
F_t_rod_cw = (a_t_cw / 2) * rod_cw.mass  # [N] Force through acceleration of rod mass
F_t_max_rod_cw = F_t_cw + F_t_rod_cw + F_d_cw # [N] Total tangential force at attachment A with drag force
M_max_rod_cw = F_d_cw * rod_cw.length + F_t_cw * rod_cw.length + F_t_rod_cw * (rod_cw.length / 2)  # [Nm] Total bending moment at attachment A

σ_rod_cw_bending = rod_cw.bending_stress(M_max_rod_cw)
δ_rod_cw_bending = rod_cw.beam_deflection(F_t_max_rod_cw) 
τ_rod_cw_shear = rod_cw.transverse_shear(F_t_max_rod_cw)
σ_rod_cw_total = rod_cw.von_mises_stress(σ_rod_cw_tensile, σ_rod_cw_bending, τ_rod_cw_shear)
safety_factor_rod_cw = rod_cw.safety_factor(σ_rod_cw_total)

# ============================
#   DIMENSIONING BEARING
# ============================
F_cr = F_n_cw + F_n_rod_cw - F_n_rod # [N] Force that is acting on the bearing for half a revolution after the first payload has been deployed
F_drive = T * params.r_drive # [N] Driving force through chain / crank handle (mostly static)
F_grav = (rod_rocket.mass + rod_cw.mass + params.m_cw) * params.g # [N] Approximate gravitational force (static) for half a revolution after the first payload has been deployed
	
# Areas & tensions	
A_projy = params.D_bear * params.w_bear # [mm²] The projected area in Y (radial)	
A_projx = (params.d1_bear**2 - params.d_bear**2) * np.pi / 4 # [mm²] The projected area in X (axial)	

# ============================
#   CLAMP SIZING
# ============================

# Forces during spin up, assuming symmetrical forces
F_Rn = F_n_rocket /2
F_Rt = F_t_rocket /2

cone_angle = 60 # [°] Cone angle of the clamp

F_Cxy =  F_Rn / (2*np.sin(np.deg2rad(cone_angle)))
F_Czy =  F_Rt / (2*np.sin(np.deg2rad(cone_angle)))

# Clamping forces
F_Cx = F_Cxy*np.sin(np.deg2rad(cone_angle))
F_Cy = F_Cxy*np.cos(np.deg2rad(cone_angle)) + F_Czy*np.cos(np.deg2rad(cone_angle))
F_Cz = -F_Czy*np.sin(np.deg2rad(cone_angle))

# Clamp dimensions
l_SBx = 55
l_BCx = 40
l_By = 20
l_Cy = 11
l_Sy = 13

# Reaction forces
F_Sy = F_Cy*l_BCx/l_SBx
F_By = F_Sy + F_Cy
F_Bx = F_Cx

print(F_Cx)
print(F_Cy)
print(F_Cz)
print(F_Sy)
print(F_By)
print(F_Bx)


# ============================
#   VISUALIZATION
# ============================

graph_data = [
    ["Actual Apogee", f"{y_max_drag:.2f} m", f"{y_max_no_drag:.2f} m"],
    ["Time to Apogee", f"{t_apogee_drag:.2f} s", f"{t_apogee_no_drag:.2f} s"],
    ["Horizontal Displacement", f"{x_impact_drag:.2f} m", f"{x_impact_no_drag:.2f} m"],
]

print(tabulate(
    graph_data,
    headers=["Quantity", "Drag", "No Drag"],
    tablefmt="fancy_grid"
))

kinematic_data = [
    ["Release Velocity", f"{result.x:.2f} m/s"],
    ["Release Angular Velocity", f"{ω_0:.2f} rad/s"],
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
    headers=["Quantity", "Value"],
    tablefmt="fancy_grid"
))

strucutal_data = [
    ["Axial Force", f"{F_n_max_rod_rocket:.2f} N", f"{F_n_max_rod_cw:.2f} N"],
    ["Axial Stress", f"{σ_rod_rocket_tensile*1e-6:.2f} MPa", f"{σ_rod_cw_tensile*1e-6:.2f} MPa"],
    ["Bending Stress", f"{σ_rod_rocket_bending*1e-6:.2f} MPa", f"{σ_rod_cw_bending*1e-6:.2f} MPa"],
    ["Tangential Force", f"{F_t_max_rod_rocket:.2f} N", f"{F_t_max_rod_cw:.2f} N"],
    ["Beam Deflection", f"{δ_rod_rocket_bending*1e3:.2f} mm", f"{δ_rod_cw_bending*1e3:.2f} mm"],
    ["Transverse Shear", f"{τ_rod_rocket_shear*1e-6:.2f} MPa", f"{τ_rod_cw_shear*1e-6:.2f} MPa"],
    ["Von Mises Stress", f"{σ_rod_rocket_total*1e-6:.2f} MPa", f"{σ_rod_cw_total*1e-6:.2f} MPa"],
    ["Saftey Factor", f"{safety_factor_rod_rocket:.2f} ", f"{safety_factor_rod_cw:.2f} "],
]


print(tabulate(
    strucutal_data,
    headers=["Quantity", "Rocket Side", "Counterweight Side"],
    tablefmt="fancy_grid"
))




# ============================
#       VISUALIZATION
# ============================

