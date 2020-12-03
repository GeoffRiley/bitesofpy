import re
from typing import List, Tuple

NAME_PATTERN = r'^(.*_S\d{1,2}_L\d{3}_R)([12])(_\d{3}.fastq.gz)$'
NAME_CHECKER = re.compile(NAME_PATTERN, re.IGNORECASE)


def check_filename(fname: str) -> bool:
    return NAME_CHECKER.match(fname) is not None


def standardise_file(fname: str) -> str:
    return NAME_CHECKER.sub(r'\1N\3', fname).lower()


def pair_files(filenames: List[str]) -> List[Tuple[str, str]]:
    """
    Function that pairs filenames

    filenames: list[str] containing filenames
    returns: list[tuple[str, str]] containing filename pairs
    """
    sorted_files = sorted([(standardise_file(f), f) for f in filenames if check_filename(f)],
                          key=lambda x: x[1].lower())
    result = []
    for file_a, file_b in zip(sorted_files[:-1], sorted_files[1:]):
        if file_a[0] == file_b[0]:
            result.append((file_a[1], file_b[1]))
    return result


# Set up for your convenience during testing
if __name__ == "__main__":
    filenames = [
        "Sample1_S1_L001_R1_001.FASTQ.GZ",
        "Sample1_S1_L001_R2_001.fastq.gz",
        "Sample2_S2_L001_R1_001.fastq.gz",
        "sample2_s2_l001_r2_001.fastq.gz",
    ]
    # ('Sample1_S1_L001_R1_001.FASTQ.GZ', 'Sample1_S1_L001_R2_001.fastq.gz')
    # ('Sample2_S2_L001_R1_001.fastq.gz', 'sample2_s2_l001_r2_001.fastq.gz')

    for pair in pair_files(filenames):
        print(pair)
