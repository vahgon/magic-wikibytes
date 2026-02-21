
class binhex:
    def __init__(self, hexString: str) -> None:
        self.text: str = _format_hexstring(hexString)
        self.byteList: list[str] = [self.text[i:i+2] for i in range(0, len(self.text), 2)]

    @staticmethod
    def _format_hexstring(hexString: str) -> str:
        jnkChars = ['\xa0', ' ']

        for char in jnkChars:
            hexString = hexString.replace(char, '')
        return hexString

class iso:
    def __init__(self, hexObj: binhex, isoString: str) -> None:
        self.text: str = isoString
        self.sisterHex: binhex = hexObj
        self._format_iso()

    def _format_iso(self) -> None:
        for i in self.sisterHex.byteList:
            if i != '??':
                byte = bytes.fromhex(i)
                decoded = byte.decode('latin-1')
