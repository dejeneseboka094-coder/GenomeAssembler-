from src.assembler.fastq import read_fastq
from src.assembler.kmer import count_kmers
from src.assembler.graph import build_debruijn_graph


def test_build_debruijn_graph():
    reads = read_fastq("data/simulated/reads.fastq")

    kmer_counts = count_kmers(reads, 5)

    graph = build_debruijn_graph(kmer_counts, 5)

    assert graph.node_count() == 19
    assert graph.edge_count() == 23
    assert graph.neighbors("GATC")["ATCG"] == 6

def test_predecessors():
    from src.assembler.graph import DeBruijnGraph

    graph = DeBruijnGraph()

    graph.add_edge("ATG", "TGC", 5)
    graph.add_edge("TGC", "GCG", 3)

    assert graph.predecessors("TGC") == ["ATG"]
    assert graph.predecessors("GCG") == ["TGC"]
    assert graph.predecessors("ATG") == []
