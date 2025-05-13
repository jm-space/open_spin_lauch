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