class ProviderHttpException(Exception):
    """Provider http exception"""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f'[{self.status_code}] {self.message}'

class ProviderTypeException(Exception):
    """Provider type exception"""
    def __init__(self, message, expected):
        self.message = message
        self.expected = expected

    def __str__(self):
        if isinstance(self.expected, list):
            self.expected = ', '.join(self.expected)
            self.expected = f'one of [{self.expected}]'
        if self.message.endswith('.'):
            return f'{self.message} Expected: {self.expected}'
        return f'{self.message}. Expected: {self.expected}'