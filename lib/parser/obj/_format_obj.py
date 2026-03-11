from dataclasses import dataclass, field
from lib.exceptions.unexpected_format_error import UnexpectedFormatError

ucode = str.maketrans({i: chr(0x2400 + i) for i in range(0x21)} | {0x7f: '\u2421'})

@dataclass
class BytePairing:
    h_bytes: list[str]
    i_bytes: list[str]

    _latin1:   list[str] = field(default_factory=list[str])
    _balanced: bool      = field(default=False)

    def __post_init__(self) -> None:
        if len(self.h_bytes) == len(self.i_bytes):
            if True: # todo - if user wants to force hex to latin conversion even if balanced
                self._set_latin()
            return

        self._set_latin()

    def _set_latin(self) -> None:
        for byte in self.h_bytes:
            # todo - if byte == '??', change to user's chosen char for wildcard bytes, n_byte+=byte
            if byte == '??':
                self._latin1.append(byte)
            else:
                decode_byte = bytes.fromhex(byte).decode('latin-1', 'replace')
                decode_byte = decode_byte.translate(ucode)
                self._latin1.append(decode_byte)

        self.i_bytes = self._latin1

@dataclass
class checkbytes:
    '''
    A checkbytes object checks the equality of the bytes in the provided hex and iso values.
    It will first check to see if they are balanced - len(bytes in hex) == len(bytes in iso), 
    then will make adjustments accordingly. 

    :param hex: `str`
    :param iso: `str`
    '''
    hex: (str | list[str])
    iso: (str | list[str])

    def __post_init__(self) -> None:
        if isinstance(self.hex, list) and isinstance(self.iso, list):
            for idx, pair in enumerate(zip(self.hex, self.iso)):
                bytepair = BytePairing(
                    [pair[0][idx:idx+2] for idx in range(0, len(pair[0]), 2)],
                    list(pair[1])
                )
                # todo - user can define spacing
                self.hex[idx] = ''.join(bytepair.h_bytes)
                self.iso[idx] = ''.join(bytepair.i_bytes)

        elif isinstance(self.hex, str) and isinstance(self.iso, str):
            bytepair = BytePairing(
                [self.hex[idx:idx+2] for idx in range(0, len(self.hex), 2)],
                list(self.iso)
            )
            # todo - user can define spacing
            self.hex = ''.join(bytepair.h_bytes)
            self.iso = ''.join(bytepair.i_bytes)

        else:
            e = UnexpectedFormatError()
            e.add_note(f'Mismatched types for hex and iso columns\n\
                    hex: {self.hex}\niso: {self.iso}')
            raise e
