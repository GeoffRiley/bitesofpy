import pytest

from Bio.Data.CodonTable import TranslationError

from translate_cds import translate_cds


# Note on Bio.Seq table ids: These can be found in the
# Seq.CodonTable.ambiguous_generic_by_name variable


@pytest.mark.parametrize(
    "cds,table,expected",
    [
        (
                "ATGCCCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Vertebrate Mitochondrial",
                "MPGKAHKKCSTPLHHPG",
        ),
        (
                "GTGCCCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Vertebrate Mitochondrial",
                "MPGKAHKKCSTPLHHPG",
        ),
        (
                "ATGCCCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Bacterial",
                "MPGKAHKKCSTPLHHPG",
        ),
        (
                "TTGCCCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Bacterial",
                "MPGKAHKKCSTPLHHPG",
        ),
        (
                "ATGCCCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTGA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),
        (
                "aTgCCcGGGAAAGCGCACaaGAAGTGCTCAACGccccTACATCATCCGGGGtaa",
                "Bacterial",
                "MPGKAHKKCSTPLHHPG",
        ),  # capitalization
        (
                "ATGCCRGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTGA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # ambiguous base R, solvable AA, CCR>P
        (
                "ATGCRCGGGAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTGA",
                "Standard",
                "MXGKAHKKCSTPLHHPG",
        ),  # ambiguous base R, ambiguous AA, CRC>X
        (
                "ATG CCC GGG AAA GCG CAC AAG AAG TGC TCA ACG CCC CTA CAT CAT CCG GGG TGA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # spaces
        (
                "ATG CCC GGG     AAAGCGCACAAGAAGTG CTCAACGCCCCTACATCATCCGGGG TAA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # multiple spaces
        (
                "ATGCCC\tGGG\tAAAGCGCACAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # tabs
        (
                "ATGCCCGGGAAAGCGCACAAGAAGTG\nCTCAACGCCCCTACATCATCCGGGGTAA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # newline
        (
                "ATGC\u00A0CCGGGAAAGCGCA\u2009CAAGAAGTGCTCAACGCCCCTACATCATCCGGGGTAA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # U+00A0: NO-BREAK SPACE; U+2009: THIN SPACE
        (
                "ATGC\u00A0CCG\tGGA AAG CGCA\u2009CAAGAAGTG\nCTCAACGC\tCCCTA\rCA TCA TCCGGGGTAA",
                "Standard",
                "MPGKAHKKCSTPLHHPG",
        ),  # lots of whitespace
    ],
)
def test_translate_cds(cds, table, expected):
    """
    Test if returned protein sequence and type are correct
    """
    result = translate_cds(cds, table)
    assert isinstance(result, str)
    assert result.upper() == expected


@pytest.mark.parametrize(
    "cds,table",
    [
        ("ATGAA", "Standard"),  # len % 3 != 0
        ("ATGAAA", "Standard"),  # last codon not stop codon
        ("TTTTAA", "Standard"),  # no start codon
        ("ATGTAATAA", "Standard"),  # internal stop codon
    ],
)
def test_translate_cds_fail(cds, table):
    """
    Test if function throws error when bad data is fed in
    """
    with pytest.raises(TranslationError):
        translate_cds(cds, table)
