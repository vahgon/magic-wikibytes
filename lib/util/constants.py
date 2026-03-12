from enum import IntEnum
from pathlib import Path

from lib.util._args import parse_args

USER_ARGS = parse_args()

type HtmlJson = dict[str, str | int]
type ReqJson = dict[str, HtmlJson]
type FileData = (list[str] | str | int)
type ParsedTableDict = list[dict[str, FileData]]

class ColType(IntEnum):
    HEX = 0
    ISO = 1
    OFF = 2
    EXT = 3
    DES = 4

BADTAGS = ['cite', 'sup', 'br']
FIXTAGS = ['a', 'p', 'span']

JNK_CHARS = ['\xa0', ' ']

HEADERNAMES = ['Hex Signature', 'ISO 8859-1', 'Offset', 'Extension', 'Description']

ROOT: Path = Path(__file__).parent
ENV_PATH: Path = Path(f'{ROOT}/.conf')
