from src.assembler.pipeline import assemble


def test_assemble_simulated_data(tmp_path):
    output_file = tmp_path / "assembled.fasta"

    contigs, metrics = assemble(
        "data/simulated/reads.fastq",
        output_file,
        k=5,
        min_coverage=2,
        tip_length=2,
    )

    # Check assembled contigs
    assert len(contigs) == 3

    # Check assembly metrics
    assert metrics["number_of_contigs"] == 3
    assert metrics["total_length"] == 27
    assert metrics["largest_contig"] == 15
    assert metrics["average_contig_length"] == 9.0
    assert metrics["N50"] == 15

    # Check FASTA output
    assert output_file.exists()

    content = output_file.read_text()

    assert ">contig_1" in content
    assert ">contig_2" in content
    assert ">contig_3" in content

    # Every returned contig should be present in FASTA
    for contig in contigs:
        assert contig in content
