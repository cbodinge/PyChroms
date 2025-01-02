from pathlib import Path


class Sample(dict):
    def __init__(self, path: Path):
        super().__init__()
        self.name = path.name
        self.path = path
        self.type = ''

