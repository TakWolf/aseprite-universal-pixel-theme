import shutil
from pathlib import Path

import png
from fontTools.ttLib import TTFont
from lxml import etree
from lxml.etree import XMLParser, Element, SubElement

from tools.configs import path_define
from tools.configs.options import FontFlavor


def _copy_theme_assets(data_dir: Path):
    for dir_from, _, file_names in path_define.theme_assets_dir.walk():
        dir_to = data_dir.joinpath(dir_from.relative_to(path_define.theme_assets_dir))
        dir_to.mkdir(exist_ok=True)
        for file_name in file_names:
            if not file_name.endswith(('.png', '.xml', '.aseprite-data')):
                continue
            shutil.copyfile(dir_from.joinpath(file_name), dir_to.joinpath(file_name))


def _copy_font_assets(data_dir: Path, font_flavor: FontFlavor):
    for font_size in [8, 10]:
        dir_from = path_define.font_assets_dir.joinpath(str(font_size))
        dir_to = data_dir.joinpath('fonts', str(font_size))
        dir_to.mkdir(parents=True)
        shutil.copytree(dir_from.joinpath('LICENSE'), dir_to.joinpath('LICENSE'))
        shutil.copyfile(dir_from.joinpath('OFL.txt'), dir_to.joinpath('OFL.txt'))
        font_file_name = f'fusion-pixel-{font_size}px-proportional-{font_flavor}.ttf'
        shutil.copyfile(dir_from.joinpath(font_file_name), dir_to.joinpath(font_file_name))


def _copy_others(data_dir: Path):
    shutil.copyfile(path_define.project_root_dir.joinpath('LICENSE'), data_dir.joinpath('LICENSE'))
    shutil.copyfile(path_define.static_assets_dir.joinpath('package.json'), data_dir.joinpath('package.json'))


def _xml_get_child_element_by_id(parent: Element, id_name: str) -> Element | None:
    for child in parent:
        if 'id' not in child.attrib:
            continue
        if child.get('id') == id_name:
            return child
    return None


def _modify_theme_xml(path: Path, theme_name: str, relative_path: str, font_flavor: FontFlavor):
    # 读取主题
    elem_root = etree.parse(path, XMLParser(remove_blank_text=True)).getroot()
    elem_root.set('name', theme_name)

    # -------
    # 补充作者
    elem_authors = elem_root.xpath('/theme/authors')[0]

    elem_author_takwolf = SubElement(elem_authors, 'author')
    elem_author_takwolf.set('name', 'TakWolf')
    elem_author_takwolf.set('url', 'https://takwolf.com')

    # -------
    # 修改字体
    elem_fonts = elem_root.xpath('/theme/fonts')[0]

    elem_font_10px = Element('font')
    elem_font_10px.set('name', 'fusion-pixel-10px-proportional')
    elem_font_10px.set('type', 'truetype')
    elem_font_10px.set('antialias', 'false')
    elem_font_10px.set('hinting', 'false')
    elem_font_10px.set('file', f'{relative_path}/fonts/10/fusion-pixel-10px-proportional-{font_flavor}.ttf')
    elem_fonts.insert(0, elem_font_10px)

    elem_font_8px = Element('font')
    elem_font_8px.set('name', 'fusion-pixel-8px-proportional')
    elem_font_8px.set('type', 'truetype')
    elem_font_8px.set('antialias', 'false')
    elem_font_8px.set('hinting', 'false')
    elem_font_8px.set('file', f'{relative_path}/fonts/8/fusion-pixel-8px-proportional-{font_flavor}.ttf')
    elem_fonts.insert(1, elem_font_8px)

    elem_font_default = _xml_get_child_element_by_id(elem_fonts, 'default')
    elem_font_default.set('font', elem_font_10px.get('name'))
    elem_font_default.set('size', '10')

    elem_font_mini = _xml_get_child_element_by_id(elem_fonts, 'mini')
    elem_font_mini.set('font', elem_font_8px.get('name'))
    elem_font_mini.set('size', '8')
    elem_font_mini.attrib.pop('mnemonics')

    # -------
    # 修复属性
    elem_dimensions = elem_root.xpath('/theme/dimensions')[0]

    elem_dim_tabs_height = _xml_get_child_element_by_id(elem_dimensions, 'tabs_height')
    elem_dim_tabs_height.set('value', '19')

    elem_parts = elem_root.xpath('/theme/parts')[0]

    elem_part_window = _xml_get_child_element_by_id(elem_parts, 'window')
    elem_part_window.set('h1', '18')

    elem_styles = elem_root.xpath('/theme/styles')[0]

    elem_style_window_with_title = _xml_get_child_element_by_id(elem_styles, 'window_with_title')
    elem_style_window_with_title.set('border-top', '18')

    elem_style_window_title_label = _xml_get_child_element_by_id(elem_styles, 'window_title_label')
    elem_style_window_title_label.set('margin-top', '4')

    elem_style_window_close_button = _xml_get_child_element_by_id(elem_styles, 'window_close_button')
    elem_style_window_close_button.set('margin-top', '4')

    elem_style_window_center_button = _xml_get_child_element_by_id(elem_styles, 'window_center_button')
    elem_style_window_center_button.set('margin-top', '4')

    elem_style_window_play_button = _xml_get_child_element_by_id(elem_styles, 'window_play_button')
    elem_style_window_play_button.set('margin-top', '4')

    elem_style_window_stop_button = _xml_get_child_element_by_id(elem_styles, 'window_stop_button')
    elem_style_window_stop_button.set('margin-top', '4')

    elem_style_window_stop_button = _xml_get_child_element_by_id(elem_styles, 'window_help_button')
    elem_style_window_stop_button.set('margin-top', '4')

    # 写入主题
    etree.indent(elem_root, space='    ')
    xml_str = etree.tostring(elem_root, encoding='utf-8', doctype='<?xml version="1.0" encoding="utf-8" ?>').replace(b'/>', b' />') + b'\n'
    path.write_bytes(xml_str)


