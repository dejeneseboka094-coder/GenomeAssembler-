from src.assembler.fastq import read_fastq, read_paired_fastq
from src.assembler.kmer import count_kmers
from src.assembler.graph import build_debruijn_graph
from src.assembler.cleaning import (
    filter_low_coverage_edges,
    remove_tips,
)
from src.assembler.traversal import find_contigs
from src.assembler.assembly import write_fasta
from src.assembler.evaluation import (
    calculate_assembly_metrics,
    calculate_read_incorporation,
)


def assemble(
    input_path,
    output_path,
    k,
    min_coverage=2,
    tip_length=2,
    input_path_r2=None,
):
    """
    Run the complete genome assembly pipeline.

    Parameters
    ----------
    input_path : str
        R1 FASTQ file.
    output_path : str
        Output FASTA file.
    k : int
        k-mer size.
    min_coverage : int
        Minimum k-mer coverage to retain.
    tip_length : int
        Maximum removable tip length.
    input_path_r2 : str or None
        Optional R2 FASTQ file for paired-end data.
    """

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if min_coverage < 1:
        raise ValueError("min_coverage must be at least 1")

    if tip_length < 1:
        raise ValueError("tip_length must be at least 1")

    if input_path_r2 is None:
        reads = read_fastq(input_path)
    else:
        paired_reads = read_paired_fastq(
            input_path,
            input_path_r2,
        )

        reads = (
            read
            for pair in paired_reads
            for read in pair
        )

        reads = list(reads)
    kmer_counts = count_kmers(reads, k)

    graph = build_debruijn_graph(
        kmer_counts,
        k,
    )

    filter_low_coverage_edges(
        graph,
        min_coverage=min_coverage,
    )

    remove_tips(
        graph,
        max_length=tip_length,
    )

    contigs = find_contigs(graph)

    write_fasta(
        contigs,
        output_path,
    )

    metrics = calculate_assembly_metrics(contigs)
    metrics["read_incorporation_percentage"] = calculate_read_incorporation(
        reads, contigs
    )

    return contigs, metrics
