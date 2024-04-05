from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from .layout_components import C_input, N_input, a_input, n_lines_input, geometry, go_button

#https://dash-bootstrap-components.opensource.faculty.ai/

introduction = "In January of 2023 I passed my PhD viva. A year later I revisited the project, and I decided to create a small " \
                "simulation app so that other people could run the same simulations I did. I have moved the model from Mathematica to Python in an effort to be more " \
                "reproducible and open source, and have used Dash to create a user-friendly app that lets users build and " \
                "run simulations of evaporating droplets.\n It's not finished yet, it currently only runs pure droplet " \
                "simulations and isn't very scalable to large values of N. I plan to add Marangoni effects, a vapour phase " \
                "model, and to improve the simulation algorithm. I'll also add other dashboard features, like the ability to " \
                "download the output simulation data."

intro_tab = dcc.Tab(label='Introduction', value='intro_tab', children=[
            html.Div([
                html.H4(introduction)
            ])
        ])


controls = dbc.Card([
    html.Div([
        html.Br(),
        C_input,
        html.Br(),
        N_input,
        html.Br(),
        html.P("select height at centre"),
        a_input,
        html.Br(),
        n_lines_input,
        html.Br(),
        geometry,
        html.Br(),
        go_button
    ])
])


simulation_intro_text = "Here you can run a simulation of a pure droplet evaporating from a well until touchdown. The control panel below " \
                        "lets you choose values of C, N (number of points), a (initial height at centre), and num_lines, " \
                        "and also select the geometry you would like -- 2D square or 3D cylindrical.\n" \
                        "I'll add the lubrication equation here once I figure out how to get latex on the app. I'm also going to make it "\
                        "easier to determine C by picking viscosity, surface tension, evaporation rate, and aspect ratio directly."
                   

simulation_tab = dcc.Tab(
    label='Simulation',
    value='sim_tab',
    children=[
        html.Div([
            html.H2('Evaporating Droplet Simulation', style={'textAlign': 'center'}),
            html.P(simulation_intro_text),
            dbc.Row([
                dbc.Col(controls, md = 2),
                dbc.Col(html.Div([dcc.Graph(id='simulation-graph')]), md = 10)
            ])
        ])
    ]
)

additional_tab =dcc.Tab(label='Additional', value='tab-3', children=[
            html.Div([
                html.H3('Additional Tab Content'),
                html.P("This is placeholder text for the additional tab.")
            ])
        ])

layout = html.Div([
    html.H1("Modelling the Evaporation of a Binary Droplet in a Well"),
    dcc.Tabs(id='tabs', value='intro_tab', children=[
        intro_tab,
        simulation_tab,
        additional_tab,
    ])
])