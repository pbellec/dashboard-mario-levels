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

# Define initial viewport
x_min, x_max = scene_data["DR_1"].min(), scene_data["DR_1"].max()
y_min, y_max = scene_data["DR_2"].min(), scene_data["DR_2"].max()

# Create a scatter plot with markers
scatter_plot = go.Figure(
    data=[go.Scatter(
        x=scene_data["DR_1"],
        y=scene_data["DR_2"],
        mode="markers",
        marker=dict(size=5, color="blue"),
        text=scene_data["scene_ID"],
        hoverinfo="text"
    )],
    layout={
        "xaxis": {"range": [x_min, x_max], "visible": True},
        "yaxis": {"range": [y_min, y_max], "visible": True, "scaleanchor": "x"},
        "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)"
    }
)

# Define layout
app.layout = html.Div([
    dcc.Graph(
        id="scatter-plot",
        config={"scrollZoom": True},
        style={"width": "100vw", "height": "100vh"},
        figure=scatter_plot,
    ),
    html.Img(id="hover-image", style={
        "position": "absolute",
        "display": "none",
        "width": "150px",
        "height": "150px",
        "border": "1px solid black",
        "background": "white"
    })
])

# Callback to switch markers to images dynamically
@app.callback(
    Output("hover-image", "src"),
    Output("hover-image", "style"),
    Input("scatter-plot", "hoverData")
)
def update_hover_image(hoverData):
    if hoverData and "points" in hoverData:
        point = hoverData["points"][0]
        scene_id = point["text"]
        img_src = f"http://127.0.0.1:8050/image/{scene_id}.jpg"
        img_style = {
            "position": "absolute",
            "left": f"{point['x']+5}px",
            "top": f"{point['y']+5}px",
            "width": "300px",
            "height": "300px",
            "border": "1px solid black",
            "background": "white",
            "display": "block"
        }
        return img_src, img_style
    return "", {"display": "none"}

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
