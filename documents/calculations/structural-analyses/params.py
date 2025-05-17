# Kinematics	
h_max = 150.00 #[m]	
include_drag = True
θ_release = 40.00 #[°]	
	
# Kinetics
t_speed_up = 60 #[s]	

# payload parameters
m_rocket = 1.50 #[kg] 
m_cw = 1.50 #[kg] 
cd_rocket = 0.75 #[] 	
A_rocket = 3850 #[mm^2]	
ρ_air = 1.225225 #[kg/m^3]	
	
# Stand	
h_0 = 3.00 #[m]	
	
# Rod to rocket	
r_1 = 2.00 #[m]	
D_rod = 25 #[mm]	
d_rod = 20 #[mm]	

# Rod to counterweight	
r_cw = 2.00 #[m]	
D_rod_cw = 25 #[mm]	
d_rod_cw = 20 #[mm]	

# Center motorization & bearing		
r_drive = 0.100	# [m] Driving radius
D_bear = 80.000	# [mm] Outer radius of bearing
d_bear = 50.000	# [mm] Inner radius of bearing
d1_bear = 58.000 # [mm] Outer radius of inner ring
w_bear = 20.000	# [mm] Bearing width

# Physical constants	
g = 9.81 #[m/s^2]	
dt = 0.02 #[s]	

materials = {
    "steel_S235": {
        'density': 7850,                  # kg/m³ (correct)
        'yield_strength': 2.35e8,        # Pa (235 MPa)
        'young_modulus': 2.1e11,         # Pa (210 GPa)
        'shear_modulus': 8.1e10,         # Pa (81 GPa)
    },
    "carbon_fibre": {
        'density': 1500,                 # kg/m³ (correct)
        'yield_strength': 6.0e8,         # Pa (600 MPa)
        'young_modulus': 2.28e11,        # Pa (228 GPa)
        'shear_modulus': 1.5e10,         # Pa (15 GPa)
    },
    "PPA_CF": {
        'yield_strength': 1.68e8,        # Pa (168 MPa)
        'young_modulus': 9.86e9,         # Pa (9.86 GPa)
    },
}
