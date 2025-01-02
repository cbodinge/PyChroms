from pathlib import Path
from .sample import Sample


class Batch(dict):
    def __init__(self, path: Path):
        super().__init__()
        self.name = ''
        self.path = path

    def add_sample(self, sample: Sample):
        self[sample.name] = sample
