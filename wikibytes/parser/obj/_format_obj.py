from argparse import Namespace
from dataclasses import dataclass, field
from typing import Any

from wikibytes.exceptions.unexpected_format_error import UnexpectedFormatError

ucode = str.maketrans({i: chr(0x2400 + i) for i in range(0x21)} | {0x7f: '\u2421'})

@dataclass
class _BytePairing:
    h_bytes:    list[str]
    i_bytes:    list[str]
    _f_latin:   bool
    _hex_wchar: str 

    _latin1:    list[str] = field(default_factory=list[str])
    _balanced:  bool      = field(default=False)

    def __post_init__(self) -> None:
        if len(self.h_bytes) == len(self.i_bytes):
            if self._f_latin:
                self._set_latin()
            return

        self._set_latin()

    def _set_latin(self) -> None:
        for idx, byte in enumerate(self.h_bytes):
            if byte == '??':
                self._latin1.append(self._hex_wchar)
                print(self._hex_wchar)
                self.h_bytes[idx] = self._hex_wchar * 2
            else:
                decode_byte = bytes.fromhex(byte).decode('latin-1', 'replace')
                decode_byte = decode_byte.translate(ucode)
                self._latin1.append(decode_byte)

        self.i_bytes = self._latin1

@dataclass
class CheckBytes:
    """
    A checkbytes object checks the equality of the bytes in the provided hex and iso values.
    It will first check to see if they are balanced - len(bytes in hex) == len(bytes in iso), 
    then will make adjustments accordingly. 

    :param hex: `str`
    :param iso: `str`
    """
    hex:            (str | list[str])
    iso:            (str | list[str])
    args:           Namespace

    _hex_sep_char:  Any = field(default='')

    def __post_init__(self) -> None:
        if isinstance(self.hex, list) and isinstance(self.iso, list):
            for idx, pair in enumerate(zip(self.hex, self.iso)):
                bytepair = _BytePairing(
                    [pair[0][idx:idx+2] for idx in range(0, len(pair[0]), 2)],
                    list(pair[1]),
                    self.args.force_latin,
                    self.args.hexsep_char
                )
                self.hex[idx] = self.args.hexsep_char.join(bytepair.h_bytes)
                self.iso[idx] = ''.join(bytepair.i_bytes)

        elif isinstance(self.hex, str) and isinstance(self.iso, str):
            bytepair = _BytePairing(
                [self.hex[idx:idx+2] for idx in range(0, len(self.hex), 2)],
                list(self.iso),
                self.args.force_latin,
                self.args.hexsep_char
            )
            self.hex = self._hex_sep_char.join(bytepair.h_bytes)
            self.iso = ''.join(bytepair.i_bytes)

        else:
            e = UnexpectedFormatError()
            e.add_note(f'Mismatched types for hex and iso columns\n\
                    hex: {self.hex}\niso: {self.iso}')
            raise e
