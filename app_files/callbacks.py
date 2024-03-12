from dash import Input, Output, State, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcols
import utils.funcs_3d as funcs_3d
import utils.funcs_2d as funcs_2d


def get_callbacks(app):


    @app.callback(
        Output('simulation-graph', 'figure'),
        Input('go_button', 'n_clicks'),
        State('C_input', 'value'),
        State('N_input', 'value'),
        State('a_input', 'value'),
        State('lines_input', 'value'),
        State('choose_geometry', 'value'),
        prevent_initial_call=True
    )
    def simulate_evaporation(nclicks, CC, NN, aa, n_lines, geom):
        if nclicks > 0:

            # Set up domain
            dr = 1/NN
            T = 2

            # Initialise droplet
            aa2 = aa - 1
            h_init = [1 + aa2 * (1 - (dr * i) ** 2) for i in range(NN)]

            # Run simulation
            if geom:
                h_sol = funcs_3d.lub_soln(h_init, T, CC, num_sol=n_lines)
            else:
                h_sol = funcs_2d.lub_soln(h_init, T, CC, num_sol=n_lines)

            touchdown_time = h_sol.t_events[0][0]

            if geom:
                h_sol = funcs_3d.lub_soln(h_init, touchdown_time * 0.99, CC, num_sol=n_lines)
            else:
                h_sol = funcs_2d.lub_soln(h_init, touchdown_time * 0.99, CC, num_sol=n_lines)

            # Add the pin to the solutions
            h_solutions = np.array([np.append(h_profile, 1) for h_profile in h_sol.y.transpose()])
            times = h_sol.t

            # get data into dataframe
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html

            # get entries for df
            h_vals = h_solutions.flatten()
            r_vals = np.array([[dr * i % (NN + 1) for i in range((NN + 1))] for k in range(len(h_solutions))]).flatten()
            t_vals = np.repeat(times, NN + 1).round(3)

            # create df
            d = {'r':r_vals, 'h':h_vals, 't':t_vals}
            df = pd.DataFrame(data=d)
            df['t'] = df['t'].astype('float')

            # colourmap
            cmap = plt.get_cmap('viridis')
            hex_cols = [mcols.rgb2hex(c) for c in cmap.colors]
            colour_map = {tt: hex_cols[int(i / len(t_vals) * len(hex_cols)) - 1] for i, tt in enumerate(t_vals)}

            # plot this using plotly express
            # https://plotly.com/python/line-charts/
            fig = px.line(df, x='r', y='h', color='t',
                          color_discrete_map=colour_map)
            return fig

        else:
            # If the button has not been clicked, return an empty graph
            return {
                'data': [],
                'layout': {}
            }
