import dash
from app_files.layout import layout
from app_files.callbacks import callback

app = dash.Dash(__name__)

app.layout = layout