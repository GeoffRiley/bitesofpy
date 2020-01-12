import os
from collections import defaultdict
from typing import List
from urllib.request import urlretrieve

# Translation Table:
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG11
# Each column represents one entry. Codon = {Base1}{Base2}{Base3}
# All Base 'U's need to be converted to 'T's to convert DNA to RNA
TRANSL_TABLE_11 = """
    AAs  = FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG
  Starts = ---M------**--*----M------------MMMM---------------M------------
  Base1  = TTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCAAAAAAAAAAAAAAAAGGGGGGGGGGGGGGGG
  Base2  = TTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGGTTTTCCCCAAAAGGGG
  Base3  = TCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAGTCAG
"""

# Converted from http://ftp.ncbi.nlm.nih.gov/genomes/archive/old_refseq/Bacteria/Staphylococcus_aureus_Newman_uid58839/NC_009641.ffn  # noqa E501
URL = "https://bites-data.s3.us-east-2.amazonaws.com/NC_009641.txt"

# Order of bases in the table
BASE_ORDER = ["U", "C", "A", "G"]


def _preload_sequences(url=URL) -> List[str]:
    """
    Provided helper function
    Returns coding sequences, one sequence each line
    """
    filename = os.path.join(os.getenv("TMP", "/tmp"), "NC_009641.txt")
    if not os.path.isfile(filename):
        urlretrieve(url, filename)
    with open(filename, "r") as f:
        return f.readlines()


def return_codon_usage_table(
        sequences=None, translation_table_str: str = TRANSL_TABLE_11
):
    """
    Receives a list of gene sequences and a translation table string
    Returns a string with all bases and their frequencies in a table
    with the following fields:
    codon_triplet: amino_acid_letter frequency_per_1000 absolute_occurrences

    Skip invalid coding sequences:
       --> must consist entirely of codons (3-base triplet)
    """
    if sequences is None:
        sequences = _preload_sequences()
    translation_table = dict(map(str.strip, l.split('='))
                             for l in translation_table_str.splitlines(keepends=False)
                             if l and len(l.strip()) > 0)
    codons = [''.join(v).replace('T', 'U') for v in
              zip(translation_table['Base1'], translation_table['Base2'], translation_table['Base3'])]
    codon_freq = defaultdict(int)
    tot = 0
    for rna in sequences:
        tot += len(rna) // 3
        while rna != '':
            codon_freq[rna[:3]] += 1
            rna = rna[3:]

    out = []
    out.append(f"|{'  Codon AA  Freq  Count  |' * 4}")
    out.append('-' * 105)
    for base1 in BASE_ORDER:
        for base3 in BASE_ORDER:
            line = ''
            for base2 in BASE_ORDER:
                base = f'{base1}{base2}{base3}'
                line += f"|  {base}:  {translation_table['AAs'][codons.index(base)]:2} {codon_freq[base] / tot * 1000:5.1f} {codon_freq[base]:6}  "
            out.append(line + '|')
        out.append('-' * 105)

    return '\n'.join(out)


if __name__ == "__main__":
    print(return_codon_usage_table())
