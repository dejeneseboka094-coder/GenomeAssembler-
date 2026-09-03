from src.assembler.fastq import read_fastq
from src.assembler.kmer import count_kmers
from src.assembler.graph import build_debruijn_graph
from src.assembler.cleaning import (
    filter_low_coverage_edges,
    remove_tips,
)
from src.assembler.traversal import find_contigs
from src.assembler.assembly import write_fasta
from src.assembler.evaluation import calculate_assembly_metrics


def assemble(
    input_path,
    output_path,
    k,
    min_coverage=2,
    tip_length=2,
):
    """
    Run the complete genome assembly pipeline.

    Parameters
    ----------
    input_path : str
        Input FASTQ file.

    output_path : str
        Output FASTA file.

    k : int
        k-mer size.

    min_coverage : int, default=2
        Minimum k-mer coverage retained in the graph.

    tip_length : int, default=2
        Maximum length of removable tips.

    Returns
    -------
    tuple
        A tuple containing:
        - contigs: assembled DNA sequences
        - metrics: assembly statistics
    """

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if min_coverage < 1:
        raise ValueError("min_coverage must be at least 1")

    if tip_length < 1:
        raise ValueError("tip_length must be at least 1")

    # Step 1: Read FASTQ
    reads = read_fastq(input_path)

    # Step 2: Count k-mers
    kmer_counts = count_kmers(reads, k)

    # Step 3: Build de Bruijn graph
    graph = build_debruijn_graph(kmer_counts, k)

    # Step 4: Remove low-coverage edges
    filter_low_coverage_edges(
        graph,
        min_coverage=min_coverage,
    )

    # Step 5: Remove short erroneous tips
    remove_tips(
        graph,
        max_length=tip_length,
    )

    # Step 6: Traverse graph
    contigs = find_contigs(graph)

    # Step 7: Write FASTA
    write_fasta(contigs, output_path)

    # Step 8: Calculate assembly metrics
    metrics = calculate_assembly_metrics(contigs)

    return contigs, metrics
