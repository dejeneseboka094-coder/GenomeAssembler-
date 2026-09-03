def _path_to_sequence(path):
    """Convert a graph path of nodes into a DNA sequence."""
    sequence = path[0]

    for node in path[1:]:
        sequence += node[-1]

    return sequence


def find_contigs(graph):
    """
    Traverse a de Bruijn graph and generate contig sequences.

    The algorithm identifies maximal non-branching paths.
    Branching nodes are used as boundaries between contigs.
    Remaining unvisited edges are used to recover isolated cycles.
    """

    visited_edges = set()
    contigs = []

    # ---------------------------------------------------------
    # Part 1: Traverse paths starting at non-1-in/1-out nodes
    # ---------------------------------------------------------
    for node in graph.nodes():

        outgoing = graph.neighbors(node)
        incoming = graph.predecessors(node)

        # Nodes with no outgoing edges cannot start a path.
        if len(outgoing) == 0:
            continue

        # A simple 1-in/1-out node belongs to the middle
        # of a non-branching path.
        if len(incoming) == 1 and len(outgoing) == 1:
            continue

        # Start a separate path from every outgoing edge.
        for next_node in outgoing:

            edge = (node, next_node)

            if edge in visited_edges:
                continue

            # IMPORTANT:
            # Mark the first edge immediately.
            visited_edges.add(edge)

            path = [node, next_node]
            current = next_node

            # Continue through simple 1-in/1-out nodes.
            while (
                len(graph.predecessors(current)) == 1
                and len(graph.neighbors(current)) == 1
            ):

                next_node = next(iter(graph.neighbors(current)))
                edge = (current, next_node)

                if edge in visited_edges:
                    break

                visited_edges.add(edge)
                path.append(next_node)
                current = next_node

            contigs.append(_path_to_sequence(path))

    # ---------------------------------------------------------
    # Part 2: Handle isolated cycles
    # ---------------------------------------------------------
    for node in graph.nodes():

        for next_node in graph.neighbors(node):

            edge = (node, next_node)

            if edge in visited_edges:
                continue

            visited_edges.add(edge)

            path = [node, next_node]
            current = next_node

            while True:

                outgoing = graph.neighbors(current)

                if len(outgoing) == 0:
                    break

                next_node = next(iter(outgoing))
                edge = (current, next_node)

                if edge in visited_edges:
                    break

                visited_edges.add(edge)
                path.append(next_node)
                current = next_node

            contigs.append(_path_to_sequence(path))

    return contigs
