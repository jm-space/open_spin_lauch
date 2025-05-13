# Kinematics	
h_max = 200.00 #[m]	
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

# Physical constants	
g = 9.81 #[m/s^2]	
dt = 0.02 #[s]	

# Materials
materials = {
    "steel_S235":{
        'density': 7850,  # kg/m^3
        'yield_strength': 235,  # MPa
        'young_modulus': 210000,  # MPa
        'shear_modulus': 81,  # GPa
    },
    "carbon_fibre":{
        'density': 1500,  # kg/m^3
        'yield_strength': 600,  # MPa
        'young_modulus': 228000,  # MPa
        'shear_modulus': 15,  # GPa
    },
    "PPA_CF":{
        'yield_strength': 168,  # MPa
        'young_modulus': 9860,  # MPa
    },
}
