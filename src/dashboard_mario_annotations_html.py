from flask import Flask, send_from_directory, jsonify, render_template
import pandas as pd
import os
from src import load_umap_data

# Load scene data
scene_data = load_umap_data()

# Get base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMAGE_FOLDER = os.path.join(BASE_DIR, "inputs", "images")

# Flask server
app = Flask(__name__)

@app.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route("/get_scenes")
def get_scenes():
    return jsonify(scene_data.to_dict("records"))

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=8050)
