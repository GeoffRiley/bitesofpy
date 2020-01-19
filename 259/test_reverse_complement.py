import pytest

import reverse_complement

# Table copied from
# http://arep.med.harvard.edu/labgc/adnan/projects/Utilities/revcomp.html
# Note that this table is different from the simple table in the template
# This table includes additional rules which are used in more advanced
# reverse complement generators. Please ensure that your functions work
# with both tables (complementary base always in last column)

COMPLEMENTS_STR = """# Full table with ambigous bases
 Base	Name	Bases Represented	Complementary Base
 A	Adenine	A	T
 T	Thymidine	T 	A
 U	Uridine(RNA only)	U	A
 G	Guanidine	G	C
 C	Cytidine	C	G
 Y	pYrimidine	C T	R
 R	puRine	A G	Y
 S	Strong(3Hbonds)	G C	S
 W	Weak(2Hbonds)	A T	W
 K	Keto	T/U G	M
 M	aMino	A C	K
 B	not A	C G T	V
 D	not C	A G T	H
 H	not G	A C T	D
 V	not T/U	A C G	B
 N	Unknown	A C G T	N
"""

# ############################################################################
# Use default table from bite template and test functions
# ############################################################################

ACGT_BASES_ONLY = [
    "ACGT",
    "TTTAAAGGGCCC",
    ("TACTGGTACTAATGCCTAAGTGACCGGCAGCAAAATGTTGCAGCACTGACCCTTTTGGGACCGCAATGGGT"
     "TGAATTAGCGGAACGTCGTGTAGGGGGAAAGCGGTCGACCGCATTATCGCTTCTCCGGGCGTGGCTAGCGG"
     "GAAGGGTTGTCAACGCGTCGGACTTACCGCTTACCGCGAAACGGACCAAAGGCCGTGGTCTTCGCCACGGC"
     "CTTTCGACCGACCTCACGCTAGAAGGA"),
]
MIXED_CASE_DNA = [
    "AcgT",
    "TTTaaaGGGCCc",
    ("TACtGGTACTAATGCCtAAGtGaccggcagCAAAATGTTGCAGCACTGACCCTTTTGGGACCGCAATGGGT"
     "TGAATTAGCGGAACGTCGTGTAGGGGGAAAgcgGTCGACCGCATTATCGCTTCTCCGGGCGTGGCTAGCGG"
     "GAAGGGTTGTCAACGCGTCGGACTTACCGCttaCCGCGAAACGGAccAAAGGCCGTGGTCTTCGCCACGGC"
     "CTTtcGACCGACCTCACGCTAGAAGGA"),
]
DIRTY_DNA = [
    "335>\nA c g T",
    ">\nT-TT-AAA-  GGGCCC!!!",
    ("TAC TGG TAC TAA TGC CTA AGT GAC CGG CAG CAA AAT GTT GCA GCA CTG ACC CTT"
     " TTG GGA CCG CAA TGG GTT GAA TTA GCG GAA CGT CGT GTA GGG GGA AAG CGG TC"
     "G ACC GCA TTA TCG CTT CTC CGG GCG TGG CTA GCG GGA AGG GTT GTC AAC GCG T"
     "CG GAC TTA CCG CTT ACC GCG AAA CGG ACC AAA GGC CGT GGT CTT CGC CAC GGC "
     "CTT TCG ACC GAC CTC ACG CTA GAA GGA"),
]

