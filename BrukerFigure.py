from pathlib import Path
from pyChroms import BrukerBatch
from pyChroms.figures.DefaultChromatogram import Chromatogram
from pyChroms.structs.drug import Drug

from PSVG import Document
from pyChroms.export import png

drugs_of_interest = {
    (286.3, 165.1, 0, 40.5): Drug('Morphine', (9, 151, 214)),
    (328.4, 310.1, 0, 14.8): Drug('Naloxone', (7, 216, 121)),
    (328.4, 165.1, 0, 32.6): Drug('6-MAM', (89, 246, 246)),
    (150.2, 119.1, 0, 5.9): Drug('Methamphetamine', (121, 21, 142)),
    (264.4, 58.2, 0, 40.0): Drug('Tramadol', (218, 7, 158)),
    (248.3, 220.1, 0, 15.8): Drug('Meperidine', (242, 67, 19)),
    (219.3, 97.2, 0, 8.9): Drug('Meprobamate', (242, 184, 19)),
    (244.4, 86.2, 0, 4.9): Drug('Phencyclidine', (47, 51, 53)),
    (337.5, 105.1, 0, 30.6): Drug('Fentanyl', (9, 151, 214), dash=[2]),
    (278.4, 234.1, 0, 25.7): Drug('EDDP', (7, 216, 121), dash=[2]),
    (384.5, 253.1, 0, 17.8): Drug('Quetiapine', (89, 246, 246), dash=[2]),
    (281.4, 86.2, 0, 9.9): Drug('Imipramine', (121, 21, 142), dash=[2]),
    (264.4, 233.1, 0, 9.9): Drug('Nortryptiline', (218, 7, 158), dash=[2]),
    (301.7, 256.1, 0, 16.8): Drug('Temazepam', (242, 67, 19), dash=[2]),
    (285.7, 193.1, 0, 27.6): Drug('Diazepam', (242, 184, 19), dash=[2]),
}

def main():
    doc = Document(w=400, h=400)

    C = Chromatogram(400, 400)
    C.title.size += 3
    C.title.text = ''
    C.plot.extrema = 1000000000, 0, .01, 1.05
    # C.plot.extrema = .00000000001, 7.5, .01, 1.05

    entries = list(BrukerBatch(Path('C:\\Data\\Bruker\\test')).values())[0]

    for key, chrom in entries.items():
        if key in drugs_of_interest:
            drug = drugs_of_interest[key]
            chrom.label = drug.name
            chrom.gauss(1)
            chrom.normalize()
            chrom.rt_window(.15)
            C.add_curve(chrom, drug.color, dasharray=drug.dash)

    C.set()
    doc.addChild(C.root)

    return doc

d = main()
png(d, 'Bruker_1', 20)