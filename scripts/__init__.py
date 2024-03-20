import logging
import os

logging.basicConfig(level=logging.DEBUG)

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
assets_dir = os.path.join(project_root_dir, 'assets')
data_dir = os.path.join(project_root_dir, 'data')
build_dir = os.path.join(project_root_dir, 'build')
cache_dir = os.path.join(build_dir, 'cache')
