class ParserException(Exception):
    """Exception raised for errors in the input parsed.

    Attributes:
        html -- input html code which caused the error
        message -- explanation of the error
    """

    def __init__(self, html, message="Unexpected html format"):
        self.html = html
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.html}\nPARSER FAILED: {self.message}'