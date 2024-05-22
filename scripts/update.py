import logging
import os
import zipfile

from scripts import theme_assets_dir, font_assets_dir, cache_dir
from scripts.utils import fs_util, github_api, download_util

logger = logging.getLogger('update')


def _update_aseprite(tag_name: str = None):
    repository_name = 'aseprite/aseprite'

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = os.path.join(theme_assets_dir, 'version.json')
    if os.path.exists(version_file_path):
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update theme to version: '%s'", version_url)

    download_dir = os.path.join(cache_dir, repository_name, tag_name)
    os.makedirs(download_dir, exist_ok=True)

    source_file_path = os.path.join(download_dir, 'source.zip')
    asset_url = f'https://github.com/{repository_name}/archive/{tag_name}.zip'
    if not os.path.exists(source_file_path):
        logger.info("Start download: '%s'", asset_url)
        download_util.download_file(asset_url, source_file_path)
    else:
        logger.info("Already downloaded: '%s'", source_file_path)

    source_unzip_dir = os.path.join(download_dir, f'aseprite-{version}')
    fs_util.delete_dir(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(download_dir)
    logger.info("Unzip: '%s'", source_unzip_dir)

    fs_util.delete_dir(theme_assets_dir)
    os.rename(os.path.join(source_unzip_dir, 'data', 'extensions', 'aseprite-theme'), theme_assets_dir)
    logger.info("Update assets: '%s'", theme_assets_dir)
    fs_util.delete_dir(source_unzip_dir)

    fs_util.write_json({
        'version': version,
        'version_url': version_url,
    }, version_file_path)


def _update_fonts(tag_name: str = None):
    repository_name = 'TakWolf/fusion-pixel-font'
    os.makedirs(font_assets_dir, exist_ok=True)

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = os.path.join(font_assets_dir, 'version.json')
    if os.path.exists(version_file_path):
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update fonts to version: '%s'", version_url)

    download_dir = os.path.join(cache_dir, repository_name, tag_name)
    os.makedirs(download_dir, exist_ok=True)

    for font_size in [8, 10]:
        asset_file_name = f'fusion-pixel-font-{font_size}px-proportional-otf-v{version}.zip'
        asset_file_path = os.path.join(download_dir, asset_file_name)
        asset_url = f'https://github.com/{repository_name}/releases/download/{tag_name}/{asset_file_name}'
        if not os.path.exists(asset_file_path):
            logger.info("Start download: '%s'", asset_url)
            download_util.download_file(asset_url, asset_file_path)
        else:
            logger.info("Already downloaded: '%s'", asset_file_path)

        asset_unzip_dir = asset_file_path.removesuffix('.zip')
        fs_util.delete_dir(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        logger.info("Unzip: '%s'", asset_unzip_dir)

        font_size_dir = os.path.join(font_assets_dir, str(font_size))
        fs_util.delete_dir(font_size_dir)
        os.rename(asset_unzip_dir, font_size_dir)
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
