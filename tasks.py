from invoke import task


# ===============================
# 🔹 TASKS: Data Processing
# ===============================

@task
def clean_data(c):
    """Cleans the raw data and saves the cleaned version."""
    c.run(f"python {SCRIPT_DIR}/clean_data.py")

@task(pre=[clean_data])
def preprocess_data(c):
    """Preprocesses data for training."""
    c.run(f"python {SCRIPT_DIR}/preprocess_data.py")

# ===============================
# 🔹 TASKS: Model Training
# ===============================

@task
def cluster_scenes(c):
    """Hierarchical clustering on scenes based on annotations."""
    c.run(f"python src/cluster_scenes.py outputs/clusters.pkl --n_clusters $(seq 5 30)")


# ===============================
# 🔹 TASKS: Running the Dashboard
# ===============================

@task(pre=[cluster_scenes])
def dashboard(c):
    """Runs the dashboard using the trained model."""
    c.run(f"python {SCRIPT_DIR}/run_dashboard.py")

# ===============================
# 🔹 TASKS: Utility & Maintenance
# ===============================

@task
def setup_env(c):
    """Sets up the virtual environment and installs dependencies."""
    c.run("pip install -r requirements.txt")
    c.run("pip install -e .")

@task
def clean_outputs(c):
    """Removes temporary files and cached data."""
    c.run("rm -rf outputs/*")

@task
def full_pipeline(c):
    """Runs the full pipeline from data cleaning to dashboard."""
    invoke_pipeline = "invoke clean_data preprocess_data train_model dashboard"
    c.run(f"datalad run -m 'Full pipeline execution' --python \"{invoke_pipeline}\"")
