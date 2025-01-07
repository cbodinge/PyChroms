from pathlib import Path
from pyChroms import BrukerBatch
from pyChroms.figures.DefaultChromatogram import Chromatogram
from pyChroms.structs.drug import Drug

from PSVG import Document
from pyChroms.export import png


drugs_of_interest = {
    (328.4, 165.1, 0, 32.6): Drug('6-MAM', (9, 151, 214)),
    (301.7, 256.1, 0, 16.8): Drug('Temazepam', (7, 216, 121)),
    (150.2, 119.1, 0, 5.9): Drug('Methamphetamine', (89, 246, 246)),
    (337.5, 105.1, 0, 30.6): Drug('Fentanyl', (121, 21, 142)),
    (264.4, 233.1, 0, 9.9): Drug('Nortryptiline', (218, 7, 158))}


def main():
    doc = Document(w=400, h=400)

    C = Chromatogram(400, 400)
    C.title.size += 3
    C.title.text = ''
    # C.plot.extrema = 1000000000, 0, 10000000000, 0
    C.plot.extrema = .00000000001, 7.5, 0, 0

    entries = list(BrukerBatch(Path('C:\\Data\\Bruker\\test')).values())[0]
    for key, chrom in entries.items():
        if key in drugs_of_interest:
            drug = drugs_of_interest[key]
            chrom.label = drug.name
            C.add_curve(chrom, drug.color)

    C.set()
    doc.addChild(C.root)

    return doc

d = main()
png(d, 'Bruker_2', 20)