from lib.exceptions.wikibytes_error import WikibytesError


class UnexpectedFormatError(WikibytesError):
    '''
    This exception is raised if the response from the request object sent to the wikimedia API returns data
    that is of an unexpected class when calling .json()
    '''
    pass
