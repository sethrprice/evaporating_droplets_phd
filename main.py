import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import utils.funcs_3d as dim_funcs


if __name__ == "__main__":

    print("\nstarting computation... \n")

    # set parameters

    #C param
    C = 1

    #domain paramaters
    N = 128
    dx = 1/N
    x = [dx*i for i in range(N+1)]

    #initial condition
    a = .5
    h_init = [1 + a * (1 - (dx*i)**2) for i in range(N)]

    #simulation run time
    T = 2

    #how many lines to show?
    number_of_lines = 10

    # run simulation. We do it twice to make sure we store a good range of values
    # not knowing in advance what the touchdown time will be
    print(f"\ncomputing solution for C = {C}... \n")
    h_sol = dim_funcs.lub_soln(h_init, T, C)
    touchdown_time = h_sol.t[-1]
    h_sol = dim_funcs.lub_soln(h_init, touchdown_time, C, num_sol=number_of_lines)
    h_solutions = h_sol.y.transpose()
    print("\nsolution found \n")

    # plot solution
    print("\nPlotting... \n")

    ##colourmap
    cmap = plt.get_cmap('viridis')
    norm = mcols.Normalize(vmin=0, vmax=number_of_lines)

    #plot
    fig, ax = plt.subplots()
    for i,hs in enumerate(h_solutions):
        colour = cmap(norm(i))
        ax.plot(x, np.append(hs, 1), color=colour)
    plt.show()