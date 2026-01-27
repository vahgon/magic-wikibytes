from argparse import Namespace
from lib.util._args import parse_args
from pathlib import Path
from enum import Enum
import re

USER_ARGS: Namespace = parse_args()

type HtmlJson = dict[str, str | int]
type ReqJson = dict[str, HtmlJson]
type TableHeaders = list[str]
type TableRows = list[dict[str, str | None]]

ColType = Enum('ColType', [('HEX', 1), ('ISO', 2), ('OFF', 3), ('EXT', 4), ('INF', 5)])

ROOT: Path = Path(__file__).parent
DOCS_PATH: Path = Path(f'{Path(__file__).parent.parent.parent}/docs')
ENV_PATH: Path = Path(f'{ROOT}/.conf')

FSIG_REGEX = {
    'HEX_REGEX': re.compile(pattern=r'(([A-F0-9?]{2})(\s{1})?)+',flags=re.IGNORECASE),
    'CONTAINER_REGEX': re.compile(pattern=r'([A-F0-9?]{2}\s?)+(\(([\w\s-])*\))(([A-F0-9?]{2}\s?)+(\(([\w\s-])*\)))',flags=re.IGNORECASE),
    'LITTLE_ENDIAN_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'BIG_ENDIAN_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'BIG_LITTLE_ENDIAN_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'WEIRD_CHARS_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'ISO_REGEX': re.compile(pattern=r''),
    'OFFSET_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'EXTENSION_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE),
    'DESC_REGEX': re.compile(pattern=r'',flags=re.IGNORECASE)
}
