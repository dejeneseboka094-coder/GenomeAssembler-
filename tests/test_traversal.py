from src.assembler.graph import DeBruijnGraph
from src.assembler.traversal import find_contigs


def test_find_contigs_simple_path():
    graph = DeBruijnGraph()

    graph.add_edge("ATG", "TGC", 5)
    graph.add_edge("TGC", "GCG", 5)
    graph.add_edge("GCG", "CGA", 5)

    contigs = find_contigs(graph)

    assert contigs == ["ATGCGA"]


def test_find_contigs_two_paths():
    graph = DeBruijnGraph()

    graph.add_edge("ATG", "TGC", 5)
    graph.add_edge("TGC", "GCG", 5)

    graph.add_edge("CCC", "CCA", 3)
    graph.add_edge("CCA", "CAT", 3)

    contigs = find_contigs(graph)

    assert "ATGCG" in contigs
    assert "CCCAT" in contigs
    assert len(contigs) == 2

def test_find_contigs_branching_graph():
    graph = DeBruijnGraph()

    # Main path leading to a branching node
    graph.add_edge("ATG", "TGC", 10)

    # Two branches from TGC
    graph.add_edge("TGC", "GCG", 10)
    graph.add_edge("TGC", "GCT", 2)

    contigs = find_contigs(graph)

    assert "ATGC" in contigs
    assert "TGCG" in contigs
    assert "TGCT" in contigs
    assert len(contigs) == 3

def test_find_contigs_cycle():
    graph = DeBruijnGraph()

    graph.add_edge("ATG", "TGC", 5)
    graph.add_edge("TGC", "GCA", 5)
    graph.add_edge("GCA", "CAT", 5)
    graph.add_edge("CAT", "ATG", 5)

    contigs = find_contigs(graph)

    assert len(contigs) >= 1
