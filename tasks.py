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
    c.run(f"python src/cluster_scenes.py outputs/clusters.pkl")

@task
def evaluate_model(c):
    """Evaluates the trained model."""
    c.run(f"python {SCRIPT_DIR}/evaluate_model.py")

# ===============================
# 🔹 TASKS: Running the Dashboard
# ===============================

@task(pre=[train_model])
def dashboard(c):
    """Runs the dashboard using the trained model."""
    c.run(f"python {SCRIPT_DIR}/run_dashboard.py")

# ===============================
# 🔹 TASKS: DataLad Integration
# ===============================

@task
def check_status(c):
    """Checks DataLad dataset status."""
    c.run("datalad status")

@task
def push_data(c):
    """Pushes latest changes to a DataLad repository."""
    c.run("datalad push --to origin")

@task
def rerun(c):
    """Re-runs the full workflow using DataLad."""
    c.run("datalad rerun")

# ===============================
# 🔹 TASKS: Utility & Maintenance
# ===============================

@task
def setup_env(c):
    """Sets up the virtual environment and installs dependencies."""
    c.run("pip install -r requirements.txt")

@task
def clean_temp(c):
    """Removes temporary files and cached data."""
    c.run("rm -rf __pycache__ .pytest_cache")

@task
def full_pipeline(c):
    """Runs the full pipeline from data cleaning to dashboard."""
    invoke_pipeline = "invoke clean_data preprocess_data train_model dashboard"
    c.run(f"datalad run -m 'Full pipeline execution' --python \"{invoke_pipeline}\"")
