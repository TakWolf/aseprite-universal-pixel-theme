import shutil

from tools import configs
from tools.configs import path_define
from tools.services import theme_service, publish_service


def main():
    if path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)

    for font_flavor in configs.font_flavors:
        theme_service.make_theme(font_flavor)
        publish_service.make_extension(font_flavor)
    publish_service.make_itchio_readme()


if __name__ == '__main__':
    main()
