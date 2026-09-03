def calculate_n50(contigs):
    """
    Calculate the N50 statistic for a collection of contigs.

    N50 is the contig length such that contigs of this
    length or longer contain at least 50% of the total
    assembly length.
    """

    if not contigs:
        return 0

    lengths = sorted(
        (len(contig) for contig in contigs),
        reverse=True,
    )

    total_length = sum(lengths)
    half_length = total_length / 2

    cumulative_length = 0

    for length in lengths:
        cumulative_length += length

        if cumulative_length >= half_length:
            return length

    return 0


def calculate_assembly_metrics(contigs):
    """
    Calculate basic assembly statistics.

    Returns
    -------
    dict
        Assembly statistics including:
        - number of contigs
        - total length
        - largest contig
        - average contig length
        - N50
    """

    if not contigs:
        return {
            "number_of_contigs": 0,
            "total_length": 0,
            "largest_contig": 0,
            "average_contig_length": 0,
            "N50": 0,
        }

    lengths = [len(contig) for contig in contigs]

    return {
        "number_of_contigs": len(contigs),
        "total_length": sum(lengths),
        "largest_contig": max(lengths),
        "average_contig_length": sum(lengths) / len(lengths),
        "N50": calculate_n50(contigs),
    }
