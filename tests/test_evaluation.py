from src.assembler.evaluation import (
    calculate_n50,
    calculate_assembly_metrics,
)


def test_calculate_n50():
    contigs = [
        "A" * 5,
        "A" * 15,
        "A" * 7,
    ]

    assert calculate_n50(contigs) == 15


def test_calculate_assembly_metrics():
    contigs = [
        "CGATC",
        "CGATGCTAGCTGATC",
        "GATCGAT",
    ]

    metrics = calculate_assembly_metrics(contigs)

    assert metrics["number_of_contigs"] == 3
    assert metrics["total_length"] == 27
    assert metrics["largest_contig"] == 15
    assert metrics["average_contig_length"] == 9.0
    assert metrics["N50"] == 15


def test_empty_contigs():
    metrics = calculate_assembly_metrics([])

    assert metrics["number_of_contigs"] == 0
    assert metrics["total_length"] == 0
    assert metrics["largest_contig"] == 0
    assert metrics["average_contig_length"] == 0
    assert metrics["N50"] == 0


def test_calculate_read_incorporation():
    from src.assembler.fastq import FastqRead
    from src.assembler.evaluation import calculate_read_incorporation

    reads = [
        FastqRead("read1", "ATGCG", "IIIII"),
        FastqRead("read2", "GCTAG", "IIIII"),
        FastqRead("read3", "TTTTT", "IIIII"),
    ]

    contigs = [
        "CCCATGCGGG",
        "AAAGCTAGCCC",
    ]

    percentage = calculate_read_incorporation(reads, contigs)

    assert percentage == (2 / 3) * 100
