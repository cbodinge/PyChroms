from PyGraphing import Graph, Icon
from PyGraphing.series.scatter.curve import Curve
from PSVG import Path, Text
from .__fonts__ import font500, font600, font700
from ..structs.chrom import Chrom

class Chromatogram(Graph):
    def __init__(self, w, h):
        super().__init__(font500, w=w, h=h)
        self._chroms = []

    def add_curve(self, chrom: Chrom, color: tuple[int, int, int],
                  fill_opacity: float=.01, stroke_opacity: float=1, stroke_width: float=0.2):

        path = Path(fill=color, fill_opacity=fill_opacity,
                    stroke=color, stroke_opacity=stroke_opacity, stroke_width=stroke_width)

        curve = Curve(icon=None, plot=self.plot, X=chrom.x, Y=chrom.y, path=path)
        self.plot.addChild(curve)
        self._chroms.append(curve)

        p = self.plot

        p.extrema = (min(p.xmin, chrom.x_min), max(p.xmax,chrom.x_max),
                     min(p.ymin, chrom.y_min), max(p.ymax, chrom.y_max))

    def _frame(self):
        f = self.frame
        f.T, f.B, f.L, f.R = False, True, True, True

        b = f.border
        b.stroke = (0, 0, 0)
        b.stroke_width = 1
        b.stroke_opacity = 1

        t = self.text()
        t.anchor = 'middle'
        t.baseline = 'hanging'

        self.frame.x_axis.dist2text = 2
        self.frame.x_axis.text = t

    def _x_axis(self):
        pass

    def _x_label(self):
        x = self.xlabel
        x.root.active = True
        x.text = 'X LABEL'
        x.textColor = (55, 75, 201)
        x.alignment = (1, 2)

    def _y_label(self):
        y = self.ylabel
        y.text = 'Y LABEL'
        y.textColor = (55, 75, 201)
        y.textOpacity = 1
        y.alignment = (1, 0)

    def set(self):
        self.plot.ymax *= 1.1
        self._frame()
        self._x_axis()
        self._x_label()
        self._y_label()

        self.set_sizes((.2,.2,.6,.6))