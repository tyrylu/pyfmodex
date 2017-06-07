class FmodError(Exception):
    def __init__(self, result):
        self.result = result
        self.message = result.name.replace("_", " ")

    def __str__(self):
        return self.message


