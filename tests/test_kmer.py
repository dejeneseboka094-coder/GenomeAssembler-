import pytest

from src.assembler.fastq import read_fastq
from src.assembler.kmer import generate_kmers, count_kmers


def test_generate_kmers():
    sequence = "ATGCGAT"

    kmers = list(generate_kmers(sequence, 4))

    assert kmers == [
        "ATGC",
        "TGCG",
        "GCGA",
        "CGAT",
    ]


def test_generate_kmers_invalid_k():
    with pytest.raises(ValueError):
        list(generate_kmers("ATGCG", 0))


def test_generate_kmers_larger_than_sequence():
    kmers = list(generate_kmers("ATG", 5))

    assert kmers == []


def test_generate_kmers_ignores_invalid_bases():
    sequence = "ATGNNGAT"

    kmers = list(generate_kmers(sequence, 4))

    assert kmers == []


def test_count_kmers():
    reads = read_fastq("data/simulated/reads.fastq")

    counts = count_kmers(reads, 5)

    assert sum(counts.values()) == 55
    assert len(counts) == 23

    assert counts["GATCG"] == 6
    assert counts["TAGCT"] == 5
    assert counts["CGATC"] == 4
