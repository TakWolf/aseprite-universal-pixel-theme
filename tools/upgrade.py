from tools.services import upgrade_service


def main():
    upgrade_service.upgrade_aseprite_theme()
    upgrade_service.upgrade_fonts()


if __name__ == '__main__':
    main()
