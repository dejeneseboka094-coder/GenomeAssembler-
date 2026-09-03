import subprocess
import sys


def test_cli_assembly(tmp_path):
    """Test genome assembly through the command-line interface."""

    output_file = tmp_path / "assembled.fasta"

    command = [
        sys.executable,
        "-m",
        "src.assembler.cli",
        "--input",
        "data/simulated/reads.fastq",
        "--output",
        str(output_file),
        "--k",
        "5",
        "--min-coverage",
        "2",
        "--tip-length",
        "2",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0

    assert "Assembly completed successfully." in result.stdout
    assert "number_of_contigs: 3" in result.stdout
    assert "total_length: 27" in result.stdout
    assert "N50: 15" in result.stdout

    assert output_file.exists()

    content = output_file.read_text()

    assert ">contig_" in content
    assert "CGATGCTAGCTGATC" in content
