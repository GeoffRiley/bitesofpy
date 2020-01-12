import re

import codon_usage
import pytest

EXPECTED = """
|  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |  Codon AA  Freq  Count  |
---------------------------------------------------------------------------------------------------------
|  UUU:  F   32.7  26200  |  UCU:  S   12.9  10309  |  UAU:  Y   30.4  24332  |  UGU:  C    4.9   3919  |
|  UUC:  F   12.1   9716  |  UCC:  S    1.6   1310  |  UAC:  Y    8.6   6887  |  UGC:  C    1.2    992  |
|  UUA:  L   53.8  43053  |  UCA:  S   20.3  16267  |  UAA:  *    2.4   1909  |  UGA:  *    0.4    299  |
|  UUG:  L   13.5  10801  |  UCG:  S    4.0   3172  |  UAG:  *    0.5    405  |  UGG:  W    7.6   6055  |
---------------------------------------------------------------------------------------------------------
|  CUU:  L   10.6   8462  |  CCU:  P   10.8   8642  |  CAU:  H   18.2  14550  |  CGU:  R   13.2  10569  |
|  CUC:  L    1.9   1560  |  CCC:  P    1.0    773  |  CAC:  H    4.5   3625  |  CGC:  R    3.1   2512  |
|  CUA:  L    8.5   6808  |  CCA:  P   16.3  13009  |  CAA:  Q   36.3  29048  |  CGA:  R    4.9   3914  |
|  CUG:  L    2.3   1826  |  CCG:  P    4.1   3262  |  CAG:  Q    5.0   3977  |  CGG:  R    0.4    348  |
---------------------------------------------------------------------------------------------------------
|  AUU:  I   52.0  41646  |  ACU:  T   16.8  13481  |  AAU:  N   43.0  34398  |  AGU:  S   16.7  13345  |
|  AUC:  I   14.9  11905  |  ACC:  T    2.6   2077  |  AAC:  N   13.9  11135  |  AGC:  S    5.2   4152  |
|  AUA:  I   18.8  15063  |  ACA:  T   28.9  23134  |  AAA:  K   61.1  48950  |  AGA:  R   11.7   9372  |
|  AUG:  M   25.9  20717  |  ACG:  T    9.5   7638  |  AAG:  K   14.3  11428  |  AGG:  R    1.5   1217  |
---------------------------------------------------------------------------------------------------------
|  GUU:  V   27.4  21938  |  GCU:  A   20.4  16291  |  GAU:  D   45.6  36531  |  GGU:  G   32.6  26104  |
|  GUC:  V    7.3   5873  |  GCC:  A    4.4   3507  |  GAC:  D   12.8  10229  |  GGC:  G    9.4   7525  |
|  GUA:  V   22.8  18270  |  GCA:  A   29.9  23954  |  GAA:  E   54.6  43675  |  GGA:  G   14.2  11399  |
|  GUG:  V    9.5   7584  |  GCG:  A    9.4   7550  |  GAG:  E   10.6   8458  |  GGG:  G    4.4   3483  |
---------------------------------------------------------------------------------------------------------
""".strip()  # noqa E501


# ############################################################################
# Helper functions
# ############################################################################


def get_whole_table(table):
    """
    Receives a results table
    Returns all results in a list of lists with whitespace removed
    """
    return [
        entry.strip().split()
        for line in table.strip().split("\n")
        for entry in line.split("|")
        if entry.replace("-", "") != "" and entry.strip() != ""
    ]


def get_field(table, field_number):
    """
    Helper function to get a specific field from table
    Receives a results table
    Returns a list of queried field
    """
    return [entry[field_number] for entry in get_whole_table(table)]


def get_codons(table):
    """
    Get field "codons" from table
    Receives a results table
    Returns a list of queried field
    """
    return get_field(table, 0)


def get_amino_acids(table):
    """
    Get field "amino acids" from table
    Receives a results table
    Returns a list of amino acids
    """
    return get_field(table, 1)


def get_frequencies(table):
    """
    Get field "frequencies" from table
    Receives a results table
    Returns a list of frequencies
    """
    return get_field(table, 2)


def get_absolute_numbers(table):
    """
    Get field "absolute numbers" from table
    Receives a results table
    Returns a list of absolute codon numbers
    """
    return get_field(table, 3)


def get_table_bars(table):
    """
    Receives a results table
    Returns a list of bars/pipes (|) per line
    """
    return [len(re.findall(r"\|", line)) for line in table.split("\n")]


def get_table_dividers(table):
    """
    Receives a results table
    Returns a list of divider rows (------)
    """
    return [len(re.findall(r"^-{3,}$", line)) for line in table.split("\n")]


# ############################################################################
# Test functions
# ############################################################################


@pytest.fixture(scope="module")
def result():
    """
    Provide codon usage table for tests
    """
    return codon_usage.return_codon_usage_table().strip()


@pytest.mark.parametrize(
    "function",
    [
        get_table_bars,
        get_table_dividers,
        get_codons,
        get_amino_acids,
        get_frequencies,
        get_absolute_numbers,
        get_whole_table,
    ],
)
def test_table(result, function):
    """
    Helper function to run all tests
    """
    print(f"Executing function '{function.__name__}'")
    assert function(result) == function(EXPECTED)
