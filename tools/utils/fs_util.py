import json
import os
import shutil
import xml.dom.minidom
from pathlib import Path
from typing import Any
from xml.dom.minidom import Document


def delete_dir(path: Path):
    if path.exists():
        shutil.rmtree(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text('utf-8'))


def write_json(data: Any, path: Path):
    path.write_text(f'{json.dumps(data, indent=2, ensure_ascii=False)}\n', 'utf-8')


def read_xml(path: Path) -> Document:
    return xml.dom.minidom.parse(os.fspath(path))


def write_xml(dom: Document, path: Path):
    xml_str = dom.toprettyxml(indent=' ' * 4, newl='\n', encoding='utf-8')
    with path.open('wb') as file:
        for line in xml_str.splitlines():
            if line.strip() == b'':
                continue
            file.write(line.replace(b'?>', b' ?>').replace(b'/>', b' />'))
            file.write(b'\n')
