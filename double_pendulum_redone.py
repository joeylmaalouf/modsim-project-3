# thanks http://matplotlib.org/examples/animation/double_pendulum_animated.html

from numpy import sin, cos, pi
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

g = 9.81
l1 = 1.0
l2 = 1.0
l3 = l1 + l2
m1 = 2.0
m2 = 2.0
m3 = m1 + m2


def derivs(state, t):
    theta1 = state[0]
    theta2 = state[1]
    omega1 = state[2]
    omega2 = state[3]
    delta = theta2-theta1

    num1 = m2 * l1 * omega1 * omega1 * sin(delta) * cos(delta) \
        + m2 * g * sin(theta2) * cos(delta) \
        + m2 * l2 * omega2 * omega2 * sin(delta) \
        - m3 * g * sin(theta1)
    den1 = m3 * l1 - m2 * l1 * cos(delta) * cos(delta)

    num2 = -m2 * l2 * omega2 * omega2 * sin(delta) * cos(delta) \
        + m3 * g * sin(theta1) * cos(delta) \
        - m3 * l1 * omega1 * omega1 * sin(delta) \
        - m3 * g * sin(theta2)
    den2 = (l2 / l1) * den1

    return [omega1, omega2, num1/den1, num2/den2]

t = np.arange(0.0, 60, 0.05)
state = np.array([90.0, 90.0, 0.0, 0.0])*pi/180
y = integrate.odeint(derivs, state, t)

x1 = l1 * sin(y[:, 0])
y1 = -l1 * cos(y[:, 0])
x2 = l2 * sin(y[:, 1]) + x1
y2 = -l2 * cos(y[:, 1]) + y1

# Energy calculations

U = m1*g*y1 + m2*g*y2
K = m1 / 2 * np.power(y[:, 1], 2) + m2 / 2 \
    * (np.power(y[:, 1], 2) + np.power(y[:, 3], 2) + 2
    * np.multiply(np.multiply(y[:, 1], y[:, 3]),
                  cos(np.subtract(y[:, 0], y[:, 2]))))
E = K+U
delta_E = E[1:]-E[:-1]

# plot energy difference over time:
plt.plot(range(len(delta_E)), delta_E, 'r-', lw=2)


fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-l3, l3), ylim=(-l3, l3))
ax.grid()
line, = ax.plot([], [], 'go-', lw=2)


def init():
    line.set_data([], [])
    return line,


def animate(i):
    line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
    return line,


animation.FuncAnimation(fig, animate, np.arange(1, len(y)),
                        interval=30, blit=True, init_func=init)
plt.show()
