from pathlib import Path
from struct import unpack
from ..structs import Chrom, Sample, Batch
from sqlite3 import connect

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def read(path: Path) -> Sample:
    p = path / 'analysis.qqq'

    if p.exists():
        with connect(str(p)) as con:
            con.row_factory = dict_factory
            cur = con.cursor()

            cur.execute('''
            SELECT a.Name as drug, 
            sd.Q1MzStart as q1, 
            sd.Q3MzStart as q3, 
            abs(sd.Q2CollisionEnergy) as ce, 
            cd.NumDataPoints as n, 
            cd.Rt as rt, 
            cd.Intensity as tic  
            FROM Analytes as a 
            INNER JOIN ScanletDefinitions as sd ON sd.Analyte = a.Id
            INNER JOIN ChromatogramData as cd ON cd.Scanlet = sd.Id''')

            data = cur.fetchall()

    entries = [Entry(row) for row in data]
    transitions = {entry.key: list(zip(entry.time, entry.resp)) for entry in entries}

    sample = Sample(path)
    for k, _list in transitions.items():
        sample[k] = Chrom(_list)

    return sample


def read_batch(path: Path) -> Batch:
    batch = Batch(path)
    batch.name = path.name

    for spath in path.iterdir():
        if spath.name.endswith('.d'):
            batch.add_sample(read(spath))

    return batch


class Entry:
    def __init__(self, data: dict):
        """
        This class represents a single point in the total chromatogram.
        Its purpose is to read a line in the bytes object and parse it into a workable data structure.

        :param data: bytes object representing one transition's worth of data
        """
        self.time = self.unpack(data['rt'])
        self.time = [t/60 for t in self.time]
        self.resp = self.unpack(data['tic'])
        self.q1 = data['q1']
        self.q3 = data['q3']
        self.frag = 0
        self.ce = data['ce']

    @staticmethod
    def unpack(data: bytes):
        """
        Perform a safe unpacking of the byte string for a particular parameter of the entry
        :param data: The original bytes object

        :return: a float value for the given parameter
        """

        n = len(data) // 8

        def gen():
            i = 0
            while i < n:
                try:
                    yield unpack('d', data[i * 8:(i + 1) * 8])[0]
                except:
                    pass
                i += 1

        return list(gen())

    @property
    def key(self) -> tuple[float, float, float, float]:
        return round(self.q1, 1), round(self.q3, 1), round(self.frag, 1), round(self.ce, 1)


