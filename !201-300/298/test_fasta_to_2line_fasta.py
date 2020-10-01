from fasta_to_2line_fasta import fasta_to_2line_fasta, FASTA_FILE

EXPECTED_RECORDS = 59


def test_well_formed_fasta():
    """
    Test if output is correct with well-formed input.
    """

    CONVERTED_FASTA = f"{FASTA_FILE}-test.fasta"

    assert fasta_to_2line_fasta(FASTA_FILE, CONVERTED_FASTA) == EXPECTED_RECORDS
    with open(FASTA_FILE, "r") as f:
        f.readline()
        assert (
                f.readline().strip()
                == "MNLLSIQPLNRIAIQFGPLTVYWYGIIIGIGILLGLILATREGKKLQVPSNTFTDLVLYA"
        )

    with open(CONVERTED_FASTA, "r") as f_conv:
        f_conv.readline()
        assert (
                f_conv.readline().strip()
                == "MNLLSIQPLNRIAIQFGPLTVYWYGIIIGIGILLGLILATREGKKLQVPSNTFTDLVLYA"
                   "LPISILSARIYYVLFEWAYYKNHLNEIFAIWNGGIAIHGGLIGAIVTTIVFTKKRNISF"
                   "WKLADIAAPSLILGQAIGRWGNFMNQEAHGGPVSRTFLESLRLPDIIINQMYINGSYYH"
                   "PTFLYESIWNIIGFVTLLILRKGSLKRGEIFLSYLIWYSIGRFFVEGLRTDSLMLTSSL"
                   "RMAQVMSISLIIISLLLMIYRRRKGLATTRYNELNNNALE"
        )


def test_malformed_fasta():
    """
    Test if output is correct with mal-formed input.
    """
    MALFORMED_FASTA = f"{FASTA_FILE}.malformed.fasta"
    CONVERTED_FASTA = f"{FASTA_FILE}.malformed-test.fasta"

    with open(FASTA_FILE, "r") as f_in, open(MALFORMED_FASTA, "w") as f_out:
        f_out.write(f_in.read()[1:])

    assert (
            fasta_to_2line_fasta(MALFORMED_FASTA, CONVERTED_FASTA) == EXPECTED_RECORDS - 1
    )

    with open(CONVERTED_FASTA, "r") as f_conv:
        assert (
                f_conv.readline().strip()
                == ">sp|Q74NT6|ARSC1_BACC1 Arsenate reductase 1 OS=Bacillus cereu"
                   "s (strain ATCC 10987 / NRS 248) OX=222523 GN=arsC1 PE=3 SV=1"
        )
        assert (
                f_conv.readline().strip()
                == "MENKKTIYFLCTGNSCRSQMAEAWGKKYLGDKWNVLSAGIEAHGVNPNAIKAMKEVDIDIT"
                   "DQTSDIIDRDILDKADLVVTLCGHANDVCPTTPPHVKRVHWGFDDPAGQEWSVFQRVRDE"
                   "IGARIKKYAETGE"
        )
