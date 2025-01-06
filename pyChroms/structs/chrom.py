# noinspection PyPackageRequirements
from numpy import ndarray, array


class Chrom:
    def __init__(self, chrom=None, label=''):
        self._chromatogram = array([[], []])

        self.label = label

        if chrom is not None:
            if isinstance(chrom, list):
                self.from_list(chrom)
            elif isinstance(chrom, ndarray):
                self.from_array(chrom)

    @property
    def n(self):
        """
        Returns the number of points in the chromatogram
        """
        return len(self._chromatogram)

    @property
    def x(self):
        return self._chromatogram[:, 0]

    @property
    def y(self):
        return self._chromatogram[:, 1]

    @property
    def x_min(self):
        return self._chromatogram[:, 0].min()

    @property
    def x_max(self):
        return self._chromatogram[:, 0].max()

    @property
    def y_min(self):
        return self._chromatogram[:, 1].min()

    @property
    def y_max(self):
        return self._chromatogram[:, 1].max()

    def move_max_to(self, x: float):
        self.translate_x(x - self.x_max)

    def from_list(self, data: list[list[float, float]]) -> None:
        """
        initializes the chromatogram data from a nested list of floats
        """
        self._chromatogram = array(data)

    def from_array(self, data: ndarray) -> None:
        """
        initializes the chromatogram data from a numpy array
        """
        self._chromatogram = array(data)

    def get(self) -> ndarray:
        """
        Returns the chromatogram data as a numpy array
        """
        return self._chromatogram.copy()

    def copy(self):
        """
        Returns a copy of this Chrom object. Automatically sets the bezier parameters after copying
        """
        return Chrom(self._chromatogram)

    def normalize(self):
        self._chromatogram[:, 1] /= self.y_max

    def center(self):
        self._chromatogram[:, 0] -= self._chromatogram[self._chromatogram[:, 1].argmax(0), 0]

    def trim(self, x_min: float, x_max: float):
        ind = (x_min <= self._chromatogram[:, 0]) * (self._chromatogram[:, 0] <= x_max)

        self._chromatogram = self._chromatogram[ind, :]


null_chrom = Chrom([[0, 0]])
