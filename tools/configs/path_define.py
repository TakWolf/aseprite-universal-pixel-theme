from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..', '..').resolve()

ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
STATIC_ASSETS_DIR = ASSETS_DIR.joinpath('static')
THEME_ASSETS_DIR = ASSETS_DIR.joinpath('aseprite-theme')
FONT_ASSETS_DIR = ASSETS_DIR.joinpath('fusion-pixel-font')

CACHE_DIR = PROJECT_ROOT_DIR.joinpath('cache')

BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
DATA_DIR = BUILD_DIR.joinpath('data')
RELEASES_DIR = BUILD_DIR.joinpath('releases')
