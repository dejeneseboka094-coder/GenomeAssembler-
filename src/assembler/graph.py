from collections import defaultdict


class DeBruijnGraph:
    """Directed de Bruijn graph for genome assembly."""

    def __init__(self):
        self.adjacency = defaultdict(dict)
        self.reverse_adjacency = defaultdict(set)

    def add_edge(self, source: str, target: str, coverage: int = 1):
        """Add a directed edge with its k-mer coverage."""

        self.adjacency[source][target] = coverage
        self.reverse_adjacency[target].add(source)

    def remove_edge(self, source: str, target: str):
        """Remove a directed edge and update both graph indexes."""

        if target in self.adjacency.get(source, {}):
            del self.adjacency[source][target]

        if source in self.reverse_adjacency.get(target, set()):
            self.reverse_adjacency[target].remove(source)

        if not self.adjacency.get(source):
            self.adjacency.pop(source, None)

        if not self.reverse_adjacency.get(target):
            self.reverse_adjacency.pop(target, None)

    def nodes(self):
        """Return all graph nodes."""

        nodes = set(self.adjacency.keys())

        for neighbors in self.adjacency.values():
            nodes.update(neighbors.keys())

        return nodes

    def neighbors(self, node: str):
        """Return outgoing neighbors of a node."""

        return self.adjacency.get(node, {})

    def predecessors(self, node: str):
        """Return nodes with edges pointing to the given node."""

        return list(self.reverse_adjacency.get(node, set()))

    def edge_count(self):
        """Return the number of directed edges."""

        return sum(
            len(neighbors)
            for neighbors in self.adjacency.values()
        )

    def node_count(self):
        """Return the number of graph nodes."""

        return len(self.nodes())


def build_debruijn_graph(kmer_counts, k: int) -> DeBruijnGraph:
    """Build a de Bruijn graph from counted k-mers."""

    graph = DeBruijnGraph()

    for kmer, coverage in kmer_counts.items():
        prefix = kmer[:-1]
        suffix = kmer[1:]

        graph.add_edge(
            prefix,
            suffix,
            coverage,
        )

    return graph
