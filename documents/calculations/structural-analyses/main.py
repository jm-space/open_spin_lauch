import params as params
import numpy as np

v_0 = 97.76 #m/s
v_0x = v_0 * np.sin(np.deg2rad(params.θ_release))
v_0y = v_0 * np.cos(np.deg2rad(params.θ_release))

v_x = np.array([v_0x])
v_y = np.array([v_0y])

time = np.array([0])
F_d = np.array([])

F_x = np.array([])
a_x = np.array([])
dv_x = np.array([])
d_x = np.array([])

F_y = np.array([])
a_y = np.array([])
dv_y = np.array([])
d_y = np.array([])

print(v_x)
print(v_y) 

for i in range(100):
    v = np.sqrt((v_x[i]**2 + v_y[i]**2))
    time = np.append(time, time[i] + params.dt)
    F_d = np.append(F_d, 1/2*params.cd_rocket*params.ρ_air*params.A_rocket*v**2/10**6)
    F_x = np.append(F_x, -F_d[i]*v_x[i]/v)
    a_x = np.append(a_x, F_x[i]/params.m_rocket)
    dv_x = np.append(dv_x, a_x[i]*params.dt)
    d_x = np.append(d_x, params.dt*(v_x[i] + dv_x[i]/2))
    v_x = np.append(v_x, v_x[i] + dv_x[i])

    F_y = np.append(F_y, -params.m_rocket*params.g-F_d[i]*v_y[i]/v)
    a_y = np.append(a_y, F_y[i]/params.m_rocket)
    dv_y = np.append(dv_y, a_y[i]*params.dt)
    d_y = np.append(d_y, params.dt*(v_y[i] + dv_y[i]/2))
    v_y = np.append(v_y, v_y[i] + dv_y[i])
    print(f"{time[i]:.02f}|{F_d[i]:.02f}|{F_x[i]:.02f}|{a_x[i]:.02f}|{dv_x[i]:.04f}|{d_x[i]:.04f}|{v_x[i]:.02f}")
