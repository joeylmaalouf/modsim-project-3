from numpy import sin, cos, pi
import numpy as np
import scipy.integrate as integrate


def pendulum_pos_hits_origin(a1, a2):
    g = 9.81
    l1 = 1.0
    l2 = 1.0
    m1 = 1.0
    m2 = 1.0
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
    state = np.array([a1, a2, 0.0, 0.0])*pi/180
    y = integrate.odeint(derivs, state, t)

    x1 = l1 * sin(y[:, 0])
    y1 = -l1 * cos(y[:, 0])
    x2 = l2 * sin(y[:, 1]) + x1
    y2 = -l2 * cos(y[:, 1]) + y1

    for i in range(len(x1)):
        if (x2[i] == 0) & (y2[i] == 0):
            return True
    return False


for i in range(-180, 180):
    for j in range(-180, 180):
        print(i, j, pendulum_pos_hits_origin(i, j))
