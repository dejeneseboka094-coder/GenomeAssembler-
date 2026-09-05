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


def calculate_read_incorporation(reads, contigs):
    """
    Calculate the percentage of reads fully incorporated into contigs.

    A read is considered incorporated if its complete sequence occurs
    in at least one assembled contig.

    Parameters
    ----------
    reads : iterable
        FASTQ read objects with a ``sequence`` attribute.
    contigs : iterable of str
        Assembled contig sequences.

    Returns
    -------
    float
        Percentage of reads whose complete sequence is found in a contig.
    """

    reads = list(reads)
    contigs = list(contigs)

    if not reads:
        return 0.0

    incorporated = 0

    for read in reads:
        sequence = read.sequence.upper()

        if any(sequence in contig for contig in contigs):
            incorporated += 1

    return (incorporated / len(reads)) * 100
