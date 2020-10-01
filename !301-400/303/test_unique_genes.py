"""
Test unique_genes.convert_to_unique_genes()
 -Test regular 2-line FASTA file (one header row, one sequence row)
 -Test multi-line FASTA file (one header row, multiple sequence rows)
 -Test that first sequence is ignored in absence of a header
 -Test case variation in gene name
 -Test case variation in sequence
 -Test additional gene name
 -Test use of gzip format as in- or output
"""
import gzip
import os
from urllib.request import urlretrieve

import pytest
import unique_genes

# ################ SETUP

NARI_URL = "https://bites-data.s3.us-east-2.amazonaws.com/narI.fna"


# ################ Support functions
def make_fasta_from_tuple(content):
    """
    Creates a FASTA text from tuples
    """
    return_text = ""
    for header, seq in content:
        return_text += f"{header}\n{seq}\n"
    return return_text


def write_test_file(filename, content, zip=False):
    """
    Writes the contents of a FASTA fie into a physical file
    """
    if not os.path.isfile(filename):
        if not zip:
            with open(filename, "w") as f:
                f.write(make_fasta_from_tuple(content))
        else:
            with gzip.open(filename, "wt") as f:
                f.write(make_fasta_from_tuple(content))


def len_and_first_line(test_filename, tmp):
    input_filename = test_filename
    output_filename = tmp / "output.fasta"

    unique_genes.convert_to_unique_genes(str(input_filename), str(output_filename))
    with open(output_filename, "r") as f:
        all_lines = f.readlines()
        return (
            sum([1 for line in all_lines if line[0] == ">"]),
            all_lines[0].strip().upper(),
        )


