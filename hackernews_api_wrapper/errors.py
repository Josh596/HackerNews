class HackerNewsWrapperError(Exception):
    """
    Python HackerNews Error
    """
    pass


class InvalidMethodError(HackerNewsWrapperError):
    """
    Invalid or unrecoginised/unimplemented HTTP request method
    """
    pass


class InvalidDataError(HackerNewsWrapperError):
    """
    Invalid input recognised. Saves unecessary trip to server
    """
    pass