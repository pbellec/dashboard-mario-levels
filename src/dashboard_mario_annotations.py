import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import os
from flask import Flask, send_from_directory
from src import load_umap_data

# Load scene data
scene_data = load_umap_data()

# Get base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGE_FOLDER = os.path.join(BASE_DIR, "inputs", "images")

# Flask server
server = Flask(__name__)

@server.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

# Initialize Dash app
app = dash.Dash(__name__, server=server)

# set viewport
x_min, x_max = [scene_data["DR_1"].min(), scene_data["DR_1"].max()]
y_min, y_max = [scene_data["DR_2"].min(), scene_data["DR_2"].max()]
zoom_factor_x = (x_max - x_min) / 30  # Image size scales with x-axis range
zoom_factor_y = (y_max - y_min) / 30  # Image size scales with y-axis range  # Adjust scaling for better visibility  # Adjust scaling factor as needed

# Add images
images = [
    dict(
        source=f"http://127.0.0.1:8050/image/{row['scene_ID']}.jpg",
        x=row["DR_1"],
        y=row["DR_2"],
        xref="x",
        yref="y",
        sizey=zoom_factor_y,
        sizex=zoom_factor_x,  # Adjust scaling
        xanchor="center",
        yanchor="middle",
        layer="above"
    ) for _, row in scene_data.iterrows()
]

# Define layout dictionary
layout_dict = {
    "xaxis": {"range": [x_min, x_max], "visible": True},
    "yaxis": {"range": [y_min, y_max], "visible": True, "scaleanchor": "x"},
    "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "images": images
}

# Define layout
app.layout = html.Div([
    dcc.Graph(
        id="scatter-plot",
        config={"scrollZoom": True},
        style={"width": "100vw", "height": "100vh"},
        figure=go.Figure(layout=layout_dict),
    )
])


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
