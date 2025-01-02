from pathlib import Path
from pyChroms import AgilentBatch
from pyChroms.figures.DefaultChromatogram import Chromatogram

from PSVG import Document


def get_chroms():
    entries = AgilentBatch(Path('C:\\Data\\Agilent\\INP\\Mon INP-106v-3-241031\\120224-9106-3monday-241125'))
    return [i[(286.2, 152.5, 164.0, 53.0)] for i in entries.values()]


def main():
    chroms = get_chroms()
    doc = Document(w=1200, h=1200)
    C = Chromatogram(500, 500)
    for chrom in chroms:
        C.add_curve(chrom, (55, 175, 122))


    C.set()
    doc.addChild(C.root)

    svg = doc.construct()

    with open('test.svg', 'w') as file:
        file.write(svg)

main()