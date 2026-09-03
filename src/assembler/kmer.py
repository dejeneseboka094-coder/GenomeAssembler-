from collections import Counter
from typing import Iterable


VALID_BASES = set("ACGT")


def generate_kmers(sequence: str, k: int) -> Iterable[str]:
    """
    Generate all k-mers from a DNA sequence.

    Parameters
    ----------
    sequence : str
        DNA sequence.
    k : int
        k-mer size.

    Yields
    ------
    str
        Each valid k-mer.
    """
    sequence = sequence.upper()

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if k > len(sequence):
        return

    for i in range(len(sequence) - k + 1):
        kmer = sequence[i:i + k]

        if set(kmer) <= VALID_BASES:
            yield kmer


def count_kmers(reads, k: int) -> Counter:
    """
    Count k-mers across an iterable of FASTQ reads.

    Parameters
    ----------
    reads : iterable
        Iterable of FastqRead objects.
    k : int
        k-mer size.

    Returns
    -------
    Counter
        Mapping of k-mers to their frequencies.
    """
    counts = Counter()

    if k <= 0:
        raise ValueError("k must be greater than zero")

    for read in reads:
        counts.update(generate_kmers(read.sequence, k))

    return counts
