import pandas as pd
import os

# Get the absolute path of the `src` directory
SRC_DIR = os.path.dirname(os.path.abspath(__file__))

# Get the project root (one level above `src/`)
BASE_DIR = os.path.dirname(SRC_DIR)

# Paths
CSV_FILE = os.path.join(BASE_DIR, "inputs/scenes_coordinates_umap.csv")
IMAGE_FOLDER = os.path.join(BASE_DIR, "inputs/images")  # No copying needed!

def load_umap_data(full_path=False):
    """Loads scene metadata from CSV and generates URLs to serve images dynamically."""

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Keep only the relevant columns
    df = df[['scene_ID', 'DR_1', 'DR_2']]

    # Generate image URLs via a custom Flask route
    if full_path:
        df['image_url'] = df['scene_ID'].apply(lambda scene: os.path.join(IMAGE_FOLDER, f"{scene}.jpg"))
    else:
        df['image_url'] = df['scene_ID'].apply(lambda scene: f"/image/{scene}.jpg")
        # Ensure images actually exist
        df = df[df['image_url'].apply(lambda url: os.path.exists(os.path.join(IMAGE_FOLDER, url.replace("/image/", ""))))]

    print(f"✅ Loaded {len(df)} scenes with valid images.")

    return df

def load_annotation_data():
    """Loads scene annotations from CSV."""

    # Load CSV
    df = pd.read_csv(CSV_FILE)

    # Drop UMAP columns (`DR_1` and `DR_2`)
    df = df.drop(columns=["DR_1", "DR_2"], errors="ignore")

    print(f"✅ Loaded {len(df)}.")

    return df
