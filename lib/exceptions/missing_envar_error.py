from lib.exceptions.wikibytes_error import WikibytesError


class MissingEnvVarError(WikibytesError):
    '''
    This exception is raised when a variable could not be found in .conf
    '''
    pass
