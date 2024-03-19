import logging
import os.path
from xml.dom.minidom import Document, Element, Node

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


def _xml_set_id_attribute(parent: Document | Element, attribute_name: str):
    if parent.nodeType == Node.ELEMENT_NODE:
        if parent.hasAttribute(attribute_name):
            parent.setIdAttribute(attribute_name)
    for child in parent.childNodes:
        _xml_set_id_attribute(child, attribute_name)


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

    node_font_default = dom.getElementById('default')
    node_font_default.setAttribute('font', node_font_10px.getAttribute('name'))
    node_font_default.setAttribute('size', '10')

    node_font_mini = dom.getElementById('mini')
    node_font_mini.setAttribute('font', node_font_8px.getAttribute('name'))
    node_font_mini.setAttribute('size', '8')
    node_font_mini.removeAttribute('mnemonics')

    node_fonts.insertBefore(node_font_8px, node_font_default)
    node_fonts.insertBefore(node_font_10px, node_font_8px)


def _modify_light_theme_xml():
    file_path = os.path.join(data_dir, 'theme.xml')
    dom = fs_util.read_xml(file_path)
    _xml_set_id_attribute(dom, 'id')
    _modify_theme_xml(dom, 'Universal Pixel Light', '.')
    fs_util.write_xml(dom, file_path)


def _modify_dark_theme_xml():
    file_path = os.path.join(data_dir, 'dark', 'theme.xml')
    dom = fs_util.read_xml(file_path)
    _xml_set_id_attribute(dom, 'id')
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


def main():
    fs_util.delete_dir(data_dir)
    fs_util.make_dir(data_dir)

    _copy_theme_assets()
    _copy_font_assets()
    _copy_others()
    _modify_light_theme_xml()
    _modify_dark_theme_xml()
    _modify_fonts(10, 11, -3)
    _modify_fonts(8, 8, -2)


if __name__ == '__main__':
    main()
