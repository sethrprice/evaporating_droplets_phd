from dash import html
from dash import dcc

intro_tab = dcc.Tab(label='Introduction', value='intro_tab', children=[
            html.Div([
                html.H3('Introduction Tab Content'),
                html.P("This is placeholder text for the introduction tab.")
            ])
        ])

simulation_tab = dcc.Tab(label='Main', value='sim_tab', children=[
            html.Div([
                html.H3('Evaporating Droplet Simulation', style={'textAlign': 'center'}),
                html.Div([dcc.Graph(id='simulation-graph')]),
                html.Div([
                    html.Label('Control Panel: ', style={'margin-top': '20px', 'font-weight': 'bold'}),
                    dcc.Input(
                        id='C_input',
                        type="number",
                        min=0,
                        max=15,
                        placeholder="C parameter",
                        style={'margin-right': '10px'}
                    ),
                    dcc.Input(
                        id='N_input',
                        type='number',
                        min=50,
                        max=200,
                        placeholder="number of points",
                        style={'margin-right': '10px'}
                    ),
                    dcc.Input(
                        id='a_input',
                        type='number',
                        min=1,
                        max=3,
                        placeholder="centre height of droplet",
                        style={'margin-right': '10px'}
                    ),
                    dcc.Input(
                        id='lines_input',
                        type='number',
                        min=2,
                        max=15,
                        placeholder="number of lines to show",
                        style={'margin-right': '10px'}
                    ),
                    dcc.RadioItems(
                        id="choose_geometry",
                        options=[
                            {'label':"2D Square", 'value':False},
                            {'label':"3D Cylindrical", 'value':True}
                        ],
                        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                    ),
                    html.Button('Run Simulation', id='go_button', n_clicks=0, style={'margin-top': '10px'})
                ], style={'margin-top': '20px', 'padding': '20px', 'border': '1px solid #ccc', 'border-radius': '5px'})
            ], style={'padding': '20px'})
        ])

additional_tab =dcc.Tab(label='Additional', value='tab-3', children=[
            html.Div([
                html.H3('Additional Tab Content'),
                html.P("This is placeholder text for the additional tab.")
            ])
        ])

layout = html.Div([
    html.H1("Modelling the Evaporation of a Binary Droplet in a Well"),
    dcc.Tabs(id='tabs', value='tabset', children=[
        intro_tab,
        simulation_tab,
        additional_tab,
    ])
])