import argparse

from src.assembler.pipeline import assemble


def main():
    """Run the genome assembler from the command line."""

    parser = argparse.ArgumentParser(
        description="Genome assembly using a de Bruijn graph."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Input FASTQ file.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output FASTA file.",
    )

    parser.add_argument(
        "--k",
        type=int,
        required=True,
        help="k-mer size.",
    )

    parser.add_argument(
        "--min-coverage",
        type=int,
        default=2,
        help="Minimum k-mer coverage to retain.",
    )

    parser.add_argument(
        "--tip-length",
        type=int,
        default=2,
        help="Maximum length of removable tips.",
    )

    args = parser.parse_args()

    contigs, metrics = assemble(
        input_path=args.input,
        output_path=args.output,
        k=args.k,
        min_coverage=args.min_coverage,
        tip_length=args.tip_length,
    )

    print("Assembly completed successfully.")
    print()
    print("Assembly metrics:")

    for key, value in metrics.items():
        print(f"{key}: {value}")

    print()
    print(f"FASTA output: {args.output}")
    print(f"Number of contigs generated: {len(contigs)}")


if __name__ == "__main__":
    main()
