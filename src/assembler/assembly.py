from pathlib import Path


def write_fasta(contigs, output_path):
    """
    Write assembled contigs to a FASTA file.

    Parameters
    ----------
    contigs : iterable of str
        DNA sequences representing assembled contigs.

    output_path : str or Path
        Path to the output FASTA file.
    """

    output_path = Path(output_path)

    if not contigs:
        raise ValueError("No contigs provided")

    with open(output_path, "w") as handle:
        for index, contig in enumerate(contigs, start=1):
            handle.write(f">contig_{index}\n")
            handle.write(f"{contig}\n")
