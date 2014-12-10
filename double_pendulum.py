# Python code found at
# http://matplotlib.org/examples/animation/double_pendulum_animated.html

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

from numpy import sin, cos, arccos, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import matplotlib.ticker as tick
import seaborn as sns
import sys

G = 9.81  # acceleration due to gravity, in m/s^2
L1 = 1.0  # length of pendulum 1 in m
L2 = 1.0  # length of pendulum 2 in m
M1 = 1.0  # mass of pendulum 1 in kg
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


total_time = 30
dt = 0.01
t = np.arange(0.0, total_time, dt)

# th1 and th2 are the initial angles (degrees)
# w1 and w2 are the initial angular velocities (degrees per second)
th1 = 92.25
w1 = 0.0
w2 = 0.0

# This equation will give the th2 for th1 such that end energy = M1G
th2 = arccos(-M1/(M2*L2) - L1/(M2*L2)*cos(th1*pi/180)*(M1+M2))
th2 = th2*180/pi

rad = pi/180
state = np.array([th1, w1, th2, w2])*rad
y = integrate.odeint(derivs, state, t)

x1 = L1 * sin(y[:, 0])
y1 = -L1 * cos(y[:, 0])
x2 = L2 * sin(y[:, 2]) + x1
y2 = -L2 * cos(y[:, 2]) + y1

# plot energy over time
# U = M1 * G * y1 + M2*G*y2
# K1 = .5*M1 * np.power(y[:, 1], 2) + .5*M2 \
       # * (np.power(y[:, 1], 2) + np.power(y[:, 3], 2) + 2 *
          # np.multiply(np.multiply(y[:, 1], y[:, 3]),
          # cos(np.subtract(y[:, 0], y[:, 2]))))
# E = K1+U
# plt.plot(range(len(E)), E, "r-", lw=2)
# ax = plt.gca()
# fmt = tick.ScalarFormatter(useOffset=False)
# fmt.set_scientific(False)
# ax.yaxis.set_major_formatter(fmt)
# plt.xlabel("Time Step")
# plt.ylabel("Total Energy")

# plot energy difference over time
# delta_E = E[1:]-E[:-1]
# plt.plot(range(len(delta_E)), delta_E, "r-", lw=2)
# plt.xlabel("Time Step")
# plt.ylabel("Change in Energy")

# animation
fig = plt.figure()
L = M1+M2
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-L, L), ylim=(-L, L))
ax.grid()

line, = ax.plot([], [], "o-", lw=2)
time_template = "time = %.2fs"
time_text = ax.text(0.05, 0.9, "", transform=ax.transAxes)


def init():
    line.set_data([], [])
    time_text.set_text("")
    return line, time_text


def animate(i):
    thisx = [0, x1[i], x2[i]]
    thisy = [0, y1[i], y2[i]]
    line.set_data(thisx, thisy)
    time_text.set_text(time_template % (i*dt))
    return line, time_text


ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                              interval=25, blit=True, init_func=init)
i = total_time/dt
plt.plot(x1[:i], y1[:i], x2[:i], y2[:i])
plt.show()
