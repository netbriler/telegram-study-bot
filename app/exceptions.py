class BadRequest(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return 'Bad Request: ' + self.message


class Conflict(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return 'Conflict: ' + self.message
