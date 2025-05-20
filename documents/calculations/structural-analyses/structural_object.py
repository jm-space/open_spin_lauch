import numpy as np
import params
from params import materials, Material

""""
BaseTube          # Handles all shared logic: material lookup, common methods
├── CircularTube  # Handles circular-specific geometry
└── RectangularTube  # Handles rectangular-specific geometry
"""
class BaseTube:
    def __init__(self, length, material_type: Material):
        self.length = length

        if material_type not in materials:
            raise ValueError(f"Material '{material_type}' not found in materials dictionary")

        self.material = materials[material_type]

        self.density = self.material.get('density', None)
        self.yield_strength = self.material.get('yield_strength', None)
        self.young_modulus = self.material.get('young_modulus', None)

        self.area = None  # To be set in child class
        self.I = None     # To be set in child class
        self.Q_max = None  # To be set in child class
    
        self.mass = self.compute_mass()
        self.J_center = (1/12) * self.mass * self.length**2 if self.mass else None
        self.J_end = (1/3) * self.mass * self.length**2 if self.mass else None

    def compute_mass(self):
        if self.density is not None and self.area is not None:
            return self.area * self.length * self.density
        return None

    def update_mass_and_moments(self):
        self.mass = self.compute_mass()
        if self.mass is not None:
            self.J_center = (1/12) * self.mass * self.length**2
            self.J_end = (1/3) * self.mass * self.length**2
        else:
            self.J_center = None
            self.J_end = None

    def axial_stress(self, force):
        return force / self.area  # [Pa]

    def bending_stress(self, moment, outer_fiber_distance):
        return moment * outer_fiber_distance / self.I  # [Pa]

    def beam_deflection(self, force):
        if self.young_modulus is None:
            raise ValueError("Young's modulus is not defined for this material")
        return (force * self.length**3) / (3 * self.young_modulus * self.I)  # [m]

    def von_mises_stress(self, σ_axial, σ_bending, τ_shear=0):
        σ_total = σ_axial + σ_bending
        return (σ_total**2 + 3 * τ_shear**2)**0.5

    def safety_factor(self, stress):
        if self.yield_strength is None:
            raise ValueError("Yield strength is not defined for this material")
        return self.yield_strength / stress
    

class CircularTube(BaseTube):
    """
    CircularTube represents a hollow circular tube with specified outer and inner diameters.

    Parameters:
    -----------
    length : float
        Length of the tube [m].
    outer_diameter : float
        Outer diameter of the tube [m].
    inner_diameter : float
        Inner diameter of the tube [m]. Must be smaller than outer_diameter.
    material_type : Material
        Material type key used to look up material properties.

    Attributes:
    -----------
    area : float
        Cross-sectional area of the tube [m²].
    I : float
        Area moment of inertia about the neutral axis [m^4].
    mass : float
        Mass of the tube calculated from material density and volume [kg].

    Methods:
    --------
    bending_stress(moment):
        Calculates bending stress at the outer fiber for a given bending moment.
    """
    def __init__(self, length, outer_diameter, inner_diameter, material_type):
        if inner_diameter >= outer_diameter:
            raise ValueError("Inner diameter must be smaller than outer diameter")
        
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter

        super().__init__(length, material_type)

        self.area = (np.pi / 4) * (outer_diameter**2 - inner_diameter**2)
        self.I = (np.pi / 64) * (outer_diameter**4 - inner_diameter**4)
        self.update_mass_and_moments()

        # Half area of the tube cross-section
        A_half = (np.pi / 8) * (outer_diameter**2 - inner_diameter**2)
        # Distance from neutral axis to centroid of half section
        y_bar = (4 / (3 * np.pi)) * (outer_diameter**3 - inner_diameter**3) / (outer_diameter**2 - inner_diameter**2)
        self.Q_max = A_half * y_bar
    
    def bending_stress(self, moment):
        outer_fiber_distance = self.outer_diameter / 2
        return super().bending_stress(moment, outer_fiber_distance)

    def transverse_shear(self, shear_force):
        wall_thickness = (self.outer_diameter - self.inner_diameter) / 2
        if wall_thickness <= 0:
            raise ValueError("Invalid wall thickness")

        return shear_force * self.Q_max / (self.I * wall_thickness)


class RectangularTube(BaseTube):
    """
    RectangularTube represents a hollow rectangular tube defined by outer width, outer height, and wall thickness.

    Parameters:
    -----------
    length : float
        Length of the tube [m].
    outer_width : float
        Outer width of the tube cross-section [m].
    outer_height : float
        Outer height of the tube cross-section [m].
    thickness : float
        Wall thickness of the tube [m]. Must be less than half of both outer_width and outer_height.
    material_type : Material
        Material type key used to look up material properties.

    Attributes:
    -----------
    area : float
        Cross-sectional area of the hollow rectangular tube [m²].
    I : float
        Area moment of inertia about the axis parallel to the width [m^4].
    mass : float
        Mass of the tube calculated from material density and volume [kg].

    Methods:
    --------
    bending_stress(moment):
        Calculates bending stress at the outer fiber for a given bending moment.
    """
    def __init__(self, length, outer_width, outer_height, thickness, material_type):
        if thickness * 2 >= outer_width:
            raise ValueError("Thickness too large for given outer width")
        if thickness * 2 >= outer_height:
            raise ValueError("Thickness too large for given outer height")

        self.outer_width = outer_width
        self.outer_height = outer_height
        self.thickness = thickness

        inner_width = outer_width - 2 * thickness
        inner_height = outer_height - 2 * thickness

        super().__init__(length, material_type)

        # Cross-sectional area of hollow rectangle
        self.area = (outer_width * outer_height) - (inner_width * inner_height)

        # Moment of inertia (bending about axis parallel to width)
        self.I = (outer_width * outer_height**3 - inner_width * inner_height**3) / 12

        self.Q_max = self.outer_width * self.thickness * ((self.outer_height / 2) - (self.thickness / 2))

        self.update_mass_and_moments()


    def bending_stress(self, moment):
        outer_fiber_distance = self.outer_height / 2
        return super().bending_stress(moment, outer_fiber_distance)
    
    def transverse_shear(self, shear_force):
        if self.thickness <= 0:
            raise ValueError("Invalid thickness")

        return shear_force * self.Q_max / (self.I * self.thickness)
    
