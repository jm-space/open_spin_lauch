"""
# Create a white figure
fig, ax = plt.subplots(figsize=(6, 8))
ax.set_axis_off()

# Add multiline text in top-left corner
ax.text(0.01, 0.99, text, fontsize=12, va='top', ha='left', family='monospace')
ax.text(0.5, 0.99, text2, fontsize=12, va='top', ha='left', family='monospace')

plt.tight_layout()
plt.show()


print(f"{t_max:0.2f}|{t_apogee:0.2f}|{x_impact:0.2f}|{y_max:0.2f}")
print(f"{ω_0:0.2f}|{n_0_rps:0.2f}|{n_0_rpm:0.2f}")

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
"""

# Output results
print(f"Axial stress: \t {σ_rod_rocket_tensile:.2f} MPa")
print(f"Bending stress: \t {σ_rod_rocket_bending:.2f} MPa")
print(f"Cantilever beam deflection: \t {δ_rod_rocket_bending:.2f} mm")
print(f"Von Mises stress: \t {σ_rod_rocket:.2f} MPa")
print(f"Safety factor: \t  {safety_rod_rocket:.2f}")

print(f"Axial stress: \t {σ_rod_cw_tensile:.2f} MPa")
print(f"Bending stress: \t {σ_rod_cw_bending:.2f} MPa")
print(f"Cantilever beam deflection: \t{δ_rod_cw_bending:.2f} mm")
print(f"Von Mises stress: \t{σ_rod_cw:.2f} MPa")
print(f"Safety factor: \t{safety_rod_cw:.2f}")
# Adjust layout and display the figure
root = tk.Tk()
root.geometry("1920x1080")
root.title("Structural Analysis")

label = tk.Label(root, text = "Hello World!", font = ('Arial', 18))
label.pack(padx = 20, pady = 20)

textbox = tk.Text(root, height = 1, font = ('Arial', 16))
textbox.pack(padx = 10)

myentry = tk.Entry(root)
myentry.pack()

button = tk.Button(root, text = "Click Me!", font = ('Arial', 18))
button.pack(padx = 10, pady = 10)

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

btn1 = tk.Button(buttonframe, text = "1", font = ('Arial', 18))
btn1.grid(row = 0, column = 0, sticky = tk.W + tk.E)
btn2 = tk.Button(buttonframe, text = "2", font = ('Arial', 18))
btn2.grid(row = 0, column = 1, sticky = tk.W + tk.E)
btn3 = tk.Button(buttonframe, text = "3", font = ('Arial', 18))
btn3.grid(row = 0, column = 2, sticky = tk.W + tk.E)
btn4 = tk.Button(buttonframe, text = "4", font = ('Arial', 18))
btn4.grid(row = 1, column = 0, sticky = tk.W + tk.E)
btn5 = tk.Button(buttonframe, text = "5", font = ('Arial', 18))
btn5.grid(row = 1, column = 1, sticky = tk.W + tk.E)
btn6 = tk.Button(buttonframe, text = "6", font = ('Arial', 18))
btn6.grid(row = 1, column = 2, sticky = tk.W + tk.E)


buttonframe.pack(fill = tk.X)

anotherbtn = tk.Button(root, text = "Test")
anotherbtn.place(x = 200, y = 100, height = 100, width = 100)

# === Main container frame ===
main_frame = tk.Frame(root)
main_frame.pack(padx=50, pady=50)

# === Text Section (LEFT) ===
text_frame = tk.Frame(main_frame)
tk.Label(text_frame, text = "Hello")
text_frame.pack()

# === Plot Section (RIGHT) ===
plot_frame = tk.Frame(main_frame)
plot_frame.pack(side="right")

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.get_tk_widget().pack()

# === Run main loop ===
root.mainloop()


"""
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
"""

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