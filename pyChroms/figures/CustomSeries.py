from PyGraphing.series.scatter.curve import Curve
from PyGraphing import Plot
from PSVG import Path
from numpy import ndarray

class FilledCurve(Curve):
    def __init__(self, X: ndarray, Y: ndarray, path: Path, plot: Plot, *args, **kwargs):
        super().__init__(X=X, Y=Y, icon=None, path=path, plot=plot, *args, **kwargs)

    def _process(self):
        super()._process()

        stroke = self.path.copy()
        stroke.fill_opacity = 0
        stroke.points = self.path.points[:]
        self.add_child(stroke)

        x0, y0 = self.path.points[0][1:]

        self.path.points.insert(0, ('M', x0, self.plot.h))
        self.path.points[1] = ('V', y0)
        self.path.points.append(('V', self.plot.h))
        self.path.stroke_opacity = 0
