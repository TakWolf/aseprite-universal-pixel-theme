import logging
import os

logging.basicConfig(level=logging.DEBUG)

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

assets_dir = os.path.join(project_root_dir, 'assets')
static_assets_dir = os.path.join(assets_dir, 'static')
theme_assets_dir = os.path.join(assets_dir, 'aseprite-theme')
font_assets_dir = os.path.join(assets_dir, 'fusion-pixel-font')

data_dir = os.path.join(project_root_dir, 'data')

build_dir = os.path.join(project_root_dir, 'build')
cache_dir = os.path.join(build_dir, 'cache')
releases_dir = os.path.join(build_dir, 'releases')
