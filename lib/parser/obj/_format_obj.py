from dataclasses import dataclass, field

@dataclass
class checkbytes:
    '''
    A checkbytes object checks the equality of the bytes in the provided hex and iso values.
    It will first check to see if they are balanced - len(bytes in hex) == len(bytes in iso), 
    then will make adjustments accordingly. 
    '''
    hex: str
    iso: str

    _hex_to_latin1: str = field(default_factory=str)

    _h_bytes: (list[str] | list[list[str]]) = field(default_factory=list)
    _i_bytes: (list[str] | list[list[str]]) = field(default_factory=list)

    def __post__init__(self) -> None:
        self._h_bytes = [self.hex[idx:idx+2] for idx in range(0, len(self.hex), 2)]
        self._i_bytes = [byte for byte in self.iso]

    def is_equal(self) -> (bool | None):
        '''
        Checks if each given byte of the hex string is equal to its converted iso 8859-1
        representation.
        
        :return: bool 
        '''
        self.__post__init__()

        if len(self._h_bytes) != len(self._i_bytes):
            return False
        return True
