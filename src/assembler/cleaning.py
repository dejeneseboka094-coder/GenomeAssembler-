def filter_low_coverage_edges(graph, min_coverage: int):
    """Remove graph edges with coverage below the minimum threshold."""

    if min_coverage < 1:
        raise ValueError("min_coverage must be at least 1")

    edges_to_remove = []

    for source, neighbors in graph.adjacency.items():
        for target, coverage in neighbors.items():
            if coverage < min_coverage:
                edges_to_remove.append((source, target))

    for source, target in edges_to_remove:
        del graph.adjacency[source][target]

    return graph

def remove_tips(graph, max_length: int):
    """
    Remove short dead-end branches from a de Bruijn graph.

    A tip is identified as a short path that:
    1. starts from a branching node,
    2. follows a single outgoing path,
    3. ends at a dead-end node,
    4. has length <= max_length.

    Parameters
    ----------
    graph : DeBruijnGraph
        Graph to clean.
    max_length : int
        Maximum number of edges in a removable tip.

    Returns
    -------
    DeBruijnGraph
        The cleaned graph.
    """

    if max_length < 1:
        raise ValueError("max_length must be at least 1")

    edges_to_remove = []

    for source, neighbors in list(graph.adjacency.items()):

        # A branching node must have more than one outgoing edge.
        if len(neighbors) <= 1:
            continue

        for first_target in list(neighbors):

            path = [(source, first_target)]
            current = first_target

            while len(path) < max_length:

                outgoing = graph.neighbors(current)

                if len(outgoing) != 1:
                    break

                next_node = next(iter(outgoing))

                # Do not follow a path that returns to an existing node.
                if next_node in {node for edge in path for node in edge}:
                    break

                path.append((current, next_node))
                current = next_node

            # Only remove the branch if it reaches a dead end
            # within the allowed tip length.
            if (
                len(path) <= max_length
                and len(graph.neighbors(current)) == 0
            ):
                # Check whether this is actually the short branch.
                # Prefer removing the lower-coverage branch.
                path_coverage = [
                    graph.adjacency[u][v]
                    for u, v in path
                ]

                competing_edges = [
                    (target, graph.adjacency[source][target])
                    for target in graph.neighbors(source)
                    if target != first_target
                ]

                if competing_edges:
                    competing_coverage = max(
                        coverage
                        for _, coverage in competing_edges
                    )

                    if max(path_coverage) < competing_coverage:
                        edges_to_remove.extend(path)

    for source, target in edges_to_remove:
        if target in graph.adjacency.get(source, {}):
            del graph.adjacency[source][target]

    return graph