CORRECT_ANSWERS_COMPLEMENTED = [
    "TGCA",
    "AAATTTCCCGGG",
    ("ATGACCATGATTACGGATTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCA"
     "ACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGGCCCGCACCGATCGCC"
     "CTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCTGGTTTCCGGCACCAGAAGCGGTGCCG"
     "GAAAGCTGGCTGGAGTGCGATCTTCCT"),
]
CORRECT_ANSWERS_REVERSE = [
    "TGCA",
    "CCCGGGAAATTT",
    ("AGGAAGATCGCACTCCAGCCAGCTTTCCGGCACCGCTTCTGGTGCCGGAAACCAGGCAAAGCGCCATTCGC"
     "CATTCAGGCTGCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCTCTTCGCTATTACGCCAGCTGGCGAAA"
     "GGGGGATGTGCTGCAAGGCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTGTAAAACGAC"
     "GGCCAGTGAATCCGTAATCATGGTCAT"),
]
CORRECT_ANSWERS_REVERSE_COMPLEMENT = [
    "ACGT",
    "GGGCCCTTTAAA",
    ("TCCTTCTAGCGTGAGGTCGGTCGAAAGGCCGTGGCGAAGACCACGGCCTTTGGTCCGTTTCGCGGTAAGCG"
     "GTAAGTCCGACGCGTTGACAACCCTTCCCGCTAGCCACGCCCGGAGAAGCGATAATGCGGTCGACCGCTTT"
     "CCCCCTACACGACGTTCCGCTAATTCAACCCATTGCGGTCCCAAAAGGGTCAGTGCTGCAACATTTTGCTG"
     "CCGGTCACTTAGGCATTAGTACCAGTA"),
]


# ############################################################################
# Test complement function
# ############################################################################


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(ACGT_BASES_ONLY, CORRECT_ANSWERS_COMPLEMENTED),
)
def test_acgt_complement(input_sequence, expected):
    assert reverse_complement.complement(input_sequence).upper() == expected


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(MIXED_CASE_DNA, CORRECT_ANSWERS_COMPLEMENTED),
)
def test_mixed_case_complement(input_sequence, expected):
    assert reverse_complement.complement(input_sequence).upper() == expected


@pytest.mark.parametrize(
    "input_sequence,expected", zip(DIRTY_DNA, CORRECT_ANSWERS_COMPLEMENTED)
)
def test_dirty_complement(input_sequence, expected):
    assert reverse_complement.complement(input_sequence).upper() == expected


# ############################################################################
# Test reverse function
# ############################################################################


@pytest.mark.parametrize(
    "input_sequence,expected", zip(ACGT_BASES_ONLY, CORRECT_ANSWERS_REVERSE)
)
def test_acgt_reverse(input_sequence, expected):
    assert reverse_complement.reverse(input_sequence).upper() == expected


@pytest.mark.parametrize(
    "input_sequence,expected", zip(MIXED_CASE_DNA, CORRECT_ANSWERS_REVERSE)
)
def test_mixed_case_reverse(input_sequence, expected):
    assert reverse_complement.reverse(input_sequence).upper() == expected


@pytest.mark.parametrize(
    "input_sequence,expected", zip(DIRTY_DNA, CORRECT_ANSWERS_REVERSE)
)
def test_dirty_reverse(input_sequence, expected):
    assert reverse_complement.reverse(input_sequence).upper() == expected


# ############################################################################
# Test reverse complement function
# ############################################################################


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(ACGT_BASES_ONLY, CORRECT_ANSWERS_REVERSE_COMPLEMENT),
)
def test_acgt_reverse_complement(input_sequence, expected):
    assert (
            reverse_complement.reverse_complement(input_sequence).upper()
            == expected
    )


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(MIXED_CASE_DNA, CORRECT_ANSWERS_REVERSE_COMPLEMENT),
)
def test_mixed_case_reverse_complement(input_sequence, expected):
    assert (
            reverse_complement.reverse_complement(input_sequence).upper()
            == expected
    )


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(DIRTY_DNA, CORRECT_ANSWERS_REVERSE_COMPLEMENT),
)
def test_dirty_reverse_complement(input_sequence, expected):
    assert (
            reverse_complement.reverse_complement(input_sequence).upper()
            == expected
    )


# ############################################################################
# Use more complex complement table
# ############################################################################


