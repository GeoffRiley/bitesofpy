import pathlib
import re
from typing import Union, Dict, List, IO

# Extracted from https://en.wikipedia.org/wiki/List_of_file_signatures
MAGIC_IMAGE_TABLE = """
"magic_bytes","text_representation","offset","extension","description"
"47 49 46 38 37 61
47 49 46 38 39 61","GIF87a
GIF89a",0,"gif","Image file encoded in the Graphics Interchange Format (GIF)"
"FF D8 FF DB
FF D8 FF E0 00 10 4A 46 49 46 00 01
FF D8 FF EE
FF D8 FF E1 ?? ?? 45 78 69 66 00 00","ÿØÿÛ
ÿØÿà..JFIF..
ÿØÿîÿØÿá..Exif..",0,"jpg
jpeg","JPEG raw or in the JFIF or Exif file format"
"89 50 4E 47 0D 0A 1A 0A",".PNG....",0,"png","Image encoded in the Portable Network Graphics format"
"49 49 2A 00 (little-endian format)
4D 4D 00 2A (big-endian format)","II*.MM.*",0,"tif
tiff","Tagged Image File Format (TIFF)"
"50 31 0A","P1.",0,"pbm","Portable bitmap"
"""  # noqa: E501


# Checking on the wikipedia page, the text representation for jpeg is incorrect,
# the final two entries have been combined into a single entry.
# ÿØÿÛ
# ÿØÿà..JFIF..
# ÿØÿî
# ÿØÿá..Exif..
# The fault lies with the wiki formatting—correction submitted to WP.


class FileNotRecognizedException(Exception):
    """
    File cannot be identified using a magic table
    """


def parse_lookup_table(lookup_table_string: str) -> List[Dict[str, Union[int, str, List[str]]]]:
    """
    lookup_table_string: a comma separated text containing a magic table

    Returns: list of table entries as dictionaries
    """
    # The standard csv library does not handle embedded cr/lf within fields
    # so it is necessary that we spin our own.
    # The 'strip()' is just to get rid of leading and trailing whitespace
    lines = lookup_table_string.strip().splitlines(keepends=False)
    # First line has the field names
    fieldnames = list(map(lambda x: x.strip('"'), lines.pop(0).split(',')))

    results = []
    # the rest of the lines are the data
    while len(lines):
        in_quote = False
        record = {}
        line = lines.pop(0)
        for field in fieldnames:
            pos = 0
            f_start = f_end = pos
            while pos < len(line):
                if line[pos] == '"':
                    if not in_quote:
                        f_start = pos + 1
                    else:
                        f_end = pos
                    in_quote = not in_quote
                    pos += 1
                    continue
                if in_quote:
                    pos += 1
                    if pos >= len(line):
                        line = f'{line}\n{lines.pop(0)}'
                    continue
                if line[pos] == ',':
                    if f_start == f_end:
                        record[field] = int(line[:pos])
                    else:
                        entry = line[f_start:f_end]
                        if field == 'magic_bytes':
                            entry = re.sub(r'\([^)]+\)', r'', entry)
                        if field == 'offset':
                            entry = int(entry)
                        elif '\n' in entry:
                            entry = list(map(str.strip, entry.split('\n')))
                        record[field] = entry
                    pos += 1
                    line = line[pos:]
                    break
                pos += 1
            if field not in record:
                record[field] = line[f_start:f_end]
        results.append(record)
    return results


def read_bytes(fh: IO, start_pos: int, chunked: int = 1024):
    fh.seek(start_pos)
    buffer = '??'
    while len(buffer) > 0:
        buffer = fh.read(chunked)
        for b in buffer:
            yield f'{b:02X}'


def determine_filetype_by_magic_bytes(
        file_name: Union[str, pathlib.Path],
        lookup_table_string: str = MAGIC_IMAGE_TABLE,
) -> str:
    """
    file_name: file name with path
    lookup_table_string: a comma separated text containing a magic table

    Returns: file format based on the magic bytes
    """
    lookup_table = parse_lookup_table(lookup_table_string)
    with open(file_name, 'rb') as fh:
        for suspect in lookup_table:
            matches = [suspect['magic_bytes']] if type(suspect['magic_bytes']) == str else suspect['magic_bytes']
            for b in read_bytes(fh, suspect['offset']):
                new_matches = []
                for mn in range(len(matches)):
                    m = matches[mn].split(maxsplit=1)
                    if m[0] == '??' or b == m[0]:
                        if len(m) == 1:
                            return suspect['description']
                        new_matches.append(m[1])
                if len(new_matches):
                    matches = new_matches
                else:
                    break

    raise FileNotRecognizedException()


# Set up for your convenience when coding:
#  - creates a test_image.gif GIF file
#  - calls determine_filetype_by_magic_bytes
#  - prints out file type
if __name__ == "__main__":
    test_filename = "test_image.gif"
    print(f"Script invoked directly. Writing out test file {test_filename}")
    with open(test_filename, "wb") as f:
        f.write(
            b"\x47\x49\x46\x38\x37\x61\x01\x00x01\x00\x80\x00\x00\xff\xff\xff"
            b"\xff\xff\xff\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02"
            b"\x44\x01\x00\x3b"
        )
    print("Testing file format")
    print(determine_filetype_by_magic_bytes(test_filename))
