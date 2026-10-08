"""
Launcher entry point for the Student Performance & Result Analysis System.
Run using:
    streamlit run app.py
or
    streamlit run main.py
"""
import runpy
import sys
import os

# Ensure current directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Execute main application
app_path = os.path.join(current_dir, "app.py")
runpy.run_path(app_path, run_name="__main__")
