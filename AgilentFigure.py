from pathlib import Path
from pyChroms import AgilentBatch
from pyChroms.figures.DefaultChromatogram import Chromatogram
from pyChroms.structs.drug import Drug

from PSVG import Document
from pyChroms.export import png


drugs_of_interest = {
    (286.2, 164.8, 135.0, 55.0): Drug('Morphine', (9, 151, 214)),
    (328.2, 310.2, 135.0, 21.0): Drug('Naloxone', (7, 216, 121)),
    (328.2, 165.0, 164.0, 45.0): Drug('6-MAM', (89, 246, 246)),
    (150.1, 119.0, 120.0, 9.0): Drug('Methamphetamine', (121, 21, 142)),
    (264.2, 58.3, 140.0, 10.0): Drug('Tramadol', (218, 7, 158)),
    (248.2, 220.0, 138.0, 21.0): Drug('Meperidine', (242, 67, 19)),
    (219.1, 97.1, 100.0, 9.0): Drug('Meprobamate', (242, 184, 19)),
    (244.2, 86.2, 90.0, 9.0): Drug('Phencyclidine', (47, 51, 53)),
    (337.2, 105.1, 130.0, 45.0): Drug('Fentanyl', (9, 151, 214), dash=[2]),
    (278.2, 234.1, 60.0, 33.0): Drug('EDDP', (7, 216, 121), dash=[2]),
    (384.2, 253.0, 35.0, 17.0): Drug('Quetiapine', (89, 246, 246), dash=[2]),
    (281.2, 86.2, 40.0, 17.0): Drug('Imipramine', (121, 21, 142), dash=[2]),
    (264.2, 233.0, 112.0, 13.0): Drug('Nortryptiline', (218, 7, 158), dash=[2]),
    (301.1, 255.0, 132.0, 13.0): Drug('Temazepam', (242, 67, 19), dash=[2]),
    (285.1, 193.0, 154.0, 33.0): Drug('Diazepam', (242, 184, 19), dash=[2]),
}




def main():
    doc = Document(w=400, h=400)

    C = Chromatogram(400, 400)
    C.title.size += 3
    C.title.text = ''
    C.plot.extrema = 1000000000, 0, .01, 1.05
    # C.plot.extrema = .00000000001, 7.5, .01, 1.05

    entries = list(AgilentBatch(Path('C:\\Data\\Agilent\\test')).values())[0]
    for key, chrom in entries.items():
        if key in drugs_of_interest:
            drug = drugs_of_interest[key]
            chrom.label = drug.name
            chrom.gauss(1)
            chrom.normalize()
            chrom.rt_window(.25)
            C.add_curve(chrom, drug.color, dasharray=drug.dash)

    C.set()
    doc.addChild(C.root)

    return doc

d = main()
png(d, 'Agilent_1', 20)