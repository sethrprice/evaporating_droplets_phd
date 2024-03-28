import dash_bootstrap_components as dbc
from dash import dcc


C_input = dbc.Input(
    id='C_input',
    type="number",
    min=0,
    max=15,
    placeholder="C parameter"
)

N_input = dbc.Input(
    id='N_input',
    type='number',
    min=1,
    max=200,
    placeholder="number of points"
)

a_input = dcc.Slider(
    id='a_input',
    min=1,
    max=3,
    step = 0.1, 
    value = 1.5, 
    marks={1:'1', 1.5:'1.5', 2:'2', 2.5:'2.5', 3:'3'}, 
    tooltip={"placement": "bottom", "always_visible": True}
)

n_lines_input = dbc.Input(
    id='lines_input',
    type='number',
    min=2,
    max=15,
    placeholder="number of lines to show"
)


geometry = dbc.RadioItems(
    id="choose_geometry",
    options=[
        {'label':"2D Square", 'value':False},
        {'label':"3D Cylindrical", 'value':True}
    ]
)


go_button = dbc.Button('Run Simulation', id='go_button', n_clicks=0)