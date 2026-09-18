from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "final" / "GenomeAssembler_Final_Report.docx"

doc = Document()

# Page setup
section = doc.sections[0]
section.top_margin = Inches(0.75)
section.bottom_margin = Inches(0.75)
section.left_margin = Inches(0.9)
section.right_margin = Inches(0.9)

styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(10.5)

for style_name in ["Title", "Heading 1", "Heading 2", "Heading 3"]:
    styles[style_name].font.name = "Arial"

# Helper functions
def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(20)
    return p

def add_center(text, size=12, bold=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.size = Pt(size)
    r.bold = bold
    return p

def add_heading(text, level=1):
    doc.add_heading(text, level=level)

def add_para(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p

def add_bullets(items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(item)

def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"

    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = str(header)
        shade_cell(cell, "D9EAF7")
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    return table

# Title page
add_title("Development of a Genome Assembly Algorithm")
add_center("for Reconstruction of Genomic Sequences from Short-Read Sequencing Data", 15)
doc.add_paragraph()
add_center("GenomeAssembler", 16, True)
doc.add_paragraph()
add_center("Advanced Programming for Bioinformatics — Project 1", 12)
add_center("Addis Ababa University", 12)
add_center("MSc Bioinformatics", 12)
doc.add_paragraph()
add_center("Final Technical Report", 14, True)
doc.add_page_break()

# Abstract
add_heading("1. Abstract")
add_para(
    "Genome assembly is the computational reconstruction of genomic sequences from sequencing reads. "
    "Short-read assembly is challenging because sequencing errors, repetitive sequences, and insufficient "
    "sequencing depth can produce fragmented or incorrect assemblies. This project presents GenomeAssembler, "
    "an educational and experimental short-read genome assembler based on the de Bruijn graph approach."
)
add_para(
    "The assembler was implemented in Python using modular components for FASTQ parsing, k-mer generation "
    "and counting, de Bruijn graph construction, graph cleaning, graph traversal, contig generation, assembly "
    "evaluation, benchmarking, reference validation, and command-line execution. The implementation supports "
    "uncompressed and gzip-compressed FASTQ files as well as single-end and paired-end reads."
)
add_para(
    "The effect of k-mer size was evaluated using k=21, 31, 41, and 51 on a paired-end Escherichia coli "
    "dataset containing 50,000 read pairs. Increasing k reduced the number of contigs from 42,024 at k=21 "
    "to 34,418 at k=51, while average contig length increased from 97.18 bp to 112.54 bp. However, total "
    "assembly length and N50 decreased as k increased, demonstrating a k-mer-size trade-off."
)
add_para(
    "For k=51, assembly completed in 8 min 40.56 sec with approximately 5.76 GB peak resident memory and "
    "99% CPU utilization. Reference-based validation showed that 99.90% of assembled contigs mapped to the "
    "E. coli MG1655 reference, covering 61.47% of the reference genome. Approximate sequence identity among "
    "aligned contig bases was 99.9868%. The results demonstrate a functional de Bruijn graph assembler while "
    "also identifying important scalability and graph-simplification limitations."
)

# Introduction
add_heading("2. Introduction")
add_para(
    "Genome assembly is the process of reconstructing a genome sequence from sequencing reads. In short-read "
    "sequencing, the genome is represented by many relatively short DNA fragments. Computational assembly "
    "methods determine how these fragments connect to form longer sequences called contigs."
)
add_para(
    "The de Bruijn graph is a standard graph representation for short-read assembly. Reads are decomposed "
    "into k-mers, with each k-mer represented as an edge between its prefix and suffix, which are (k-1)-mers. "
    "The resulting graph can be simplified and traversed to reconstruct genomic sequences."
)
add_para(
    "The objective of this project was to develop a functional genome assembly algorithm using the de Bruijn "
    "graph approach while applying advanced programming concepts including object-oriented programming, graph "
    "data structures, hash-table-based indexing, modular architecture, complexity analysis, testing, "
    "benchmarking, command-line interfaces, and version control."
)

# Objectives
add_heading("3. Objectives")
add_bullets([
    "Develop a short-read genome assembly algorithm based on a de Bruijn graph.",
    "Implement FASTQ input processing.",
    "Generate and count k-mers using hash-based data structures.",
    "Construct a de Bruijn graph using (k-1)-mers as nodes and k-mers as edges.",
    "Remove low-frequency graph edges and short erroneous structures.",
    "Traverse the cleaned graph to generate assembled contigs.",
    "Produce contigs in FASTA format.",
    "Calculate standard assembly metrics.",
    "Investigate the effect of k-mer size.",
    "Measure execution time and memory consumption.",
    "Validate the assembly against a known reference genome.",
    "Compare the prototype with an established assembler baseline.",
    "Develop automated tests and a reproducible command-line workflow.",
])

# Architecture
add_heading("4. System Design and Architecture")
add_para("The assembler was implemented as a modular Python package:")
add_para(
    "src/assembler/fastq.py\n"
    "src/assembler/kmer.py\n"
    "src/assembler/graph.py\n"
    "src/assembler/cleaning.py\n"
    "src/assembler/traversal.py\n"
    "src/assembler/assembly.py\n"
    "src/assembler/evaluation.py\n"
    "src/assembler/pipeline.py\n"
    "src/assembler/benchmarking.py\n"
    "src/assembler/reference_validation.py\n"
    "src/assembler/cli.py"
)
add_para(
    "Overall pipeline: FASTQ reads → validation → k-mer generation → k-mer counting → "
    "low-coverage filtering → de Bruijn graph → graph cleaning → traversal → contigs → "
    "FASTA → evaluation/reference validation/benchmarking."
)

# Methodology
add_heading("5. Methodology")
add_heading("5.1 FASTQ Processing", 2)
add_para(
    "The FASTQ parser supports uncompressed and gzip-compressed files and single-end and paired-end input. "
    "Validation checks file existence, FASTQ record structure, the @ identifier, the + separator, and "
    "sequence/quality length consistency. Sequences are converted to uppercase."
)
add_heading("5.2 k-mer Generation and Counting", 2)
add_para(
    "For a sequence of length L and k-mer size k, L-k+1 k-mers are generated using a sliding window. "
    "Only A, C, G, and T k-mers are accepted. Python Counter is used as a hash-table-based k-mer index."
)
add_heading("5.3 de Bruijn Graph", 2)
add_para(
    "Nodes represent (k-1)-mers and edges represent k-mers. Edge coverage stores k-mer frequency. "
    "Outgoing adjacency dictionaries and reverse adjacency sets are maintained for graph traversal."
)
add_heading("5.4 Graph Cleaning", 2)
add_para(
    "Edges with coverage below the minimum threshold are removed. Short dead-end paths are also removed "
    "when they satisfy the configured tip-length condition and have lower coverage than a competing branch."
)
add_heading("5.5 Graph Traversal", 2)
add_para(
    "A visited-edge strategy identifies maximal non-branching paths. Paths are extended while the current "
    "node has exactly one predecessor and one outgoing edge. Remaining isolated cyclic structures are "
    "processed separately."
)
add_heading("5.6 Contig Generation", 2)
add_para(
    "The first graph node contributes the initial (k-1)-mer and each subsequent node contributes its final "
    "nucleotide. The resulting DNA sequence is written to FASTA."
)

# Dataset
add_heading("6. Experimental Setup")
add_para(
    "The primary dataset was paired-end Escherichia coli K-12 MG1655 sequencing data."
)
add_table(
    ["Parameter", "Value"],
    [
        ["R1 reads", "50,000"],
        ["R2 reads", "50,000"],
        ["Total reads", "100,000"],
        ["Read length", "151 bp"],
        ["Reference", "NC_000913.3"],
        ["Reference length", "4,641,652 bp"],
        ["Minimum k-mer coverage", "2"],
        ["Tip length", "2"],
        ["Tested k values", "21, 31, 41, 51"],
    ],
)

# Results
add_heading("7. Results")
add_heading("7.1 Effect of k-mer Size", 2)
add_table(
    ["k", "Contigs", "Total bp", "Largest bp", "Average bp", "N50 bp"],
    [
        [21, "42,024", "4,084,017", "786", "97.18", "151"],
        [31, "37,805", "3,996,942", "846", "105.73", "146"],
        [41, "35,767", "3,932,085", "846", "109.94", "139"],
        [51, "34,418", "3,873,375", "1,038", "112.54", "133"],
    ],
)
add_para(
    "Increasing k reduced the number of contigs and increased average and largest contig length. "
    "At the same time, total assembly length and N50 decreased. These results demonstrate a trade-off "
    "between different assembly characteristics rather than a universally optimal k-mer size."
)

add_heading("7.2 Computational Performance", 2)
add_table(
    ["Metric", "k=51 result"],
    [
        ["Wall-clock time", "8 min 40.56 sec"],
        ["CPU utilization", "99%"],
        ["Peak resident memory", "approximately 5.76 GB"],
        ["Exit status", "0"],
    ],
)

add_heading("7.3 Reference-Based Validation", 2)
add_para("Read-level validation:")
add_table(
    ["Metric", "Result"],
    [
        ["Primary reads", "100,000"],
        ["Mapped reads", "98,907"],
        ["Read mapping rate", "98.83%"],
        ["Properly paired", "97.95%"],
        ["Singletons", "0.40%"],
        ["Reference coverage by reads", "95.14%"],
        ["Mean read depth", "approximately 3.15×"],
    ],
)
add_para("k=51 contig validation:")
add_table(
    ["Metric", "Result"],
    [
        ["Primary contigs", "34,418"],
        ["Mapped contigs", "34,387"],
        ["Contig mapping rate", "99.90%"],
        ["Reference coverage", "61.47%"],
        ["Mean alignment depth", "0.834×"],
        ["Approximate identity", "99.9868%"],
    ],
)
add_para(
    "The approximate identity is calculated from aggregate alignment edit distance among aligned contig "
    "bases. It is not a formal global assembly accuracy metric. Similarly, the 99.90% contig mapping rate "
    "should not be interpreted as 99.90% whole-genome accuracy."
)

# Scalability
add_heading("8. Scalability Analysis")
add_table(
    ["Metric", "Result"],
    [
        ["Unique k-mers at k=51", "7,034,865"],
        ["Total k-mer occurrences", "10,100,000"],
        ["Retained at minimum coverage 2", "2,152,496"],
        ["Singleton k-mers removed", "4,882,369"],
    ],
)
add_para(
    "The minimum-coverage-1 assembly was started but terminated before completion. The exact cause could "
    "not be confirmed from available system diagnostics. The experiment nevertheless demonstrated the "
    "scalability limitation of the current implementation: Python dictionaries and sets have substantial "
    "memory overhead when millions of k-mers and graph structures are retained."
)

# Comparison
add_heading("9. Comparison with Established Assembler")
add_table(
    ["Metric", "Velvet baseline", "GenomeAssembler k=51"],
    [
        ["Contigs >500 bp", "203", "Not directly equivalent"],
        ["Total assembly length", "4,536,804 bp", "3,873,375 bp"],
        ["Largest contig", "132,857 bp", "1,038 bp"],
        ["N50", "53,779 bp", "133 bp"],
    ],
)
add_para(
    "The existing Velvet baseline is substantially less fragmented than the prototype results. However, "
    "the exact Velvet command and settings could not be recovered, so this is not treated as a controlled "
    "apples-to-apples benchmark. The comparison illustrates the gap between an educational prototype and "
    "a mature assembler with more sophisticated error correction, graph simplification, repeat resolution, "
    "and memory optimization."
)

# Testing
add_heading("10. Testing and Software Quality")
add_para(
    "The final automated test suite contains 23 tests, and all 23 tests passed. Tests cover FASTQ parsing, "
    "k-mer generation and counting, graph construction and cleaning, traversal, FASTA output, evaluation "
    "metrics, read incorporation, pipeline integration, benchmarking, and the command-line interface."
)
add_para(
    "The project was developed under Git version control using incremental commits. The final repository "
    "working tree was clean after the implementation and documentation were finalized."
)

# Discussion
add_heading("11. Discussion")
add_para(
    "The implementation demonstrates the principal stages of short-read de Bruijn graph assembly. "
    "The k-mer experiments showed that increasing k changed graph connectivity and assembly fragmentation. "
    "Fewer contigs and longer average contigs were observed at larger k values, while N50 and total assembly "
    "length declined."
)
add_para(
    "Reference validation provided additional evidence that assembled sequences correspond to the target "
    "genome. The k=51 assembly had a high contig mapping rate and high approximate identity among aligned "
    "bases, but reference coverage was only 61.47%. Thus, sequence agreement among mapped contigs does not "
    "imply complete genome reconstruction."
)
add_para(
    "The low sequencing depth of the experimental subset also contributes to fragmentation. Finally, the "
    "scalability experiment demonstrated that the current Python data structures become costly as the number "
    "of unique k-mers increases."
)

# Limitations
add_heading("12. Limitations")
add_bullets([
    "High memory overhead from Python dictionaries and sets.",
    "Substantial fragmentation on the low-depth E. coli dataset.",
    "Limited graph simplification compared with production assemblers.",
    "No sophisticated repeat resolution.",
    "No explicit paired-end distance constraints during graph traversal.",
    "No quality-based trimming or adapter removal inside the core assembler.",
    "Limited error-correction strategies.",
    "No bubble resolution.",
    "Read-incorporation calculation can become expensive for large assemblies.",
    "The prototype is not intended for production-scale genome assembly.",
])

# Future work
add_heading("13. Future Work")
add_bullets([
    "Compact numerical k-mer representations.",
    "More memory-efficient graph structures.",
    "Bloom filters or counting filters.",
    "Stronger sequencing-error correction.",
    "Bubble detection and resolution.",
    "Repeat-aware graph traversal.",
    "Explicit paired-end constraints.",
    "Parallel k-mer counting.",
    "Improved memory management.",
    "Larger and higher-depth datasets.",
    "Controlled comparison with established assemblers.",
    "Additional assembly-quality and misassembly metrics.",
])

# Conclusion
add_heading("14. Conclusion")
add_para(
    "This project developed a functional short-read genome assembler based on the de Bruijn graph algorithm. "
    "The implementation covers FASTQ input, k-mer counting, graph construction, graph cleaning, graph "
    "traversal, contig generation, FASTA output, assembly evaluation, reference validation, benchmarking, "
    "automated testing, and command-line execution."
)
add_para(
    "Experiments using k=21, 31, 41, and 51 demonstrated measurable effects of k-mer size on assembly "
    "structure. The k=51 assembly showed high agreement among contig sequences that mapped to the reference, "
    "while also revealing incomplete genome coverage and substantial computational requirements."
)
add_para(
    "The project therefore demonstrates the core principles of short-read de Bruijn graph assembly while "
    "providing a clear foundation for future improvements in error correction, repeat resolution, graph "
    "representation, parallelization, and scalability."
)

# References
add_heading("15. References")
add_para(
    "1. Project 1 specification: Development of a Genome Assembly Algorithm for Reconstruction of Genomic "
    "Sequences from Short-Read Sequencing Data, Advanced Programming for Bioinformatics."
)
add_para(
    "2. NC_000913.3, Escherichia coli K-12 substr. MG1655 complete genome, used as the reference sequence "
    "for assembly validation."
)
add_para(
    "3. Velvet assembler baseline results used for contextual comparison. Exact command and settings were "
    "not available and therefore the comparison is reported with this limitation."
)
add_para(
    "4. GenomeAssembler project source code and technical documentation, maintained under Git version control."
)

# Appendix
add_heading("Appendix A. Example CLI Command")
add_para(
    "python -m src.assembler.cli \\\n"
    "    --input reads_R1.fastq \\\n"
    "    --input-r2 reads_R2.fastq \\\n"
    "    --k 51 \\\n"
    "    --min-coverage 2 \\\n"
    "    --tip-length 2 \\\n"
    "    --output contigs.fasta"
)

add_heading("Appendix B. Final Verification")
add_table(
    ["Verification item", "Status"],
    [
        ["Automated tests", "23/23 passed"],
        ["Git working tree", "Clean"],
        ["FASTQ parser", "Implemented"],
        ["Paired-end support", "Implemented"],
        ["k-mer counting", "Implemented"],
        ["de Bruijn graph", "Implemented"],
        ["Graph cleaning", "Implemented"],
        ["Contig traversal", "Implemented"],
        ["FASTA output", "Implemented"],
        ["Assembly metrics", "Implemented"],
        ["Benchmarking", "Implemented"],
        ["Reference validation", "Completed"],
        ["Technical documentation", "Completed"],
        ["Final experimental results", "Committed"],
    ],
)

OUT.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUT)
print(f"Created: {OUT}")
