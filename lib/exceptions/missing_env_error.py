from lib.exceptions.wikibytes_error import WikibytesError

class MissingEnvError(WikibytesError):
    """
    This exception is raised when a value could not be read from .env
    """
    pass
