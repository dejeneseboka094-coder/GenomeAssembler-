from src.assembler.fastq import read_fastq


def test_read_fastq():
    reads = list(read_fastq("data/simulated/reads.fastq"))

    assert len(reads) == 5

    assert reads[0].identifier == "read1"
    assert reads[0].sequence == "ATGCGATCGATGCTA"
    assert reads[0].quality == "IIIIIIIIIIIIIII"

    assert all(len(read.sequence) == len(read.quality) for read in reads)
    assert all(set(read.sequence) <= set("ACGT") for read in reads)
