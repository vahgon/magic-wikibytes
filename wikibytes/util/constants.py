from enum import IntEnum
from pathlib import Path

type HtmlJson           = dict[str, str | int]
type ReqJson            = dict[str, HtmlJson]
type ParsedTableDict    = list[dict[str, list[str] | str | int]]

class ColType(IntEnum):
    HEX = 0
    ISO = 1
    OFF = 2
    EXT = 3
    DES = 4

ENV_VARS    = {
    "EMAIL": True,
    "REVID": False,
}

API_URL     = 'https://en.wikipedia.org/w/api.php' 

BADTAGS     = ['cite', 'sup', 'br']
FIXTAGS     = ['a', 'p', 'span']
JNK_CHARS   = ['\xa0', ' ']

HEADERNAMES = [
    'Hex Signature',
    'ISO 8859-1',
    'Offset',
    'Extension',
    'Description',
]

ROOT:     Path  = Path(__file__).parent
ENV_PATH: Path  = Path(f'{ROOT}/.conf')
