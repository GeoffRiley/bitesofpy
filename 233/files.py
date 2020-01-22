from datetime import datetime
from pathlib import Path, PosixPath
from zipfile import ZipFile

TMP = Path('/tmp')
LOG_DIR = TMP / 'logs'
ZIP_FILE = 'logs.zip'


def zip_last_n_files(directory: PosixPath = LOG_DIR,
                     zip_file: str = ZIP_FILE, n: int = 3):
    file_list = {}
    for f in directory.glob('*.log'):
        s = f.stat()
        file_list[s.st_ctime] = f
    file_list = sorted(file_list.items())
    with ZipFile(zip_file, 'w') as zippery:
        for t, f in file_list[-n:]:
            zippery.write(f, f'{f.stem}_{datetime.fromtimestamp(t).strftime("%Y-%m-%d")}.log')
            # f'{f.stem}-{datetime.fromtimestamp(s.st_ctime).strftime("%Y-%m-%d")}.log'
