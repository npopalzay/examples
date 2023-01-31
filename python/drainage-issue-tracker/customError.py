class AppError(Exception):
    """custom class to capture exceptions

    Args:
        Exception (Exceptiosn):
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class EmailError(AppError):
    """sub class of the app error to capture email exceptions

    Args:
        AppError (AppError):
    """

    def __init__(self, message):
        super().__init__(message)
