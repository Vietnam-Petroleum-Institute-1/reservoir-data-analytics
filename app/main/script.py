"""
Import libraries for load file and warnings notifical
"""

import dotenv
import os
import warnings
warnings.filterwarnings('ignore')

"""
Import env
"""

project_dir = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
dotenv_path = os.path.join(project_dir, '.env')
dotenv.load_dotenv(dotenv_path)