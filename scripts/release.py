import logging
import zipfile

import markdown

from scripts import project_root_dir, data_dir, releases_dir
from scripts.utils import fs_util

logger = logging.getLogger('release')


def _make_extension_file():
    package_json_file_path = data_dir.joinpath('package.json')
    package_info = fs_util.read_json(package_json_file_path)
    package_name = package_info['name']
    package_version = package_info['version']

    extension_file_path = releases_dir.joinpath(f'{package_name}-v{package_version}.aseprite-extension')
    with zipfile.ZipFile(extension_file_path, 'w') as file:
        for file_dir, _, file_names in data_dir.walk():
            for file_name in file_names:
                if file_name.startswith('.'):
                    continue
                file_path = file_dir.joinpath(file_name)
                arc_path = file_path.relative_to(data_dir)
                file.write(file_path, arc_path)
                logger.info("Pack file: '%s'", arc_path)


def _make_itchio_readme():
    md_file_path = project_root_dir.joinpath('README.md')
    md_text = md_file_path.read_text('utf-8')
    md_text = md_text.replace('](docs/', '](https://raw.githubusercontent.com/TakWolf/aseprite-universal-pixel-theme/master/docs/')
    html = markdown.markdown(md_text)
    html_file_path = releases_dir.joinpath('itchio-readme.html')
    html_file_path.write_text(f'{html}\n', 'utf-8')


def main():
    fs_util.delete_dir(releases_dir)
    releases_dir.mkdir(parents=True)

    _make_extension_file()
    _make_itchio_readme()


if __name__ == '__main__':
    main()