def _modify_light_theme_xml(data_dir: Path, font_flavor: FontFlavor):
    file_path = data_dir.joinpath('theme.xml')
    _modify_theme_xml(file_path, 'Universal Pixel Light', '.', font_flavor)


def _modify_dark_theme_xml(data_dir: Path, font_flavor: FontFlavor):
    file_path = data_dir.joinpath('dark', 'theme.xml')
    _modify_theme_xml(file_path, 'Universal Pixel Dark', '..', font_flavor)


def _modify_fonts(data_dir: Path, font_size: int, ascent: int, descent: int):
    fonts_dir = data_dir.joinpath('fonts', str(font_size))
    for file_path in fonts_dir.iterdir():
        if file_path.suffix != '.ttf':
            continue

        font = TTFont(file_path, recalcTimestamp=False)
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


def _load_png(file_path: Path) -> tuple[list[list[tuple[int, int, int, int]]], int, int]:
    width, height, pixels, _ = png.Reader(filename=file_path).read()
    bitmap = []
    for pixels_row in pixels:
        bitmap_row = []
        for x in range(0, width * 4, 4):
            red = pixels_row[x]
            green = pixels_row[x + 1]
            blue = pixels_row[x + 2]
            alpha = pixels_row[x + 3]
            bitmap_row.append((red, green, blue, alpha))
        bitmap.append(bitmap_row)
    return bitmap, width, height


def _save_png(bitmap: list[list[tuple[int, int, int, int]]], file_path: Path):
    pixels = []
    for bitmap_row in bitmap:
        pixels_row = []
        for red, green, blue, alpha in bitmap_row:
            pixels_row.append(red)
            pixels_row.append(green)
            pixels_row.append(blue)
            pixels_row.append(alpha)
        pixels.append(pixels_row)
    png.from_array(pixels, 'RGBA').save(file_path)


def _modify_sheet_png(data_dir: Path, is_dark: bool):
    if is_dark:
        static_png_path = path_define.static_assets_dir.joinpath('dark', 'sheet.png')
        data_png_path = data_dir.joinpath('dark', 'sheet.png')
    else:
        static_png_path = path_define.static_assets_dir.joinpath('sheet.png')
        data_png_path = data_dir.joinpath('sheet.png')

    static_bitmap, static_width, static_height = _load_png(static_png_path)
    data_bitmap, data_width, data_height = _load_png(data_png_path)
    assert static_width == data_width
    assert static_height == data_height
    for y, bitmap_row in enumerate(static_bitmap):
        for x, (red, green, blue, alpha) in enumerate(bitmap_row):
            if alpha == 0:
                continue
            data_bitmap[y][x] = red, green, blue, alpha

    _save_png(data_bitmap, data_png_path)


def make_theme(font_flavor: FontFlavor):
    data_dir = path_define.data_dir.joinpath(font_flavor)
    if data_dir.exists():
        shutil.rmtree(data_dir)
    data_dir.mkdir(parents=True)

    _copy_theme_assets(data_dir)
    _copy_font_assets(data_dir, font_flavor)
    _copy_others(data_dir)
    _modify_light_theme_xml(data_dir, font_flavor)
    _modify_dark_theme_xml(data_dir, font_flavor)
    _modify_fonts(data_dir, 10, 10, -2)
    _modify_fonts(data_dir, 8, 7, -1)
    _modify_sheet_png(data_dir, False)
    _modify_sheet_png(data_dir, True)
    print(f"Make theme: '{data_dir}'")
