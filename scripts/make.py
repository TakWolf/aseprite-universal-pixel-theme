import logging
import os.path
from xml.dom.minidom import Document, Element, Node

import png
from fontTools.ttLib import TTFont

from scripts import project_root_dir, assets_dir, data_dir
from scripts.utils import fs_util

logger = logging.getLogger('make')


def _copy_theme_assets():
    theme_assets_dir = os.path.join(assets_dir, 'aseprite-theme')
    for dir_from, _, file_names in os.walk(theme_assets_dir):
        for file_name in file_names:
            if not file_name.endswith(('.png', '.xml', '.aseprite-data')):
                continue
            dir_to = dir_from.replace(theme_assets_dir, data_dir, 1)
            fs_util.make_dir(dir_to)
            fs_util.copy_the_file(file_name, dir_from, dir_to)


def _copy_font_assets():
    for font_size in [8, 10]:
        dir_from = os.path.join(assets_dir, 'fusion-pixel-font', str(font_size))
        dir_to = os.path.join(data_dir, 'fonts', str(font_size))
        fs_util.make_dir(dir_to)
        fs_util.copy_the_dir('LICENSE', dir_from, dir_to)
        fs_util.copy_the_file('OFL.txt', dir_from, dir_to)
        fs_util.copy_the_file(f'fusion-pixel-{font_size}px-proportional-zh_hans.otf', dir_from, dir_to)


def _copy_others():
    fs_util.copy_the_file('LICENSE', project_root_dir, data_dir)
    fs_util.copy_the_file('package.json', os.path.join(assets_dir, 'static'), data_dir)


def _xml_get_item_node_by_id(parent: Element, id_name: str) -> Element | None:
    for child in parent.childNodes:
        if child.nodeType != Node.ELEMENT_NODE:
            continue
        if not child.hasAttribute('id'):
            continue
        if child.getAttribute('id') == id_name:
            return child
    return None


def _modify_theme_xml(dom: Document, theme_name: str, relative_path: str):
    # ----------
    # 修改主题名称
    node_theme = dom.firstChild
    node_theme.setAttribute('name', theme_name)

    # -------
    # 补充作者
    node_authors = dom.getElementsByTagName('authors')[0]

    node_author_takwolf = dom.createElement('author')
    node_author_takwolf.setAttribute('name', 'TakWolf')
    node_author_takwolf.setAttribute('url', 'https://takwolf.com')
    node_authors.appendChild(node_author_takwolf)

    # -------
    # 修改字体
    node_fonts = dom.getElementsByTagName('fonts')[0]

    node_font_10px = dom.createElement('font')
    node_font_10px.setAttribute('name', 'fusion-pixel-10px-proportional')
    node_font_10px.setAttribute('type', 'truetype')
    node_font_10px.setAttribute('antialias', 'false')
    node_font_10px.setAttribute('file', f'{relative_path}/fonts/10/fusion-pixel-10px-proportional-zh_hans.otf')

    node_font_8px = dom.createElement('font')
    node_font_8px.setAttribute('name', 'fusion-pixel-8px-proportional')
    node_font_8px.setAttribute('type', 'truetype')
    node_font_8px.setAttribute('antialias', 'false')
    node_font_8px.setAttribute('file', f'{relative_path}/fonts/8/fusion-pixel-8px-proportional-zh_hans.otf')

    node_font_default = _xml_get_item_node_by_id(node_fonts, 'default')
    node_font_default.setAttribute('font', node_font_10px.getAttribute('name'))
    node_font_default.setAttribute('size', '10')

    node_font_mini = _xml_get_item_node_by_id(node_fonts, 'mini')
    node_font_mini.setAttribute('font', node_font_8px.getAttribute('name'))
    node_font_mini.setAttribute('size', '8')
    node_font_mini.removeAttribute('mnemonics')

    node_fonts.insertBefore(node_font_8px, node_font_default)
    node_fonts.insertBefore(node_font_10px, node_font_8px)

    # -------
    # 修复属性
    node_dimensions = dom.getElementsByTagName('dimensions')[0]

    node_dim_tabs_height = _xml_get_item_node_by_id(node_dimensions, 'tabs_height')
    node_dim_tabs_height.setAttribute('value', '19')

    node_parts = dom.getElementsByTagName('parts')[0]

    node_part_window = _xml_get_item_node_by_id(node_parts, 'window')
    node_part_window.setAttribute('h1', '18')

    node_styles = dom.getElementsByTagName('styles')[0]

    node_style_window_with_title = _xml_get_item_node_by_id(node_styles, 'window_with_title')
    node_style_window_with_title.setAttribute('border-top', '18')

    node_style_window_title_label = _xml_get_item_node_by_id(node_styles, 'window_title_label')
    node_style_window_title_label.setAttribute('margin-top', '4')


