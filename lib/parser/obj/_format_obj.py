JNK_CHARS = ['\xa0', ' ']

class Filebyte:
    def __init__(self, hexStr: str) -> None:
        self.__text:        str       = hexStr
        self.__byte_list:   list[str] = [self.__text[i:i+2] for i in range(0, len(self.__text), 2)]

    def format_hexstring(self) -> str:
        hexString:  str = self.__text

        for char in JNK_CHARS:
            hexString = self.__text.replace(char, '')
        return hexString

class Latin1:
    def __init__(self, hexStr: str) -> None:
        self.sisterHex: str = hexStr
        self.__latin1:  str   = ''

    def format_iso(self) -> str:
        for idx in range(0, len(self.sisterHex), 2):
            byte = self.sisterHex[idx:idx+2]
            if byte != '??':
                byte_hex = bytes.fromhex(byte)
                self.__latin1 += byte_hex.decode('latin-1')
        return self.__latin1
