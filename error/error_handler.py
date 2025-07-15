class JsonParserError(Exception):
    """Custom exception for errors during JSON parsing."""

    def __init__(self, message, position=None):
        self.position = position  # (line, column)
        formatted = self._format_message(message)
        super().__init__(formatted)

    def _format_message(self, message):
        if self.position:
            line, col = self.position
            return f"[Line {line}, Column {col}] {message}"
        return message

    def __str__(self):
        return self.args[0]
