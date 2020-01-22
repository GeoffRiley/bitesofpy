import re
from pathlib import Path
from time import sleep
from zipfile import ZipFile

from files import zip_last_n_files, ZIP_FILE

TMP = Path('/tmp')
LOG_DIR = TMP / 'logs'


def test_zip_3_last_files(tmp_path):
    log_dir = tmp_path / "logs"
    log_dir.mkdir()
    for i in range(1, 10, 2):
        sleep(0.01)
        p = log_dir / f"{i}.log"
        p.write_text('log line')
    zip_file = tmp_path / ZIP_FILE
    zip_last_n_files(directory=log_dir, zip_file=zip_file)
    zip_ = ZipFile(zip_file)
    files = sorted(zip_.namelist())
    assert len(files) == 3
    f1, f2, f3 = files
    assert re.match(r'^5_\d{4}-\d{2}-\d{2}.log$', f1)
    assert re.match(r'^7_\d{4}-\d{2}-\d{2}.log$', f2)
    assert re.match(r'^9_\d{4}-\d{2}-\d{2}.log$', f3)


def test_zip_2_last_files(tmp_path):
    log_dir = tmp_path / "logs2"
    log_dir.mkdir()
    for i in range(20, 6, -3):
        sleep(0.01)
        p = log_dir / f"{i}.log"
        p.write_text('log line')
    zip_file = tmp_path / ZIP_FILE
    zip_last_n_files(directory=log_dir, zip_file=zip_file, n=2)
    zip_ = ZipFile(zip_file)
    files = sorted(zip_.namelist())
    assert len(files) == 2
    f1, f2 = files
    assert re.match(r'^11_\d{4}-\d{2}-\d{2}.log$', f1)
    assert re.match(r'^8_\d{4}-\d{2}-\d{2}.log$', f2)
