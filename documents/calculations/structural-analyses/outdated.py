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
