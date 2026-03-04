from argparse import Namespace
from enum import IntEnum
from pathlib import Path
from typing import Self

from lib.util._args import parse_args

USER_ARGS: Namespace = parse_args()

type HtmlJson = dict[str, str | int]
type ReqJson = dict[str, HtmlJson]
type FileData = (list[bytes] | list[str] | str | bytes | int)
type ParsedTableDict = list[dict[str, FileData]]

class ColType(IntEnum):
    HEX = 0
    ISO = 1
    OFF = 2
    EXT = 3
    DES = 4

BADTAGS = ['cite', 'sup', 'span', 'br']
FIXTAGS = ['a', 'p']

HEADERNAMES = ['Hex Signature', 'ISO 8859-1', 'Offset', 'Extension', 'Description']

ROOT: Path = Path(__file__).parent
DOCS_PATH: Path = Path(f'{Path(__file__).parent.parent.parent}/docs')
ENV_PATH: Path = Path(f'{ROOT}/.conf')
