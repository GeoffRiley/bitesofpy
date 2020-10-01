import pytest

import scoring_matrix

# Grabbed from ftp://ftp.ncbi.nih.gov/blast/matrices/PAM70
# Fixed width table with width of 4
PAM70 = """#
# This matrix was produced by "pam" Version 1.0.6 [28-Jul-93]
#
# PAM 70 substitution matrix, scale = ln(2)/2 = 0.346574
#
# Expected score = -2.77, Entropy = 1.60 bits
#
# Lowest score = -11, Highest score = 13
#
    A   R   N   D   C   Q   E   G   H   I   L   K   M   F   P   S   T   W   Y   V   B   Z   X   *
A   5  -4  -2  -1  -4  -2  -1   0  -4  -2  -4  -4  -3  -6   0   1   1  -9  -5  -1  -1  -1  -2 -11
R  -4   8  -3  -6  -5   0  -5  -6   0  -3  -6   2  -2  -7  -2  -1  -4   0  -7  -5  -4  -2  -3 -11
N  -2  -3   6   3  -7  -1   0  -1   1  -3  -5   0  -5  -6  -3   1   0  -6  -3  -5   5  -1  -2 -11
D  -1  -6   3   6  -9   0   3  -1  -1  -5  -8  -2  -7 -10  -4  -1  -2 -10  -7  -5   5   2  -3 -11
C  -4  -5  -7  -9   9  -9  -9  -6  -5  -4 -10  -9  -9  -8  -5  -1  -5 -11  -2  -4  -8  -9  -6 -11
Q  -2   0  -1   0  -9   7   2  -4   2  -5  -3  -1  -2  -9  -1  -3  -3  -8  -8  -4  -1   5  -2 -11
E  -1  -5   0   3  -9   2   6  -2  -2  -4  -6  -2  -4  -9  -3  -2  -3 -11  -6  -4   2   5  -3 -11
G   0  -6  -1  -1  -6  -4  -2   6  -6  -6  -7  -5  -6  -7  -3   0  -3 -10  -9  -3  -1  -3  -3 -11
H  -4   0   1  -1  -5   2  -2  -6   8  -6  -4  -3  -6  -4  -2  -3  -4  -5  -1  -4   0   1  -3 -11
I  -2  -3  -3  -5  -4  -5  -4  -6  -6   7   1  -4   1   0  -5  -4  -1  -9  -4   3  -4  -4  -3 -11
L  -4  -6  -5  -8 -10  -3  -6  -7  -4   1   6  -5   2  -1  -5  -6  -4  -4  -4   0  -6  -4  -4 -11
K  -4   2   0  -2  -9  -1  -2  -5  -3  -4  -5   6   0  -9  -4  -2  -1  -7  -7  -6  -1  -2  -3 -11
M  -3  -2  -5  -7  -9  -2  -4  -6  -6   1   2   0  10  -2  -5  -3  -2  -8  -7   0  -6  -3  -3 -11
F  -6  -7  -6 -10  -8  -9  -9  -7  -4   0  -1  -9  -2   8  -7  -4  -6  -2   4  -5  -7  -9  -5 -11
P   0  -2  -3  -4  -5  -1  -3  -3  -2  -5  -5  -4  -5  -7   7   0  -2  -9  -9  -3  -4  -2  -3 -11
S   1  -1   1  -1  -1  -3  -2   0  -3  -4  -6  -2  -3  -4   0   5   2  -3  -5  -3   0  -2  -1 -11
T   1  -4   0  -2  -5  -3  -3  -3  -4  -1  -4  -1  -2  -6  -2   2   6  -8  -4  -1  -1  -3  -2 -11
W  -9   0  -6 -10 -11  -8 -11 -10  -5  -9  -4  -7  -8  -2  -9  -3  -8  13  -3 -10  -7 -10  -7 -11
Y  -5  -7  -3  -7  -2  -8  -6  -9  -1  -4  -4  -7  -7   4  -9  -5  -4  -3   9  -5  -4  -7  -5 -11
V  -1  -5  -5  -5  -4  -4  -4  -3  -4   3   0  -6   0  -5  -3  -3  -1 -10  -5   6  -5  -4  -2 -11
B  -1  -4   5   5  -8  -1   2  -1   0  -4  -6  -1  -6  -7  -4   0  -1  -7  -4  -5   5   1  -2 -11
Z  -1  -2  -1   2  -9   5   5  -3   1  -4  -4  -2  -3  -9  -2  -2  -3 -10  -7  -4   1   5  -3 -11
X  -2  -3  -2  -3  -6  -2  -3  -3  -3  -3  -4  -3  -3  -5  -3  -1  -2  -7  -5  -2  -2  -3  -3 -11
* -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11 -11   1"""

# For this bite assume that the proteins are already aligned
# and that no gaps or insertions are present


