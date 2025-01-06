from pathlib import Path
from struct import unpack
from ..structs import Chrom, Sample, Batch


def read(path: Path) -> Sample:
    transitions = {}
    for entry in _decode(_open(path)):
        transition = transitions.get(entry.key, [])
        transition.append((entry.time, entry.resp))
        transitions[entry.key] = transition

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


def _open(path: Path) -> bytes:
    """
    Open a file and return the contents of MSScan.bin as a bytes object
    :param path:
    :return:
    """
    p = path / 'AcqData\\MSScan.bin'
    if p.exists():
        with open(path / 'AcqData\\MSScan.bin', 'rb') as file:
            file.seek(0)
            return file.read()

    else:
        raise FileNotFoundError('The specified location does not contain the MSScan.bin file.'
                                f'\n\n file:   {path}')


class Entry:
    def __init__(self, data: bytes):
        """
        This class represents a single point in the total chromatogram.
        Its purpose is to read a line in the bytes object and parse it into a workable data structure.

        :param data: bytes object representing one transition's worth of data
        """
        self.time = self.unpack(data, 'd', 12, 20)
        self.resp = self.unpack(data, 'd', 26, 34)
        self.q1 = self.unpack(data, 'd', 68, 76)
        self.q3 = self.unpack(data, 'd', 34, 42)
        self.frag = self.unpack(data, 'f', 60, 64)
        self.ce = self.unpack(data, 'f', 64, 68)

    @staticmethod
    def unpack(data: bytes, btype: str, beg: int, end: int) -> float:
        """
        Perform a safe unpacking of the byte string for a particular parameter of the entry
        :param data: The original bytes object
        :param btype: The format to pass to struct.unpack
        :param beg: the starting index to slice the bytes object
        :param end: the ending index to slice the bytes object

        :return: a float value for the given parameter
        """

        try:
            return unpack(btype, data[beg:end])[0]
        except:
            return 0

    @property
    def key(self) -> tuple[float, float, float, float]:
        return round(self.q1, 1), round(self.q3, 1), round(self.frag, 1), round(self.ce, 1)


def _decode(buff: bytes):
    # magic_number = 186
    magic_number = 158
    offset = unpack('I', buff[88:92])[0]
    n = len(buff)


    nrows = (n - offset) // magic_number
    for i in range(nrows):
        start = offset + magic_number * i
        yield Entry(buff[start:start + magic_number])
