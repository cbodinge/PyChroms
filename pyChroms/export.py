from PSVG import Document
from subprocess import run
from pathlib import Path

def png(document: Document, filename: str, zoom: float=1.0):
    # Save Document as a Dummy File
    with open('dummy.svg', 'w') as file:
        file.write(document.construct())

    path1 = Path.cwd() / 'dummy.svg'
    path2 = Path.cwd() / f'{filename}.png'

    run(['wkhtmltoimage', f'--zoom', f'{zoom}', '--width', f'{document.root.w}',
         str(path1.absolute()), str(path2.absolute())], shell=True)

