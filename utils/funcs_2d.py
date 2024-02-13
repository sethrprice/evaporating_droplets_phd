import numpy as np
from scipy.integrate import solve_ivp

# finite differences are computed using a convolution with a gaussian kernel
# these are the kernels corresponding to certain finite differences (fds)
fds = {'p1': [0,1,1,0,0],
       'm1': [0,0,1,1,0],
       'd3+': [1,-3,3,-1,0], 
       'd3-': [0,1,-3,3,-1]}


def lub_g_2d(h, plus):

    '''this finds 2D g, part of the 2D lubrication equation'''

    # convert h to numpy array
    h = np.array(h)

    # find the step size
    dx = 1/(len(h))

    # choose the plus or minus gaussian kernels for the convolution
    if plus:
        d3 = fds['d3+']
        pm = fds['p1']
    else:
        d3 = fds['d3-']
        pm = fds['m1']

    # add boundary conditions for h
    # think these need to be numpy array operations bcos of np.linspace
    h = np.insert(h, 0, [h[2], h[1]]) #symmetry across centre
    h = np.append(h, [1, 3 - 3*h[-1] + h[-2]]) #pinned contact line and symmetry

    # compute g
    g = (np.convolve(h, pm, 'valid')/(2*dx))**3 * np.convolve(h, d3, 'valid')

    return g


def lub_eq_2d(t, h, C):

    '''The lubrication equation in 2D for a droplet in a well'''

    dx = 1/len(h)

    dhdt = -1 - C/3 * 1/dx * (lub_g_2d(h, True) - lub_g_2d(h, False))

    return dhdt


def touch_floor(t, h, C):

    '''Termination condition of the integration -- when the droplet touches down.'''

    if min(h) < 0.001:
        return 0
    else:
        return 1

    return min(h)

touch_floor.terminal = True

def lub_soln_2d(h0, t, C, solver='LSODA'):

    '''Use solve_ivp to solve the lubrication equation on a two dimensional domain'''

    sol = solve_ivp(lub_eq_2d, [0,t], h0, args = (C,), method=solver, events=touch_floor, t_eval=np.linspace(0,t,10))

    return sol