# Pytest fixtures ###############################
@pytest.fixture(scope="session")
def fasta_dir(tmpdir_factory):
    simple_fasta = [
        (">gene [locustag=AA11]", "AAAAAA"),
        (">gene [locustag=BB22]", "AAAAAA"),
        (">gene [locustag=CC33]", "AAAAAA"),
        (">gene [locustag=DD44]", "GAAAAC"),
    ]

    tmp_d = tmpdir_factory.mktemp("fastas")

    # Regular 2-line FASTA file (1 line header, one line sequence)
    write_test_file(tmp_d.join("simple_test.fasta"), simple_fasta)
    write_test_file(tmp_d.join("simple_test.fasta.gz"), simple_fasta, zip=True)

    # FASTA File where the sequence is spread over more than one line
    simple_multi_fasta = simple_fasta.copy()
    simple_multi_fasta[0] = (">gene [locustag=AA11]", "AAA\nAAA")
    write_test_file(tmp_d.join("simple_multi_fasta.fasta"), simple_multi_fasta)

    # FASTA File with first header missing
    missing_header = simple_fasta.copy()
    missing_header[0] = ("gene [locustag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("first_header_missing.fasta"), missing_header)

    # FASTA with same gene but upper/lower case variation
    name_case_variation = simple_fasta.copy()
    name_case_variation[0] = (">gEnE [locustag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("gene_case_variation.fasta"), name_case_variation)

    # FASTA with upper and lower case variation in sequence
    seq_case_variation = simple_fasta.copy()
    seq_case_variation[0] = (">gene [locustag=AA11]", "AaAaAa")
    write_test_file(tmp_d.join("seq_case_variation.fasta"), seq_case_variation)

    # FASTA file with more than one gene
    two_different_genes = simple_fasta.copy()
    two_different_genes[0] = (">gene2 [locustag=AA11]", "AAAAAA")
    write_test_file(tmp_d.join("two_gene_names.fasta"), two_different_genes)

    if not os.path.isfile(tmp_d.join("narI.fasta")):
        urlretrieve(url=NARI_URL, filename=tmp_d.join("narI.fasta"))

    return tmp_d


# End of setup ####################################

# Tests ###########################################


def test_regular_2line_fasta(fasta_dir, tmp_path):
    """
    Use a short FASTA file to test output
    """
    assert len_and_first_line(fasta_dir / "simple_test.fasta", tmp_path) == (
        2,
        ">gene [locustags=AA11,BB22,CC33]".upper(),
    )


def test_multiline_fasta(fasta_dir, tmp_path):
    """
    Test multi line FASTA file
    """
    assert len_and_first_line(fasta_dir / "simple_multi_fasta.fasta", tmp_path) == (
        2,
        ">gene [locustags=AA11,BB22,CC33]".upper(),
    )


def test_name_case_variation(fasta_dir, tmp_path):
    """
    Test if case variation in name is ignored
    """
    assert len_and_first_line(fasta_dir / "gene_case_variation.fasta", tmp_path) == (
        2,
        ">gene [locustags=AA11,BB22,CC33]".upper(),
    )


def test_seq_case_variation(fasta_dir, tmp_path):
    """ "
    Test if case variation in sequence is ignored
    """
    assert len_and_first_line(fasta_dir / "seq_case_variation.fasta", tmp_path) == (
        2,
        ">gene [locustags=AA11,BB22,CC33]".upper(),
    )


def test_header_missing(fasta_dir, tmp_path):
    """
    Test FASTA with missing header
    """
    assert len_and_first_line(fasta_dir / "first_header_missing.fasta", tmp_path) == (
        2,
        ">gene [locustags=BB22,CC33]".upper(),
    )


def test_longer_input(fasta_dir, tmp_path):
    """
    Test longer FASTA input
    """
    assert len_and_first_line(fasta_dir / "narI.fasta", tmp_path) == (
        58,
        ">narI [locustags=AKT31_RS21590,AQ748_RS19920,AQ784_RS19345,AQ785_RS13635,AQ812_RS36520,AQ814_RS06970,AQ813_RS16170,AQ815_RS05930,AQ817_RS32295,AQ816_RS19885,AQ818_RS10925,AQ820_RS04380,AQ821_RS24315,AQ822_RS15280,AQ823_RS29490,AQ825_RS18275,AQ824_RS32145,AQ826_RS01305,AQ827_RS28590,AQ828_RS04410,AQ829_RS31805,AQ830_RS02445,AQ831_RS15090,AQ832_RS15115,AQ833_RS17275,AQ835_RS13565,AQ834_RS22940,AQ836_RS11625,AQ842_RS13375,AQ843_RS34445,AQ844_RS13660,AQ845_RS30860,AQ847_RS22875,AQ848_RS00095,AQ849_RS01070,AQ850_RS14315,AQ851_RS25640,AQ852_RS31515,AQ934_RS19920]".upper(),
    )


def test_ambigious_gene_name(fasta_dir, tmp_path):
    """
    Test with more than one gene name present in FASTA file
    """
    with pytest.raises(NameError) as excinfo:
        unique_genes.convert_to_unique_genes(
            str(fasta_dir / "two_gene_names.fasta"), str(tmp_path / "output.fasta")
        )
    assert "Gene names differ between entries: 'gene2' vs. 'gene'" in str(excinfo.value)


def test_gzipped_fastas(fasta_dir, tmp_path):
    """
    Test how function handles gzipped FASTA files
    """

    # gz INPUT > fna OUTPUT
    assert len_and_first_line(fasta_dir / "simple_test.fasta.gz", tmp_path) == (
        2,
        ">gene [locustags=AA11,BB22,CC33]".upper(),
    )

    # fna INPUT > gz OUTPUT
    unique_genes.convert_to_unique_genes(
        str(fasta_dir / "simple_test.fasta"), str(tmp_path / "output.fasta.gz")
    )
    with gzip.open(str(tmp_path / "output.fasta.gz"), "rt") as f:
        assert (
                f.readlines()[0].strip().upper()
                == ">gene [locustags=AA11,BB22,CC33]".upper()
        )

    # gz INPUT > gz OUTPUT
    unique_genes.convert_to_unique_genes(
        str(fasta_dir / "simple_test.fasta.gz"), str(tmp_path / "output2.fasta.gz")
    )
    with gzip.open(str(tmp_path / "output2.fasta.gz"), "rt") as f:
        assert (
                f.readlines()[0].strip().upper()
                == ">gene [locustags=AA11,BB22,CC33]".upper()
        )
