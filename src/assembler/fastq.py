from dataclasses import dataclass
from pathlib import Path
import gzip
from typing import Iterator


@dataclass
class FastqRead:
    """Represent a single FASTQ read."""
    identifier: str
    sequence: str
    quality: str


def open_fastq(path: str):
    """Open plain-text or gzip-compressed FASTQ files."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"FASTQ file not found: {path}")

    if file_path.suffix == ".gz":
        return gzip.open(file_path, "rt")
    
    return open(file_path, "r")


def read_fastq(path: str) -> Iterator[FastqRead]:
    """
    Stream reads from a FASTQ file.

    Each FASTQ record contains four lines:
    1. Identifier
    2. DNA sequence
    3. '+' separator
    4. Quality string
    """
    with open_fastq(path) as handle:
        while True:
            identifier = handle.readline()

            if not identifier:
                break

            sequence = handle.readline()
            separator = handle.readline()
            quality = handle.readline()

            if not sequence or not separator or not quality:
                raise ValueError("Incomplete FASTQ record")

            identifier = identifier.strip()
            sequence = sequence.strip().upper()
            separator = separator.strip()
            quality = quality.strip()

            if not identifier.startswith("@"):
                raise ValueError(
                    f"Invalid FASTQ identifier: {identifier}"
                )

            if separator != "+":
                raise ValueError(
                    f"Invalid FASTQ separator: {separator}"
                )

            if len(sequence) != len(quality):
                raise ValueError(
                    f"Sequence and quality lengths differ for {identifier}"
                )

            yield FastqRead(
                identifier=identifier[1:],
                sequence=sequence,
                quality=quality,
            )

def read_paired_fastq(r1_path: str, r2_path: str):
    """
    Stream paired-end reads from two FASTQ files.

    Reads from R1 and R2 are returned as pairs.
    """

    r1_reads = read_fastq(r1_path)
    r2_reads = read_fastq(r2_path)

    for read1, read2 in zip(r1_reads, r2_reads):
        yield read1, read2
