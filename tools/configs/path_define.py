from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..', '..').resolve()

assets_dir = project_root_dir.joinpath('assets')
static_assets_dir = assets_dir.joinpath('static')
theme_assets_dir = assets_dir.joinpath('aseprite-theme')
font_assets_dir = assets_dir.joinpath('fusion-pixel-font')

cache_dir = project_root_dir.joinpath('cache')

build_dir = project_root_dir.joinpath('build')
data_dir = build_dir.joinpath('data')
releases_dir = build_dir.joinpath('releases')
