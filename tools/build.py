import shutil

from tools.config import paths, options
from tools.services import theme_service, publish_service


def main() -> None:
    if paths.BUILD_DIR.exists():
        shutil.rmtree(paths.BUILD_DIR)

    for font_flavor in options.FONT_FLAVORS:
        theme_service.make_theme(font_flavor)
        publish_service.make_extension(font_flavor)
    publish_service.make_itchio_readme()


if __name__ == '__main__':
    main()
