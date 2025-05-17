import numpy as np
import params

class Tube:
    def __init__(self, length, outer_diameter, inner_diameter, material_name):
        """
        Initialize a Tube object with geometric and material properties.

        Parameters:
            length (float): Length of the tube in [m].
            outer_diameter (float): Outer diameter of the tube in [m]
            inner_diameter (float): Inner diameter of the tube in [m]
            material_name (str): Key string for material lookup in the materials dictionary.
                                 Must correspond to one of the available materials that can be found in params.py

        Attributes set from material dictionary:
            density (float or None): Density in kg/m³
            yield_strength (float or None): Yield strength in MPa
            young_modulus (float or None): Young's modulus in MPa

        Calculated geometric properties:
            area (float): Cross-sectional area [m²].
            I (float): Second moment of area (moment of inertia) [m⁴].
            mass (float or None): Mass of the tube [kg], calculated if density is known.
        """
        if inner_diameter >= outer_diameter:
            raise ValueError("Inner diameter must be smaller than outer diameter")
        
        self.length = length
        self.outer_diameter = outer_diameter
        self.inner_diameter = inner_diameter

        # Material lookup
        if material_name not in params.materials:
            raise ValueError(f"Material '{material_name}' not found in materials dictionary")
        self.material = params.materials[material_name]

        self.density = self.material.get('density', None)
        self.yield_strength = self.material.get('yield_strength', None)
        self.young_modulus = self.material.get('young_modulus', None)
        
        # Cross-sectional area for hollow circular section
        self.area = (np.pi / 4) * (self.outer_diameter**2 - self.inner_diameter**2)

        # Moment of inertia for hollow circular section
        self.I = (np.pi / 64) * (self.outer_diameter**4 - self.inner_diameter**4)

        if self.density is not None:
            self.mass = self.area * self.length * self.density       
            self.J_center = (1/12) * self.mass * self.length**2
            self.J_end = (1/3) * self.mass * self.length**2
        else:
            self.mass = None

    def axial_stress(self, force):
        return force / self.area  # [Pa]

    def bending_stress(self, moment):
        # Use outer radius for max bending stress
        return moment * (self.outer_diameter / 2) / self.I  # [Pa]

    def beam_deflection(self, force):
        if self.young_modulus is None:
            raise ValueError("Young's modulus is not defined for this material")
        return (force * self.length**3) / (3 * self.young_modulus * self.I)  # [m]

    def von_mises_stress(self, σx, σy, τxy=0):
        return np.sqrt(σx**2 + σy**2 - σx*σy + 3*τxy**2)

    def safety_factor(self, stress):
        if self.yield_strength is None:
            raise ValueError("Yield strength is not defined for this material")
        return self.yield_strength / stress