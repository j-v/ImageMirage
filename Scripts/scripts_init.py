import sys
import os

# Add parent directory to path, to allow script's access to ColorZoner modules
abs_path = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.join(abs_path, os.path.pardir)
sys.path.insert(0, parent_dir)

proj_dir = parent_dir
