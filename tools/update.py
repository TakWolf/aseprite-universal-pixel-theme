import logging
import zipfile

from tools import theme_assets_dir, font_assets_dir, cache_dir
from tools.utils import fs_util, github_api, download_util

logger = logging.getLogger(__name__)


def _update_aseprite(tag_name: str | None = None):
    repository_name = 'aseprite/aseprite'

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = theme_assets_dir.joinpath('version.json')
    if version_file_path.exists():
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update theme to version: '%s'", version_url)

    download_dir = cache_dir.joinpath(repository_name, tag_name)
    download_dir.mkdir(parents=True, exist_ok=True)

    source_file_path = download_dir.joinpath('source.zip')
    asset_url = f'https://github.com/{repository_name}/archive/{tag_name}.zip'
    if not source_file_path.exists():
        logger.info("Start download: '%s'", asset_url)
        download_util.download_file(asset_url, source_file_path)
    else:
        logger.info("Already downloaded: '%s'", source_file_path)

    source_unzip_dir = download_dir.joinpath(f'aseprite-{version}')
    fs_util.delete_dir(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(download_dir)
    logger.info("Unzip: '%s'", source_unzip_dir)

    fs_util.delete_dir(theme_assets_dir)
    source_unzip_dir.joinpath('data', 'extensions', 'aseprite-theme').rename(theme_assets_dir)
    logger.info("Update assets: '%s'", theme_assets_dir)
    fs_util.delete_dir(source_unzip_dir)

    fs_util.write_json({
        'version': version,
        'version_url': version_url,
    }, version_file_path)


def _update_fonts(tag_name: str | None = None):
    repository_name = 'TakWolf/fusion-pixel-font'
    font_assets_dir.mkdir(parents=True, exist_ok=True)

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = font_assets_dir.joinpath('version.json')
    if version_file_path.exists():
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update fonts to version: '%s'", version_url)

    download_dir = cache_dir.joinpath(repository_name, tag_name)
    download_dir.mkdir(parents=True, exist_ok=True)

    for font_size in [8, 10]:
        asset_file_name = f'fusion-pixel-font-{font_size}px-proportional-otf-v{version}.zip'
        asset_file_path = download_dir.joinpath(asset_file_name)
        asset_url = f'https://github.com/{repository_name}/releases/download/{tag_name}/{asset_file_name}'
        if not asset_file_path.exists():
            logger.info("Start download: '%s'", asset_url)
            download_util.download_file(asset_url, asset_file_path)
        else:
            logger.info("Already downloaded: '%s'", asset_file_path)

        asset_unzip_dir = asset_file_path.with_suffix('')
        fs_util.delete_dir(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info("Unzip: '%s'", asset_unzip_dir)

        font_size_dir = font_assets_dir.joinpath(str(font_size))
        fs_util.delete_dir(font_size_dir)
        asset_unzip_dir.rename(font_size_dir)
        logger.info("Update assets: '%s'", font_size_dir)

    fs_util.write_json({
        'version': version,
        'version_url': version_url,
    }, version_file_path)


def main():
    _update_aseprite('v1.3.7')
    _update_fonts()


if __name__ == '__main__':
    main()
