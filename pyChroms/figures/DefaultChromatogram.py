from PyGraphing import Graph, Icon
from PyGraphing.series.scatter.curve import Curve
from PSVG import Path
from .__fonts__ import font500
from ..structs.chrom import Chrom
from math import ceil


class Chromatogram(Graph):
    def __init__(self, w, h):
        super().__init__(font500, w=w, h=h)
        self._chroms = []

    def add_curve(self, chrom: Chrom, color: tuple[int, int, int],
                  fill_opacity: float=.6, stroke_opacity: float=1, stroke_width: float=1):

        path = Path(fill=color, fill_opacity=fill_opacity,
                    stroke=color, stroke_opacity=stroke_opacity, stroke_width=stroke_width)

        curve = Curve(icon=None, plot=self.plot, X=chrom.x, Y=chrom.y, path=path)
        curve.label = chrom.label
        self.plot.addChild(curve)
        self._chroms.append(curve)

        p = self.plot

        p.extrema = (min(p.xmin, chrom.x_min), max(p.xmax,chrom.x_max),
                     min(p.ymin, chrom.y_min), max(p.ymax, chrom.y_max))

    def _frame(self):
        f = self.frame
        f.T, f.B, f.L, f.R = False, True, True, False

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
        x = self.frame.x_axis
        x.text.baseline = 'hanging'
        x.dist2text = 7
        n = 7
        x_min = self.plot.xmin
        x_max = self.plot.xmax

        rng = abs(x_max - x_min)
        factor = significance(rng)
        dx = select_dx(ceil(rng*factor)/n)/factor

        _x = ceil(factor*x_min)/factor

        while _x<x_max:
            x.addTick(_x, f'{_x:.2f}')
            _x += dx

    def _y_axis(self):
        y = self.frame.y_axis
        y.text.anchor = 'end'
        y.dist2text = 3
        n = 7
        y_min = self.plot.ymin
        y_max = self.plot.ymax

        rng = abs(y_max - y_min)
        factor = significance(rng)
        dy = select_dx(ceil(rng*factor)/n)/factor

        _y = ceil(factor*y_min)/factor

        while _y<y_max:
            y.addTick(_y, f'{_y:.0f}')
            _y += dy

    def _x_label(self):
        x = self.xlabel
        x.root.active = True
        x.text = 'Retention Time (min)'
        # x.textColor = (55, 75, 201)
        x.alignment = (1, 2)

    def _y_label(self):
        y = self.ylabel
        y.text = 'Response'
        # y.textColor = (55, 75, 201)
        y.textOpacity = 1
        y.alignment = (1, 0)

    def _icon(self, curve: Curve):
        w = 10
        h = 5


        line = Path([('M', -2, h*2),
                     ('L', -2, .2*h),
                     ('L', w*2, .2*h),
                     ('L', w*2, h*2)],
                    stroke=curve.path.stroke,
                    fill=curve.path.fill,
                    fill_opacity=curve.path.fill_opacity)

        return Icon(line, w, h)

    def _legend(self):
        self.legend.active = True

        for chrom in self._chroms:
            text = self.text(text=chrom.label)
            text.size -= 4
            self.legend.addItem(self._icon(chrom), text)


        self.legend.set()

    def set(self):
        self.plot.ymax *= 1.1
        self._frame()
        self._x_axis()
        self._y_axis()
        self._x_label()
        self._y_label()
        self._legend()

        self.set_sizes((.2,.15,.6,.7))

def significance(x):
    multiple = 1
    if x < 1:
        while x<1:
            x *= 10
            multiple *= 10
        return multiple
    elif x > 1:
        while x>=1:
            x /= 10
            multiple /= 10

        return multiple*10

    return multiple

def select_dx(x):
    if x<=1:
        return 1
    if x<=2:
        return 2
    if x<=2.5:
        return 2.5
    if x<=5:
        return 5

    return 10
