
class ResponseError(Exception):
    def __init__(self, message):            
        super().__init__(message)


class AuthError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class UserNotFoundError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)