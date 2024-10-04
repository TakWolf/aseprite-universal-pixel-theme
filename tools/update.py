import json
import shutil
import zipfile

from tools import theme_assets_dir, font_assets_dir, cache_dir
from tools.utils import github_api, download_util


def _update_aseprite(tag_name: str | None = None):
    repository_name = 'aseprite/aseprite'

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = theme_assets_dir.joinpath('version.json')
    if version_file_path.exists():
        if version == json.loads(version_file_path.read_bytes())['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    print(f"Need update theme to version: '{version_url}'")

    download_dir = cache_dir.joinpath(repository_name, tag_name)
    download_dir.mkdir(parents=True, exist_ok=True)

    source_file_path = download_dir.joinpath('source.zip')
    asset_url = f'https://github.com/{repository_name}/archive/{tag_name}.zip'
    if not source_file_path.exists():
        print(f"Start download: '{asset_url}'")
        download_util.download_file(asset_url, source_file_path)
    else:
        print(f"Already downloaded: '{source_file_path}'")

    source_unzip_dir = download_dir.joinpath(f'aseprite-{version}')
    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)
    with zipfile.ZipFile(source_file_path) as file:
        file.extractall(download_dir)
    print(f"Unzip: '{source_unzip_dir}'")

    if theme_assets_dir.exists():
        shutil.rmtree(theme_assets_dir)
    source_unzip_dir.joinpath('data', 'extensions', 'aseprite-theme').rename(theme_assets_dir)
    print(f"Update assets: '{theme_assets_dir}'")
    if source_unzip_dir.exists():
        shutil.rmtree(source_unzip_dir)

    version_file_path.write_text(f'{json.dumps({
        'version': version,
        'version_url': version_url,
    }, indent=2, ensure_ascii=False)}\n', 'utf-8')


def _update_fonts(tag_name: str | None = None):
    repository_name = 'TakWolf/fusion-pixel-font'
    font_assets_dir.mkdir(parents=True, exist_ok=True)

    if tag_name is None:
        tag_name = github_api.get_releases_latest_tag_name(repository_name)
    version = tag_name.removeprefix('v')

    version_file_path = font_assets_dir.joinpath('version.json')
    if version_file_path.exists():
        if version == json.loads(version_file_path.read_bytes())['version']:
            return
    version_url = f'https://github.com/{repository_name}/releases/tag/{tag_name}'
    print(f"Need update fonts to version: '{version_url}'")

    download_dir = cache_dir.joinpath(repository_name, tag_name)
    download_dir.mkdir(parents=True, exist_ok=True)

    for font_size in [8, 10]:
        asset_file_name = f'fusion-pixel-font-{font_size}px-proportional-otf-v{version}.zip'
        asset_file_path = download_dir.joinpath(asset_file_name)
        asset_url = f'https://github.com/{repository_name}/releases/download/{tag_name}/{asset_file_name}'
        if not asset_file_path.exists():
            print(f"Start download: '{asset_url}'")
            download_util.download_file(asset_url, asset_file_path)
        else:
            print(f"Already downloaded: '{asset_file_path}'")

        asset_unzip_dir = asset_file_path.with_suffix('')
        if asset_unzip_dir.exists():
            shutil.rmtree(asset_unzip_dir)
        with zipfile.ZipFile(asset_file_path) as file:
            file.extractall(asset_unzip_dir)
        print(f"Unzip: '{asset_unzip_dir}'")

        font_size_dir = font_assets_dir.joinpath(str(font_size))
        if font_size_dir.exists():
            shutil.rmtree(font_size_dir)
        asset_unzip_dir.rename(font_size_dir)
        print(f"Update assets: '{font_size_dir}'")

    version_file_path.write_text(f'{json.dumps({
        'version': version,
        'version_url': version_url,
    }, indent=2, ensure_ascii=False)}\n', 'utf-8')


def main():
    _update_aseprite('v1.3.9.1')
    _update_fonts()


if __name__ == '__main__':
    main()
