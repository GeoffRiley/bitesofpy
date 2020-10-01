import re

from Bio import Seq


def translate_cds(cds: str, translation_table: str) -> str:
    """
    :param cds: str: DNA coding sequence (CDS)
    :param translation_table: str: translation table as defined in Bio.Seq.Seq.CodonTable.ambiguous_generic_by_name
    :return: str: Protein sequence
    """
    # Clean up any whitespace
    sanitized = re.sub(r'\s*', '', cds)
    # Turn it into a Sequence object
    seq = Seq.Seq(sanitized)
    # …and translate!
    translated = Seq.translate(seq, translation_table, cds=True)

    return str(translated)
