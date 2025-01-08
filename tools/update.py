from tools.services import update_service


def main():
    update_service.update_aseprite_theme('v1.3.11')
    update_service.update_fonts()


if __name__ == '__main__':
    main()
