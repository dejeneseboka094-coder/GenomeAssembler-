from src.assembler.assembly import write_fasta


def test_write_fasta(tmp_path):
    contigs = [
        "ATGC",
        "TGCG",
        "TGCT",
    ]

    output_file = tmp_path / "contigs.fasta"

    write_fasta(contigs, output_file)

    assert output_file.exists()

    content = output_file.read_text()

    expected = (
        ">contig_1\n"
        "ATGC\n"
        ">contig_2\n"
        "TGCG\n"
        ">contig_3\n"
        "TGCT\n"
    )

    assert content == expected
