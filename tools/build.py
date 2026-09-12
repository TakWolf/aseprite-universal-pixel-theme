import shutil

from tools.configs import path_define, options
from tools.services import theme_service, publish_service


def main() -> None:
    if path_define.BUILD_DIR.exists():
        shutil.rmtree(path_define.BUILD_DIR)

    for font_flavor in options.FONT_FLAVORS:
        theme_service.make_theme(font_flavor)
        publish_service.make_extension(font_flavor)
    publish_service.make_itchio_readme()


if __name__ == '__main__':
    main()
