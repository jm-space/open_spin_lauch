import numpy as np

def axial_stress(F, A):
    """
    Calculate normal stress from axial loading.
    σ = F / A

    Parameters:
        F (float): Axial force [N]
        A (float): Cross-sectional area [mm²]

    Returns:
        float: Axial stress [MPa]
    """
    return F / A

def bending_stress(M, y, I):
    """
    Calculate bending stress.
    σ = M * y / I

    Parameters:
        M (float): Bending moment [Nm]
        y (float): Distance from neutral axis [mm]
        I (float): Moment of inertia [mm⁴]

    Returns:
        float: Bending stress [MPa]
    """
    return M *1e3 * y / I

def cantilever_beam_deflection(F, L, E, I):
    """
    Calculate maximum deflection for a cantilever beam with an fixed and an open end. Load positioned at the open end point. 
    δ = F * L³ / (3 * E * I)

    Parameters:
        F (float): End point load [N]
        L (float): Beam length [mm]
        E (float): Young's modulus [MPa]
        I (float): Moment of inertia [mm⁴]

    Returns:
        float: Maximum deflection [mm]
    """
    return (F * L**3) / (3 * E * I)

def von_mises_stress(σx, σy, τxy):
    """
    Calculate von Mises stress under plane stress conditions.
    σ_vm = sqrt(σx² - σx*σy + σy² + 3*τxy²)

    Parameters:
        σx (float): Normal stress in x-direction [MPa]
        σy (float): Normal stress in y-direction [MPa]
        τxy (float): Shear stress [MPa]

    Returns:
        float: von Mises stress [MPa]
    """
    return np.sqrt(σx**2 - σx*σy + σy**2 + 3*τxy**2)