def _modify_light_theme_xml():
    file_path = os.path.join(data_dir, 'theme.xml')
    dom = fs_util.read_xml(file_path)
    _modify_theme_xml(dom, 'Universal Pixel Light', '.')
    fs_util.write_xml(dom, file_path)


def _modify_dark_theme_xml():
    file_path = os.path.join(data_dir, 'dark', 'theme.xml')
    dom = fs_util.read_xml(file_path)
    _modify_theme_xml(dom, 'Universal Pixel Dark', '..')
    fs_util.write_xml(dom, file_path)


def _modify_fonts(font_size: int, ascent: int, descent: int):
    fonts_dir = os.path.join(data_dir, 'fonts', str(font_size))
    for file_name in os.listdir(fonts_dir):
        if not file_name.endswith('.otf'):
            continue
        file_path = os.path.join(fonts_dir, file_name)

        font = TTFont(file_path)
        font.recalcTimestamp = False
        px_to_units = 100

        hhea = font['hhea']
        hhea.ascent = ascent * px_to_units
        hhea.descent = descent * px_to_units

        os2 = font['OS/2']
        os2.sTypoAscender = ascent * px_to_units
        os2.sTypoDescender = descent * px_to_units
        os2.usWinAscent = ascent * px_to_units
        os2.usWinDescent = -descent * px_to_units

        font.save(file_path)


def _load_png(
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    width, height, bitmap, _ = png.Reader(filename=file_path).read()
    data = []
    for bitmap_row in bitmap:
        data_row = []
        for x in range(0, width * 4, 4):
            red = bitmap_row[x]
            green = bitmap_row[x + 1]
            blue = bitmap_row[x + 2]
            alpha = bitmap_row[x + 3]
            data_row.append((red, green, blue, alpha))
        data.append(data_row)
    return data, width, height


def _save_png(
        data: list[list[tuple[int, int, int, int]]],
        file_path: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    bitmap = []
    for data_row in data:
        bitmap_row = []
        for red, green, blue, alpha in data_row:
            bitmap_row.append(red)
            bitmap_row.append(green)
            bitmap_row.append(blue)
            bitmap_row.append(alpha)
        bitmap.append(bitmap_row)
    png.from_array(bitmap, 'RGBA').save(file_path)


def _modify_sheet_png(is_dark: bool):
    static_png_path = os.path.join(assets_dir, 'static')
    data_png_path = data_dir
    if is_dark:
        static_png_path = os.path.join(static_png_path, 'dark')
        data_png_path = os.path.join(data_png_path, 'dark')
    static_png_path = os.path.join(static_png_path, 'sheet.png')
    data_png_path = os.path.join(data_png_path, 'sheet.png')

    static_bitmap, static_width, static_height = _load_png(static_png_path)
    data_bitmap, data_width, data_height = _load_png(data_png_path)
    assert static_width == data_width
    assert static_height == data_height
    for row, data_row in enumerate(static_bitmap):
        for col, (red, green, blue, alpha) in enumerate(data_row):
            if alpha == 0:
                continue
            data_bitmap[row][col] = red, green, blue, alpha

    _save_png(data_bitmap, data_png_path)


def main():
    fs_util.delete_dir(data_dir)
    fs_util.make_dir(data_dir)

    _copy_theme_assets()
    _copy_font_assets()
    _copy_others()
    _modify_light_theme_xml()
    _modify_dark_theme_xml()
    _modify_fonts(10, 10, -2)
    _modify_fonts(8, 7, -1)
    _modify_sheet_png(False)
    _modify_sheet_png(True)


if __name__ == '__main__':
    main()
