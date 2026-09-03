from src.assembler.pipeline import assemble


def test_assemble_simulated_data(tmp_path):
    output_file = tmp_path / "assembled.fasta"

    contigs = assemble(
        "data/simulated/reads.fastq",
        output_file,
        k=5,
        min_coverage=2,
        tip_length=2,
    )

    assert len(contigs) == 3
    assert output_file.exists()

    content = output_file.read_text()

    assert ">contig_1" in content
    assert ">contig_2" in content
    assert ">contig_3" in content

    for contig in contigs:
        assert contig in content
