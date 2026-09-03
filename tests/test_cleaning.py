from src.assembler.fastq import read_fastq
from src.assembler.kmer import count_kmers
from src.assembler.graph import build_debruijn_graph
from src.assembler.cleaning import filter_low_coverage_edges


def test_filter_low_coverage_edges():
    reads = read_fastq("data/simulated/reads.fastq")

    kmer_counts = count_kmers(reads, 5)

    graph = build_debruijn_graph(kmer_counts, 5)

    assert graph.edge_count() == 23

    filter_low_coverage_edges(graph, min_coverage=2)

    assert graph.edge_count() == 16
    assert "TGCG" not in graph.neighbors("ATGC")
    assert graph.neighbors("GATC")["ATCG"] == 6

def test_remove_tips():
    from src.assembler.graph import DeBruijnGraph
    from src.assembler.cleaning import remove_tips

    graph = DeBruijnGraph()

    # Main path
    graph.add_edge("AAA", "AAT", 10)
    graph.add_edge("AAT", "ATG", 10)
    graph.add_edge("ATG", "TGG", 10)

    # Short erroneous tip
    graph.add_edge("AAT", "ATC", 1)
    graph.add_edge("ATC", "TCG", 1)

    assert graph.edge_count() == 5

    remove_tips(graph, max_length=2)

    assert graph.edge_count() == 3
    assert "ATC" not in graph.neighbors("AAT")
