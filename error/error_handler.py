class JsonParserError(Exception):
    """Custom exception for errors during JSON parsing."""
    
    def __init__(self, message, position=None):
        self.message = message
        self.position = position  # e.g., (line, column)
        super().__init__(self._format_message())

    def _format_message(self):
        if self.position:
            return f"[Line {self.position[0]}, Column {self.position[1]}] {self.message}"
        return self.message

    def __str__(self):
        return self._format_message()
