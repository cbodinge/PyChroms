class Drug:
    def __init__(self, name: str, color: tuple[int, int, int] = (0, 0, 0), factor: float=1.0, dash=None):
        self.name = name
        self.color = color
        self.factor = factor
        self.dash = dash