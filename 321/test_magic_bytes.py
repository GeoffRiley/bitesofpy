import pathlib

import pytest

from magic_bytes import (
    determine_filetype_by_magic_bytes,
    FileNotRecognizedException,
    MAGIC_IMAGE_TABLE,
)

CUSTOM_MAGIC_TABLE2 = """
"magic_bytes","text_representation","offset","extension","description"
"01 70 79 62 69 74 65 73 00 01 22 ?? ?? ?? 66 6F 72 6D 61 74 (little endian)
01 70 79 62 69 74 65 73 01 00 22 ?? ?? ?? 66 6F 72 6D 61 74 (big endian)",".pybites..""...format
.pybites..""...format","1","pybites
pbf2","Fantasy pybites file format"
"""  # noqa: E501


def create_test_file(
        tmp_dir: pathlib.Path, file_type: str, data: bytes
) -> pathlib.Path:
    """
    Write out temporary test files used in tests

    tmp_dir: pytest.tmpdir fixture: temporary directory
    file_type: file type, used as file extension
    data: file data

    returns file path of file written
    """
    file_name = tmp_dir / f"image.{file_type}"
    with open(file_name, "wb") as data_file:
        data_file.write(data)
    return file_name


@pytest.mark.parametrize(
    "file_type, file_data, magic_table, expected_description",
    [
        (
                "gif_file",
                (
                        b"GIF87a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\xff\xff\xff,"
                        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
                ),
                MAGIC_IMAGE_TABLE,
                "Image file encoded in the Graphics Interchange Format (GIF)",
        ),
        (
                "png_file",
                (
                        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00"
                        b"\x00\x01\x08\x04\x00\x00\x00\xb5\x1c\x0c\x02\x00\x00\x00"
                        b"\x0bIDATx\xdac\xfc\xff\x1f\x00\x03\x03\x02\x00\xef\xa2\xa7["
                        b"\x00\x00\x00\x00IEND\xaeB`\x82"
                ),
                MAGIC_IMAGE_TABLE,
                "Image encoded in the Portable Network Graphics format",
        ),
        (
                "tiff_files",
                (
                        b"II*\x00\x0c\x00\x00\x00\xff\xff\xff\x00\x10\x00\x00\x01\x03"
                        b"\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x01\x03\x00\x01"
                        b"\x00\x00x00\x01\x00\x00\x00\x02\x01\x03\x00\x03\x00\x00\x00"
                        b"\xe2\x00\x00\x00\x03\x01\x03\x00\x01\x00\x00\x00\x01\x00"
                        b"\x00\x00\x06\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00"
                        b"\x11\x01\x04\x00\x01\x00\x00\x00\x08\x00\x00\x00\x12\x01"
                        b"\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x15\x01\x03\x00"
                        b"\x01\x00\x00\x00\x03\x00\x00\x00\x16\x01\x03\x00\x01\x00"
                        b"\x00\x00\x80\x00\x00\x00\x17\x01\x04\x00\x01\x00\x00\x00"
                        b"\x03\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00\xd2\x00"
                        b"\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00\xda\x00\x00\x00"
                        b"\x1c\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00\x1d\x01"
                        b"\x02\x00\x0b\x00\x00\x00\xee\x00\x00\x00(\x01\x03\x00\x01"
                        b"\x00\x00\x00\x02\x00\x00\x00S\x01\x03\x00\x03\x00\x00\x00"
                        b"\xe8\x00\x00\x00\x00\x00\x00\x00,\x01\x00\x00\x01\x00\x00"
                        b"\x00,\x01\x00\x00\x01\x00\x00\x00\x08\x00\x08\x00\x08\x00"
                        b"\x01\x00\x01\x00\x01\x00Background\x00"
                ),
                MAGIC_IMAGE_TABLE,
                "Tagged Image File Format (TIFF)",
        ),
        (
                "pbm_file",
                b"P1\n# PyBites\n1 1\n0",
                MAGIC_IMAGE_TABLE,
                "Portable bitmap",
        ),
        (
                "jpg_file",
                (
                        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x01,\x01,\x00"
                        b"\x00\xff\xdb\x00C\x00\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xff"
                        b"\xdb\x00C\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\xff\xc0\x00"
                        b"\x11\x08\x00\x01\x00\x01\x03\x01\x11\x00\x02\x11\x01\x03"
                        b"\x11\x01\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01"
                        b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04"
                        b"\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x10\x00\x02\x01"
                        b"\x03\x03\x02\x04\x03\x05\x05\x04\x04\x00\x00\x01}\x01"
                        b'\x02\x03\x00\x04\x11\x05\x12!1A\x06\x13Qa\x07"q\x142'
                        b"\x81\x91\xa1\x08#B\xb1\xc1\x15R\xd1\xf0$3br\x82\t\n\x16\x17"
                        b"\x18\x19\x1a%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz"
                        b"\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96\x97"
                        b"\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2\xb3"
                        b"\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7\xc8"
                        b"\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe1\xe2\xe3"
                        b"\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf1\xf2\xf3\xf4\xf5\xf6\xf7"
                        b"\xf8\xf9\xfa\xff\xc4\x00\x1f\x01\x00\x03\x01\x01\x01\x01"
                        b"\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x02\x03"
                        b"\x04\x05\x06\x07\x08\t\n\x0b\xff\xc4\x00\xb5\x11\x00\x02"
                        b"\x01\x02\x04\x04\x03\x04\x07\x05\x04\x04\x00\x01\x02w\x00"
                        b'\x01\x02\x03\x11\x04\x05!1\x06\x12AQ\x07aq\x13"2\x81\x08'
                        b"\x14B\x91\xa1\xb1\xc1\t#3R\xf0\x15br\xd1\n\x16$4\xe1%\xf1"
                        b"\x17\x18\x19\x1a&'()*56789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz"
                        b"\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x92\x93\x94\x95\x96"
                        b"\x97\x98\x99\x9a\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xb2"
                        b"\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xc2\xc3\xc4\xc5\xc6\xc7"
                        b"\xc8\xc9\xca\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xe2\xe3"
                        b"\xe4\xe5\xe6\xe7\xe8\xe9\xea\xf2\xf3\xf4\xf5\xf6\xf7\xf8"
                        b"\xf9\xfa\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00?"
                        b"\x00\xfe\xfe(\x03\xff\xd9"
                ),
                MAGIC_IMAGE_TABLE,
                "JPEG raw or in the JFIF or Exif file format",
        ),
        (
                "jpg_exif_stub",
                b"\xff\xd8\xff\xe1f\x10Exif\x00\x00\x00",
                MAGIC_IMAGE_TABLE,
                "JPEG raw or in the JFIF or Exif file format",
        ),
        (
                "pybites_format_variant_1",
                (
                        b'\xff\x01pybites\x00\x01"\x99\xaa\xbbformat\x00\x00\x00\x00'
                        b"\x00\x00"
                ),
                CUSTOM_MAGIC_TABLE2,
                "Fantasy pybites file format",
        ),
        (
                "pybites_format_variant_2",
                (
                        b'\xff\x01pybites\x01\x00"\x99\xcc\xddformat\x00\x00\x00\x00'
                        b"\x00\x00"
                ),
                CUSTOM_MAGIC_TABLE2,
                "Fantasy pybites file format",
        ),
        (
                "pybites_format_variant_3",
                (
                        b'\xee\x01pybites\x00\x01"\x00\xec\xedformat\x01\x00\x00\x00'
                        b"\x00\x01"
                ),
                CUSTOM_MAGIC_TABLE2,
                "Fantasy pybites file format",
        ),
    ],
)
def test_files_by_magic_bytes(
        tmpdir: pathlib.Path,
        file_type: str,
        file_data: bytes,
        magic_table: str,
        expected_description: str,
) -> None:
    """
    Tests if file types can  can be identified correctly

    tmpdir: pytest.tmpdir fixture
    file_type: type of file, used as file extension
    file_data: data for test files
    magic_table: csv string of magic table with columns
        "magic_bytes","text_representation","offset","extension","description"
    expected_description: expected description
    """

    file_name = create_test_file(tmpdir, file_type, file_data)
    result = determine_filetype_by_magic_bytes(file_name, magic_table)
    assert result == expected_description


@pytest.mark.parametrize(
    "file_type, file_data, magic_table",
    [
        (
                "text_file1",
                b"PYBITES FILE http://codechalleng.es\n",
                MAGIC_IMAGE_TABLE,
        ),
        (
                "corrupted pybites_format",
                (
                        b'\xee\x01pyb1tes\x00\x01"\x99\xec\xedf0rm4t\x01\x00\x00\x00'
                        b"\x00\x01"
                ),
                CUSTOM_MAGIC_TABLE2,
        ),
    ],
)
def test_magic_bytes_fail(
        tmpdir: pathlib.Path, file_type: str, file_data: bytes, magic_table: str
) -> None:
    """
    Tests for fails with unrecognized file formats

    tmpdir: pytest.tmpdir fixture
    file_type: str: type of file, used as file extension
    file_data: byte string: data for test files
    magic_table: str: csv string of magic table with columns
        "magic_bytes","text_representation","offset","extension","description"
    """
    file_name = create_test_file(tmpdir, file_type, file_data)

    with pytest.raises(FileNotRecognizedException):
        determine_filetype_by_magic_bytes(file_name, magic_table)
