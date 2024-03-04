import numpy as np
from scipy.integrate import solve_ivp
import functools

# set the default argument of convolve to be mode=valid
np.convolve = functools.partial(np.convolve, mode = 'valid')

fds = {'p+': [0,1,1,0,0],
       'p-': [0,0,1,1,0],
       'd3+': [1,-3,3,-1,0], 
       'd3-': [0,1,-3,3,-1], 
       'd2+': [1,-1,-1,1,0], 
       'd2-': [0, 1,-1,-1,1], 
       'd1+': [0,1,-1,0,0], 
       'd1-': [0,0,1,-1,0]}

def h_index(h):

    index_of_h = np.array([i for i, hi in enumerate(h)])

    index_of_h = index_of_h[1:]

    return index_of_h


def laplace_g(h, X, plus):

    '''This finds 3D g, part of the 3D lubrication equation'''

    # get discretisation
    dr = 1/len(h)

    # get different sides of the finite difference
    if plus:
        add_string = '+'
    else:
        add_string = '-'

    d3 = fds['d3' + add_string]
    d2 = fds['d2' + add_string]
    d1 = fds['d1' + add_string]
    pm = fds['p' + add_string]

    # get the index of each h value and determine whether we're adding or subtracting 0.5
    hi = h_index(h)
    half_add = 0.5 * (-1)**(plus + 1)

    # boundary conditions. We withold the -2 ghost point to prevent evaluation at r = 0
    h = np.insert(h, 0, h[1]) #symmetry across centre

    # get the N+1 ghost point
    hNp1 = (3 * (1 + 2/3 * dr + dr**2) - h[-1] * (3 + dr + 2*dr**2 + 3/4*dr**3) + h[-2])/(1 + dr + dr**2 - 3/4 * dr**3)
    h = np.append(h, [1, hNp1]) 

    # g runs from 1 to N-1
    g = (hi + half_add) * (np.convolve(h, pm)/ (2 * dr))**3 *\
          (np.convolve(h, d3) + \
           (1/(2 * (hi + half_add))) * np.convolve(h, d2) - \
            (1/(hi + half_add))**2 * np.convolve(h, d1))

    return g 


def marangoni_g(h, X, plus):


    # get discretisation
    dr = 1/len(h)

    # get different sides of the finite difference
    if plus:
        add_string = '+'
    else:
        add_string = '-'

    d1 = fds['d1' + add_string]
    pm = fds['p' + add_string]

    # get the index of each h value and determine whether we're adding or subtracting 0.5
    hi = h_index(h)
    half_add = 0.5 * (-1)**(plus + 1)

    g = (hi + half_add) * (np.convolve(h, pm)/2)**2 * np.convolve(X, d1)

    return g


def lub_eq(t, h, X, C, alpha, beta, epsilon=1/75):

    dr = 1/len(h)

    M = - beta * C/epsilon**2

    # get the index of each h value
    hi = h_index(h)

    # do dh/dt at r = 0 separately 
    dh0dt = - 16/9 * C*h[0]**3/dr**4 * (h[2] - 4 * h[1] + 3* h[0]) - 1

    dhdt = - C * 1/(3 * hi * dr) * (laplace_g(h, True) - laplace_g(h, False)) - \
        M/(8 * hi * (dr)**2) * (marangoni_g(h, X, True) - marangoni_g(h, X, False)) - \
            (1 - alpha * X)/np.sqrt(1 - (hi * dr)**2)

    dhdt = np.insert(dhdt, 0, dh0dt)

    return dhdt

def touch_floor(t, h, X, C, alpha, beta, epsilon):

    '''Termination condition of the integration -- when the droplet touches down.'''

    if min(h) < 0.001:
        return 0
    else:
        return 1
    
touch_floor.terminal = True