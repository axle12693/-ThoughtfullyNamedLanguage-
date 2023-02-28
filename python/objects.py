
class Token:

    def __init__(self, type: str, value: str, pos: tuple) -> None:
        self.type: str = type
        self.val = value
        self.pos = pos
