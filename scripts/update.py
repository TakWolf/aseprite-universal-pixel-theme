import logging
import os
import zipfile

import requests

from scripts import assets_dir, cache_dir
from scripts.utils import fs_util

logger = logging.getLogger('update')


def _get_github_releases_latest_tag_name(repository_name: str) -> str:
    url = f'https://api.github.com/repos/{repository_name}/releases/latest'
    response = requests.get(url)
    assert response.ok, url
    return response.json()['tag_name']


def _download_file(url: str, file_path: str):
    response = requests.get(url, stream=True)
    assert response.ok, url
    tmp_file_path = f'{file_path}.download'
    with open(tmp_file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=512):
            if chunk is not None:
                file.write(chunk)
    os.rename(tmp_file_path, file_path)


def _update_aseprite(tag_name: str = None):
    repository_name = 'aseprite/aseprite'
    theme_assets_dir = os.path.join(assets_dir, 'aseprite-theme')

    if tag_name is None:
        tag_name = _get_github_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = f'{theme_assets_dir}.json'
    if os.path.exists(version_file_path):
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update theme to version: '%s'", version_url)

    download_dir = os.path.join(cache_dir, repository_name, tag_name)
    fs_util.make_dir(download_dir)

    source_file_path = os.path.join(download_dir, 'source.zip')
    asset_url = f'https://github.com/{repository_name}/archive/{tag_name}.zip'
    if not os.path.exists(source_file_path):
        logger.info("Start download: '%s'", asset_url)
        _download_file(asset_url, source_file_path)
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
    font_assets_dir = os.path.join(assets_dir, 'fusion-pixel-font')
    fs_util.make_dir(font_assets_dir)

    if tag_name is None:
        tag_name = _get_github_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = f'{font_assets_dir}.json'
    if os.path.exists(version_file_path):
        if version == fs_util.read_json(version_file_path)['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    logger.info("Need update fonts to version: '%s'", version_url)

    download_dir = os.path.join(cache_dir, repository_name, tag_name)
    fs_util.make_dir(download_dir)

    for font_size in [8, 10]:
        asset_file_name = f'fusion-pixel-font-{font_size}px-proportional-otf-v{version}.zip'
        asset_file_path = os.path.join(download_dir, asset_file_name)
        asset_url = f'https://github.com/{repository_name}/releases/download/{tag_name}/{asset_file_name}'
        if not os.path.exists(asset_file_path):
            logger.info("Start download: '%s'", asset_url)
            _download_file(asset_url, asset_file_path)
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
    _update_aseprite('v1.3.5')
    _update_fonts()


if __name__ == '__main__':
    main()
