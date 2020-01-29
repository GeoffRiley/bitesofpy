from collections import Counter


def calculate_gc_content(sequence):
    """
    Receives a DNA sequence (A, G, C, or T)
    Returns the percentage of GC content (rounded to the last two digits)
    """
    counts = Counter(sequence.upper())
    gc = (counts['G'] + counts['C'])
    acgt = sum(v for k, v in counts.items() if k in 'ACGT')
    return round(gc / acgt * 100, 2)
