import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

project_root_dir = Path(__file__).parent.joinpath('..').resolve()

assets_dir = project_root_dir.joinpath('assets')
static_assets_dir = assets_dir.joinpath('static')
theme_assets_dir = assets_dir.joinpath('aseprite-theme')
font_assets_dir = assets_dir.joinpath('fusion-pixel-font')

data_dir = project_root_dir.joinpath('data')

build_dir = project_root_dir.joinpath('build')
cache_dir = build_dir.joinpath('cache')
releases_dir = build_dir.joinpath('releases')
