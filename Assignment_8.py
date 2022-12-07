from math import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt


theta= 30 * np.pi / 180 # initial angle to radian
v_i  = 100 # m/s
vx_i = v_i * np.cos(theta) # x component of velocity
vy_i = v_i * np.sin(theta) # y component of velocity
x_i  = 0.0
y_i  = 0.0
# time for trajectory 
t_initial  = 0.0
t_final    = 10.0

h    = 0.01 # experimented with multiple h values and settled on this one
g    = 9.81   # acceleration due to gravity m/s^2
C    = 0.47   # coefficient of drag
R    = 0.08   # Radius of ball in meter
rho  = 1.22 # density kg/m^3

# Define function for calculating the values of the differential equations
def f(r, constants):
  x = r[0]
  y = r[1]
  Vx = r[2]
  Vy = r[3]
  fxv = (-1) * constants* Vx * np.sqrt(Vx**2+Vy**2)
  fyv = (-1*g) - constants* Vy * np.sqrt(Vx**2+Vy**2)
  return np.array([Vx, Vy, fxv, fyv])

# Create method to calculate the trajectory of an object of given mass in kg
def cb_trajectory(mass):
  # Create arrays for the timestep values and the equation solutions filled with zeros
  t_points = np.arange(t_initial, t_final + h, h)
  r_points = np.zeros((len(t_points), 4))
  r_points[0,:] = [x_i, y_i, vx_i, vy_i]
  constants = (np.pi * R**2 * rho * C) / (2.0 * mass)

  #Runge-Kutta method 
  for i in range(1, len(t_points)):
    k1 = f(r_points[i-1,:], constants)
    k2 = f(r_points[i-1,:] + (h/2)*k1, constants)
    k3 = f(r_points[i-1,:] + (h/2)*k2, constants)
    k4 = f(r_points[i-1,:] + h*k3, constants)
    if (r_points[i-1,:][0] >= 0) and (r_points[i-1,:][1] >= 0):
      r_points[i, :] = r_points[i-1,:] + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
    else:
      break
  return r_points[:i]

result = cb_trajectory(1) # initial mass in kg
# Plot the y values as a function of x
fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(5, 6))
ax1.plot(result[:, 0], result[:, 1], 'blue',linewidth=1.5)
ax1.set(ylabel='y(m)')
#ax1.set(xlabel='x(m)',ylabel='y(m)')
# ax1.label_outer()
print("The maximum horizontal distance travel by CannonBall:")
print(result[658,0])
ax1.set_title('Cannonball trajectory with air resistance')
mass_one = cb_trajectory(1)
mass_two  = cb_trajectory(2.5)
mass_three= cb_trajectory(5.0)
mass_four= cb_trajectory(10.0)

ax2.plot(mass_one[:, 0], mass_one[:, 1])
ax2.plot(mass_two[:, 0], mass_two[:, 1])
ax2.plot(mass_three[:, 0], mass_three[:, 1])
ax2.plot(mass_four[:, 0], mass_four[:, 1])
ax2.plot()
ax2.set_title('Cannonball trajectory with air resistance by mass')
ax2.set(xlabel='Distance (m)',ylabel='Altitude (m)')
ax2.legend(('1kg', '2.5kg', '5kg', '10kg'))
print('Q8.7(C) Heavier the mass, larger the horizontal distance.')
plt.show()