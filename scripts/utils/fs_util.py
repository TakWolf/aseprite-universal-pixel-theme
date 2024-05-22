import json
import os
import shutil
import xml.dom.minidom
from typing import Any
from xml.dom.minidom import Document


def delete_dir(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.exists(path):
        shutil.rmtree(path)


def read_str(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_str(text: str, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_json(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Any:
    return json.loads(read_str(path))


def write_json(data: Any, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    write_str(f'{json.dumps(data, indent=2, ensure_ascii=False)}\n', path)


def read_xml(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Document:
    return xml.dom.minidom.parse(path)


def write_xml(dom: Document, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    xml_str = dom.toprettyxml(indent=' ' * 4, newl='\n', encoding='utf-8')
    with open(path, 'wb') as file:
        for line in xml_str.splitlines():
            if line.strip() == b'':
                continue
            file.write(line.replace(b'?>', b' ?>').replace(b'/>', b' />'))
            file.write(b'\n')