sequence_pairs = [
    (
        "MSIQHFRVALIPFFAAFCLPVFAHPETLVKVKDAEDKLGARVGYIELDLNSGKILESFRPEERFPMMSTFKVLLCGAVLSRVDAG",
        "MSIaHFRVALIPFFAAFCLPVFAHPETLVKVKiAEDKLGARVGYIELDLNSGKILESFRPgERFPMMSTFKVLLCGAVLSRVDAG",
    ),
    (
        "QEQLGRRIHYSQNDLVEYSPVTEKHLTDGMTVRELCSAAITMSDNTAANLLLTTIGGPKELTAFLHNMGDHVTRLDRWEPELNEA",
        "QEaLGRRIHiSQNDLVEYpPVTEKHLTsGMTVRngCSAAITMSDNTppNLaaTTIGGlKELTAFLHNMGhHVTRLhRWEPELNiA",
    ),
    ("IPNDERDTTMPAAMATTLRKLLTGELLTLASRQQ", "IPNfnRDppMPppMpppLRKaaTGELgTLtSRdQ"),
    (
        "LIDWMEADKVAGPLLRSALPAGWFIADKSGAGERGSRGIIAALGPDGKPSRIVVIYTTGSQATMDERNRQIAEIGASLIKHW",
        "LIDWMsADKpGaqLLRSALPaAfFIADKdGgGfeGSRGggppLGPDGKPSRIttIYTTGSQpTiDEpNReIAEIGASLIKHW",
    ),
]

HUMAN_INSULIN = "malwmrllpllallalwgpdpaaafvnqhlcgshlvealylvcgergffytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycn"

INSULIN_VARIANTS_TIES = [
    "mQlwmrllpllallalwgpdpaaaDvnqhlcgshlvealylvcgergDDytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycn",
    # Tie
    "mIlwmrllpllallalwgpdpaaaDvnqhlcgshlvealylvcgergDDytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycn",
    # Tie
    "mRlwmrllpllallalwgpdpaaaDvnqhlcgshlvealylvcgergDDytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycn",
    # Ties in BLOSUM62 but not PAM70
    "mWlwmrllpllallalwgpdpaaaDvnqhlcgshlvealylvcgergDDytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycn",
    # Lower in all
]

INSULIN_BEST_SCORING = [
    "malwmrllpllallalwgpdpaaafvnqhlcgshlvealylvcgergffytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsicslyqlenycD",
    # PAM70
    "malwmrllpllallalwgpdpaaafvnqhlcgshlvealylvcgergffytpktrreaedlqvgqvelgggpgagslqplalegslqkrgiveqcctsVcslyqlenycn",
    # BLOSUM62
]

INSULIN_VARIANTS_NO_TIE = INSULIN_VARIANTS_TIES + INSULIN_BEST_SCORING


@pytest.mark.parametrize(
    "seqs,matrix,expected_score",
    list(
        zip(
            sequence_pairs,
            [scoring_matrix.BLOSUM62] * len(sequence_pairs),
            [412, 355, 86, 304],
        )
    )
    + list(zip(sequence_pairs, [PAM70] * len(sequence_pairs), [530, 438, 105, 363])),
)
def test_matrix_score(seqs, matrix, expected_score):
    """
    Test if the matrix_score function returns the correct value
    """
    seq1, seq2 = seqs
    assert scoring_matrix.matrix_score(seq1, seq2, matrix) == expected_score


def test_matrix_score_error():
    """
    Check if inputting an invalid character raises and error
    """
    with pytest.raises(KeyError) as kerr:
        scoring_matrix.matrix_score("MAAAAG", "MAAAAO", PAM70)

    assert (
            repr(kerr.value)
            == "AminoAcidNotFoundError(\"Scoring matrix does not support scoring for: ('G', 'O')\")"
    )


@pytest.mark.parametrize(
    "matrix,index_best", [(scoring_matrix.BLOSUM62, -1), (PAM70, -2)]
)
def test_best_hit(matrix, index_best):
    """
    Check if the correct best hit is returned
    """
    best_hit = scoring_matrix.closest_match(
        HUMAN_INSULIN, INSULIN_VARIANTS_NO_TIE, matrix
    )
    assert isinstance(best_hit, str)
    assert best_hit.upper() == INSULIN_VARIANTS_NO_TIE[index_best].upper()


@pytest.mark.parametrize("matrix,to_index", [(scoring_matrix.BLOSUM62, 3), (PAM70, 2)])
def test_best_hit_ties(matrix, to_index):
    """
    Check if multiple best hits are dealt with correctly
    """
    best_hits = scoring_matrix.closest_match(
        HUMAN_INSULIN, INSULIN_VARIANTS_TIES, matrix
    )
    assert isinstance(best_hits, list)
    assert sorted([s.upper() for s in best_hits]) == sorted(
        [s.upper() for s in INSULIN_VARIANTS_TIES[:to_index]]
    )


def test_best_hit_none():
    """
    Test if empty query returns a None
    """
    assert scoring_matrix.closest_match("AAA", []) is None


def test_best_hit_single_invalid_sequence():
    """
    Check if the sequence is validated if only one sequence is input
    """
    with pytest.raises(KeyError) as kerr:
        scoring_matrix.closest_match("MAAAAG", ["MAAAAO"], PAM70)

    assert (
            repr(kerr.value)
            == "AminoAcidNotFoundError(\"Scoring matrix does not support scoring for: ('G', 'O')\")"
    )
