from pathlib import Path


def read_fasta(path: str) -> str:
    """Read a single-sequence FASTA file and return its DNA sequence."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"FASTA file not found: {path}")

    sequence_parts = []

    with open(file_path, "r") as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                continue

            sequence_parts.append(line.upper())

    return "".join(sequence_parts)


def read_contigs(path: str) -> list[str]:
    """Read assembled contigs from a FASTA file."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Contig FASTA file not found: {path}")

    contigs = []
    current_sequence = []

    with open(file_path, "r") as handle:
        for line in handle:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                if current_sequence:
                    contigs.append("".join(current_sequence))
                    current_sequence = []
            else:
                current_sequence.append(line.upper())

        if current_sequence:
            contigs.append("".join(current_sequence))

    return contigs


def reverse_complement(sequence: str) -> str:
    """Return the reverse complement of a DNA sequence."""
    table = str.maketrans("ACGT", "TGCA")
    return sequence.upper().translate(table)[::-1]


def generate_kmer_set(sequence: str, k: int) -> set[str]:
    """Generate the set of valid k-mers from a DNA sequence."""
    valid_bases = set("ACGT")
    sequence = sequence.upper()

    if k <= 0:
        raise ValueError("k must be greater than zero")

    return {
        min(sequence[i:i + k], reverse_complement(sequence[i:i + k]))
        for i in range(len(sequence) - k + 1)
        if set(sequence[i:i + k]) <= valid_bases
    }


def calculate_kmer_validation(
    reference: str,
    contigs: list[str],
    k: int,
) -> dict:
    """Compare assembly k-mers against reference k-mers."""

    reference_kmers = generate_kmer_set(reference, k)

    assembly_kmers = set()

    for contig in contigs:
        assembly_kmers.update(generate_kmer_set(contig, k))

    shared_kmers = reference_kmers & assembly_kmers

    reference_recall = (
        len(shared_kmers) / len(reference_kmers) * 100
        if reference_kmers
        else 0.0
    )

    assembly_precision = (
        len(shared_kmers) / len(assembly_kmers) * 100
        if assembly_kmers
        else 0.0
    )

    return {
        "k": k,
        "reference_kmers": len(reference_kmers),
        "assembly_kmers": len(assembly_kmers),
        "shared_kmers": len(shared_kmers),
        "reference_kmer_recall_percent": reference_recall,
        "assembly_kmer_precision_percent": assembly_precision,
    }
