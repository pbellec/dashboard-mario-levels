import pandas as pd
import os

# Get the absolute path of the `src` directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
print(SRC_DIR)

# Get the project root (one level above `src/`)
BASE_DIR = os.path.dirname(SRC_DIR)

# Paths
CSV_FILE = os.path.join(BASE_DIR, "inputs/scenes_coordinates_umap.csv")
IMAGE_FOLDER = os.path.join(BASE_DIR, "inputs/images")  # No copying needed!

def load_scene_data():
    """Loads scene metadata from CSV and generates URLs to serve images dynamically."""

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Keep only the relevant columns
    df = df[['scene_ID', 'DR_1', 'DR_2']]

    # Generate image URLs via a custom Flask route
    df['image_url'] = df['scene_ID'].apply(lambda scene: f"/image/{scene}.jpg")

    # Ensure images actually exist
    df = df[df['image_url'].apply(lambda url: os.path.exists(os.path.join(IMAGE_FOLDER, url.replace("/image/", ""))))]

    print(f"✅ Loaded {len(df)} scenes with valid images.")

    return df
