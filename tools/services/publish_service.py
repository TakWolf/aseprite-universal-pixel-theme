import json
import zipfile

import markdown

from tools.configs import path_define, FontFlavor


def make_extension(font_flavor: FontFlavor):
    data_dir = path_define.data_dir.joinpath(font_flavor)

    package_json_file_path = data_dir.joinpath('package.json')
    package_info = json.loads(package_json_file_path.read_bytes())
    package_name = package_info['name']
    package_version = package_info['version']

    path_define.releases_dir.mkdir(parents=True, exist_ok=True)
    extension_file_path = path_define.releases_dir.joinpath(f'{package_name}-{font_flavor}-v{package_version}.aseprite-extension')
    with zipfile.ZipFile(extension_file_path, 'w') as file:
        for file_dir, _, file_names in data_dir.walk():
            for file_name in file_names:
                if file_name.startswith('.'):
                    continue
                file_path = file_dir.joinpath(file_name)
                arc_path = file_path.relative_to(data_dir)
                file.write(file_path, arc_path)
    print(f"Make extension: '{extension_file_path}'")


def make_itchio_readme():
    md_file_path = path_define.project_root_dir.joinpath('README.md')
    md_text = md_file_path.read_text('utf-8')
    md_text = md_text.replace('](docs/', '](https://raw.githubusercontent.com/TakWolf/aseprite-universal-pixel-theme/master/docs/')
    html = markdown.markdown(md_text)
    path_define.releases_dir.mkdir(parents=True, exist_ok=True)
    html_file_path = path_define.releases_dir.joinpath('itchio-readme.html')
    html_file_path.write_text(f'{html}\n', 'utf-8')
    print(f"Make itch.io readme: '{html_file_path}'")
