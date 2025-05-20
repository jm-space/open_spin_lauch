from enum import Enum, auto

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

# Tube dimensions
h_1 = 40 #[mm]	
w_1 = 40 #[mm]	
t_1 = 4 #[mm]	

# Center motorization & bearing		
r_drive = 0.100	# [m] Driving radius
D_bear = 80.000	# [mm] Outer radius of bearing
d_bear = 50.000	# [mm] Inner radius of bearing
d1_bear = 58.000 # [mm] Outer radius of inner ring
w_bear = 20.000	# [mm] Bearing width

# Physical constants	
g = 9.81 #[m/s^2]	
dt = 0.02 #[s]	

class Material(Enum):
    STEEL_S235 = auto()     #Automatically a unique value to each class member
    CARBON_FIBRE = auto()
    PPA_CF = auto()
    ALUMINIUM_6060 = auto()

# Using ENUM as keys for the normal dictonary entry
materials = {
    Material.STEEL_S235: {
        'density': 7850,
        'yield_strength': 2.35e8,
        'young_modulus': 2.1e11,
        'shear_modulus': 8.1e10,
    },
    Material.CARBON_FIBRE: {
        'density': 1500,
        'yield_strength': 6.0e8,
        'young_modulus': 2.28e11,
        'shear_modulus': 1.5e10,
    },
    Material.PPA_CF: {
        'yield_strength': 1.68e8,
        'young_modulus': 9.86e9,
    },
    Material.ALUMINIUM_6060: {
        'density': 2700,                # kg/m³
        'yield_strength': 6e7,          # Pa (60 - 110MPa)
        'young_modulus': 6.9e10,        # Pa (69 GPa)
        'shear_modulus': 2.6e10,        # Pa (26 GPa)
    },
}