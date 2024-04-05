from dash import Dash
from app_files.layout import layout
from app_files.callbacks import get_callbacks
import dash_bootstrap_components as dbc


# Initialise Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = layout

get_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)