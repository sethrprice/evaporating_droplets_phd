from dash import Dash
from app_files.layout import layout
from app_files.callbacks import get_callbacks


# Initialise Dash app
app = Dash(__name__)

app.layout = layout

get_callbacks(app)


if __name__ == '__main__':
    app.run(debug=True)