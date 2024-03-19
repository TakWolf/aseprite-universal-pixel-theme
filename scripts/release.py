import logging
import os
import zipfile

from scripts import build_dir, data_dir
from scripts.utils import fs_util

logger = logging.getLogger('release')


def _make_extension_file():
    package_json_file_path = os.path.join(data_dir, 'package.json')
    package_info = fs_util.read_json(package_json_file_path)
    package_name: str = package_info['name']
    package_version: str = package_info['version']

    extension_file_path = os.path.join(build_dir, f'{package_name}-v{package_version}.aseprite-extension')
    with zipfile.ZipFile(extension_file_path, 'w') as file:
        for file_dir, _, file_names in os.walk(data_dir):
            for file_name in file_names:
                if file_name.startswith('.'):
                    continue
                file_path = os.path.join(file_dir, file_name)
                arc_path = file_path.removeprefix(f'{data_dir}/')
                file.write(file_path, arc_path)
                logger.info("Pack file: '%s'", arc_path)


def main():
    fs_util.delete_dir(build_dir)
    fs_util.make_dir(build_dir)

    _make_extension_file()


if __name__ == '__main__':
    main()
