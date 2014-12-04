# Python code found at
# http://matplotlib.org/examples/animation/double_pendulum_animated.html

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from numpy import sin, cos, pi, arcsin, arccos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import seaborn as sns
import sys

G = 9.8   # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 2.0  # mass of pendulum 1 in kg
M2 = 1.0  # mass of pendulum 2 in kg


def derivs(state, t):

    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    del_ = state[2]-state[0]
    den1 = (M1+M2)*L1 - M2*L1*cos(del_)*cos(del_)
    dydx[1] = (M2*L1*state[1]*state[1]*sin(del_)*cos(del_)
               + M2*G*sin(state[2])*cos(del_)+M2*L2*state[3]*state[3]*sin(del_)
               - (M1+M2)*G*sin(state[0]))/den1

    dydx[2] = state[3]

    den2 = (L2/L1)*den1
    dydx[3] = (-M2*L2*state[3]*state[3]*sin(del_)*cos(del_)
               + (M1+M2)*G*sin(state[0])*cos(del_)
               - (M1+M2)*L1*state[1]*state[1]*sin(del_)
               - (M1+M2)*G*sin(state[2]))/den2

    return dydx

# create a time array from 0..20 sampled at 0.05 second steps
dt = 0.01
t = np.arange(0.0, 20, dt)

# th1 and th2 are the initial angles (degrees)
# w1 and w2 are the initial angular velocities (degrees per second)
th1 = 90.0
w1 = 0.0
#th2 = 0.0

# This equation will give all th2 for th1 such that end energy = M1G
print cos( th1*pi/180)
print (M1/(M2*L2) + L1/L2 * cos( th1*pi/180 )*(1-M1/M2))/ (2*pi)
th2 = arccos( (M1/(M2*L2) + L1/L2 * cos( th1*pi/180 )*(1-M1/M2)) /( 2*pi) )
th2 = th2*180/pi
print th2
w2 = 0.0

rad = pi/180

# initial state
state = np.array([th1, w1, th2, w2])*pi/180.

# integrate your ODE using scipy.integrate.
y = integrate.odeint(derivs, state, t)

x1 = L1 * sin(y[:, 0])
y1 = -L1 * cos(y[:, 0])

x2 = L2 * sin(y[:, 2]) + x1
y2 = -L2 * cos(y[:, 2]) + y1

# Energy calculations

U = M1 * G * y1 + M2*G*y2
K1 = .5* M1 * np.power(y[:,1],2) +  .5*M2 * ( np.power(y[:,1],2) + np.power(y[:,3],2) +2 * np.multiply( np.multiply(y[:,1], y[:,3]) , cos( np.subtract(y[:,0], y[:,2]) ) ) )
E = K1+U
delta_E = E[1:]-E[:-1]

# Uncomment following lines to plot energy difference over time:
plt.figure()
plt.plot(range(len(delta_E)),delta_E,'r-',lw=2)


# Plotting animation

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-2, 2), ylim=(-2, 2))
ax.grid()

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=55, blit=True, init_func=init)

#ani.save('double_pendulum.mp4', fps=15)
plt.show()