AMBIGOUS_DIRTY_DNA = [
    "AGB Vnc gRy Tvv V",
    ">\nT-TT-AAA-BDNNSSRYMNXXXX  GGGCCC!!!",
    ("TAC WSA YBG KGK DVN YRS TGG TAC TAA TGC CTA AGT GAC CGG CAG CAA AAT GTT"
     " GCA GCA CTG ACC CTT TTG GGA CCG CAA TGG GTT GAA TTA GCG GAA CGT CGT GT"
     "A GGG GGA AAG CGG TCG ACC GCA TTA TCG CTT CTC CGG GCG TGG CTA GCG GGA A"
     "GG GTT GTC AAC GCG TCG GAC TTA CCG CTT ACC GCG AAA CGG ACC AAA GGC CGT "
     "GGT CTT CGC CAC GGC CTT TCG ACC GAC CTC ACG CTA GAA GGA"),
]
CORRECT_ANSWER_AMBIGOUS_DNA_COMPLEMENT = [
    "TCVBNGCYRABBB",
    "AAATTTVHNNSSYRKNCCCGGG",
    ("ATGWSTRVCMCMHBNRYSACCATGATTACGGATTCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAA"
     "CCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATAGCGAAGAGG"
     "CCCGCACCGATCGCCCTTCCCAACAGTTGCGCAGCCTGAATGGCGAATGGCGCTTTGCCTGGTTTCCGGCA"
     "CCAGAAGCGGTGCCGGAAAGCTGGCTGGAGTGCGATCTTCCT"),
]
CORRECT_ANSWER_AMBIGOUS_DNA_REVERSE = [
    "VVVTYRGCNVBGA",
    "CCCGGGNMYRSSNNDBAAATTT",
    ("AGGAAGATCGCACTCCAGCCAGCTTTCCGGCACCGCTTCTGGTGCCGGAAACCAGGCAAAGCGCCATTCGC"
     "CATTCAGGCTGCGCAACTGTTGGGAAGGGCGATCGGTGCGGGCCTCTTCGCTATTACGCCAGCTGGCGAAA"
     "GGGGGATGTGCTGCAAGGCGATTAAGTTGGGTAACGCCAGGGTTTTCCCAGTCACGACGTTGTAAAACGAC"
     "GGCCAGTGAATCCGTAATCATGGTSRYNVDKGKGBYASWCAT"),
]
CORRECT_ANSWER_AMBIGOUS_DNA_REVERSE_COMPLEMENT = [
    "BBBARYCGNBVCT",
    "GGGCCCNKRYSSNNHVTTTAAA",
    ("TCCTTCTAGCGTGAGGTCGGTCGAAAGGCCGTGGCGAAGACCACGGCCTTTGGTCCGTTTCGCGGTAAGCGG"
     "TAAGTCCGACGCGTTGACAACCCTTCCCGCTAGCCACGCCCGGAGAAGCGATAATGCGGTCGACCGCTTTCC"
     "CCCTACACGACGTTCCGCTAATTCAACCCATTGCGGTCCCAAAAGGGTCAGTGCTGCAACATTTTGCTGCCG"
     "GTCACTTAGGCATTAGTACCASYRNBHMCMCVRTSWGTA"),
]


# ############################################################################
# Test reverse, complement and rev comp. function with new table
# ############################################################################


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(AMBIGOUS_DIRTY_DNA, CORRECT_ANSWER_AMBIGOUS_DNA_COMPLEMENT),
)
def test_acgt_complement_new_table(input_sequence, expected):
    assert (
            reverse_complement.complement(input_sequence, COMPLEMENTS_STR).upper()
            == expected
    )


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(AMBIGOUS_DIRTY_DNA, CORRECT_ANSWER_AMBIGOUS_DNA_REVERSE),
)
def test_mixed_case_reverse_new_table(input_sequence, expected):
    assert (
            reverse_complement.reverse(input_sequence, COMPLEMENTS_STR).upper()
            == expected
    )


@pytest.mark.parametrize(
    "input_sequence,expected",
    zip(AMBIGOUS_DIRTY_DNA, CORRECT_ANSWER_AMBIGOUS_DNA_REVERSE_COMPLEMENT),
)
def test_dirty_reverse_complement_new_table(input_sequence, expected):
    assert (
            reverse_complement.reverse_complement(
                input_sequence, COMPLEMENTS_STR
            ).upper()
            == expected
    )
