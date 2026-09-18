# GenomeAssembler

## Development of a Genome Assembly Algorithm for Reconstruction of Genomic Sequences from Short-Read Sequencing Data

GenomeAssembler is a Python-based genome assembly prototype for reconstructing genomic sequences from short-read sequencing data using a de Bruijn graph approach.

The project was developed as an Advanced Programming for Bioinformatics project and implements FASTQ processing, k-mer counting, de Bruijn graph construction, graph cleaning, graph traversal, contig generation, assembly evaluation, benchmarking, and reference-based validation.

## Project Objectives

- Read short-read sequencing data in FASTQ format.
- Support single-end and paired-end FASTQ input.
- Generate and count k-mers.
- Construct a de Bruijn graph.
- Remove low-coverage and erroneous graph structures.
- Remove short dead-end branches (tips).
- Traverse the graph and generate contigs.
- Write assembled contigs in FASTA format.
- Calculate assembly statistics.
- Measure computational performance.
- Perform reference-based validation when a reference is available.
- Provide automated unit and integration tests.
- Provide a command-line interface.
- Support reproducible computational experiments.

## Assembly Workflow

```text
FASTQ reads
    |
    v
Read validation and preprocessing
    |
    v
k-mer generation
    |
    v
k-mer counting
    |
    v
Low-coverage k-mer filtering
    |
    v
de Bruijn graph construction
    |
    v
Graph cleaning
    |
    +--> Low-coverage edge removal
    |
    +--> Tip removal
    |
    v
Graph traversal
    |
    v
Contig generation
    |
    v
Assembly evaluation
## Repository Structure

```text
GenomeAssembler/
├── benchmarks/
├── data/
│   ├── processed/
│   ├── raw/
│   └── simulated/
├── docs/
├── results/
│   └── final/
├── scripts/
├── src/
│   └── assembler/
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
## Requirements

- Python 3.12
- Git
- pytest
- psutil
- Linux or macOS

BWA and SAMtools are required only for reference-based validation.

## Installation
## Testing

Run:

```bash
pytest -q
Current result:

```text
23 passed
Command-Line Interface

Single-End

python -m src.assembler.cli \
    --input INPUT \
    --output OUTPUT \
    --k 31 \
    --min-coverage 2 \
    --tip-length 2

Paired-End

python -m src.assembler.cli \
    --input R1.fastq \
    --input-r2 R2.fastq \
    --output contigs.fasta \
    --k 31 \
    --min-coverage 2 \
    --tip-length 2

Parameters

--input          Input FASTQ file
--input-r2       Optional paired-end R2 FASTQ
--output         Output FASTA file
--k              k-mer size
--min-coverage   Minimum k-mer/edge coverage
--tip-length     Maximum tip length removed
Quick Start

Example using the simulated E. coli dataset:

python -m src.assembler.cli \
    --input data/simulated/Ecoli_test10000_R1.fastq \
    --input-r2 data/simulated/Ecoli_test10000_R2.fastq \
    --k 31 \
    --min-coverage 2 \
    --tip-length 2 \
    --output results/k31/Ecoli_test10000_contigs.fasta


Algorithm

GenomeAssembler uses a k-mer-based de Bruijn graph assembly strategy.

FASTQ Processing

Reads are parsed and validated from FASTQ files.

Both single-end and paired-end reads are supported.

k-mer Generation

Reads are divided into overlapping k-mers.

For example, with k = 3:

ACGTACGT
ACG
CGT
GTA
TAC
ACG

k-mer Counting

A hash-table-based Counter stores k-mer frequencies.

Low-frequency k-mers can be filtered to reduce sequencing-error-derived graph structures.

de Bruijn Graph

For each k-mer, the first and last (k-1) bases define the graph nodes.

For example:

ACGT

creates an edge:

ACG → CGT

Graph Cleaning

The graph is simplified by:

- removing low-coverage edges
- removing short dead-end branches (tips)

Graph Traversal

The graph is traversed using maximal non-branching paths to generate contigs.

Isolated cycles are also handled.

Contig Generation

Traversed paths are converted into nucleotide sequences and written to FASTA.


Assembly Evaluation

The assembler calculates:

- number of contigs
- total assembly length
- largest contig
- average contig length
- N50
- read incorporation percentage

Computational performance is measured using execution time and peak memory.


Experimental Setup

The main experiment used approximately 50,000 paired-end E. coli read pairs.

Parameters:

k = 21, 31, 41, 51
minimum coverage = 2
tip length = 2


Assembly Results

k       Contigs    Total Length (bp)    Largest Contig (bp)    Average Length (bp)    N50 (bp)
21      42,024     4,084,017            786                    97.18                  151
31      37,805     3,996,942            846                   105.73                  146
41      35,767     3,932,085            846                   109.94                  139
51      34,418     3,873,375           1,038                  112.54                  133

Increasing k reduced the number of contigs and increased the average and largest contig lengths, while total assembly length and N50 decreased in these experiments.

These results demonstrate a trade-off between k-mer size and assembly characteristics rather than a single universally optimal k-mer size.
Quick Start

Example using the simulated E. coli dataset:

python -m src.assembler.cli \
    --input data/simulated/Ecoli_test10000_R1.fastq \
    --input-r2 data/simulated/Ecoli_test10000_R2.fastq \
    --k 31 \
    --min-coverage 2 \
    --tip-length 2 \
    --output results/k31/Ecoli_test10000_contigs.fasta


Algorithm

GenomeAssembler uses a k-mer-based de Bruijn graph assembly strategy.

FASTQ Processing

Reads are parsed and validated from FASTQ files.

Both single-end and paired-end reads are supported.

k-mer Generation

Reads are divided into overlapping k-mers.

For example, with k = 3:

ACGTACGT
ACG
CGT
GTA
TAC
ACG

k-mer Counting

A hash-table-based Counter stores k-mer frequencies.

Low-frequency k-mers can be filtered to reduce sequencing-error-derived graph structures.

de Bruijn Graph

For each k-mer, the first and last (k-1) bases define the graph nodes.

For example:

ACGT

creates an edge:

ACG → CGT

Graph Cleaning

The graph is simplified by:

- removing low-coverage edges
- removing short dead-end branches (tips)

Graph Traversal

The graph is traversed using maximal non-branching paths to generate contigs.

Isolated cycles are also handled.

Contig Generation

Traversed paths are converted into nucleotide sequences and written to FASTA.


Assembly Evaluation

The assembler calculates:

- number of contigs
- total assembly length
- largest contig
- average contig length
- N50
- read incorporation percentage

Computational performance is measured using execution time and peak memory.


Experimental Setup

The main experiment used approximately 50,000 paired-end E. coli read pairs.

Parameters:

k = 21, 31, 41, 51
minimum coverage = 2
tip length = 2


Assembly Results

k       Contigs    Total Length (bp)    Largest Contig (bp)    Average Length (bp)    N50 (bp)
21      42,024     4,084,017            786                    97.18                  151
31      37,805     3,996,942            846                   105.73                  146
41      35,767     3,932,085            846                   109.94                  139
51      34,418     3,873,375           1,038                  112.54                  133

Increasing k reduced the number of contigs and increased the average and largest contig lengths, while total assembly length and N50 decreased in these experiments.

These results demonstrate a trade-off between k-mer size and assembly characteristics rather than a single universally optimal k-mer size.
Performance Benchmark

For 50,000 read pairs with k = 51, minimum coverage = 2, and tip length = 2:

Wall time:       8 min 40.56 sec
CPU utilization: 99%
Peak memory:     approximately 5.76 GB
Exit status:     0


Reference-Based Validation

The E. coli K-12 MG1655 reference genome is 4,641,652 bp.

For the k=51 assembly:

Primary contigs:             34,418
Mapped contigs:              34,387
Mapped percentage:            99.90%
Reference coverage:           61.47%
Mean depth:                    0.83×
Mean mapping quality:         59
Approximate aligned identity: 99.9868%

The mapped-contig percentage should not be interpreted as assembly accuracy.

The approximate identity represents identity among aligned contig bases and is not a formal global assembly-accuracy measure.


Read-Level Validation

For the evaluated reads:

Primary reads:          100,000
Mapped reads:            98,907
Mapped percentage:       98.83%
Properly paired:          97.95%
Reference coverage:       95.14%
Mean depth:                3.15×
Mean base quality:        32.1
Mean mapping quality:     59

These values describe read alignment to the reference rather than directly measuring assembly accuracy.


Scalability

For the k=51, 50,000-pair experiment:

Unique k-mers:             7,034,865
Total k-mer occurrences:  10,100,000
Coverage-1 k-mers:         4,882,369
Coverage-2 k-mers:         1,503,795
Retained k-mers ≥2:        2,152,496

Approximately 69.4% of the unique k-mers occurred only once.

The experiment demonstrates that the current Python dictionary/set-based graph representation has substantial memory requirements.
Comparison with Velvet

An existing Velvet baseline was available:

Metric                     Velvet
Contigs >500 bp             203
Total length                4,536,804 bp
Largest contig              132,857 bp
N50                         53,779 bp
N90                         11,001 bp
L50                         30
L90                         101
GC                          50.74%

The original Velvet command and configuration could not be recovered, so this is treated as an existing baseline rather than a fully controlled comparison.


Software Architecture

The implementation is organized into modular components:

fastq.py                  FASTQ parsing and validation
kmer.py                   k-mer generation and counting
graph.py                  de Bruijn graph representation
cleaning.py               graph simplification
traversal.py              graph traversal
assembly.py               FASTA output
evaluation.py             assembly metrics
benchmarking.py           performance benchmarking
reference_validation.py   reference validation
pipeline.py               end-to-end assembly
cli.py                    command-line interface


Complexity

Let N be the total number of input bases and U the number of unique k-mers.

Approximate complexity:

k-mer generation:       O(N)
k-mer counting:         expected O(N)
graph construction:     expected O(U)
graph traversal:        approximately O(V + E)
FASTA output:           proportional to contig sequence length

Memory consumption is dominated by Python hash tables and graph objects.


Testing and Quality Assurance

The project includes unit and integration tests for:

- FASTQ parsing
- FASTQ validation
- k-mer generation
- k-mer counting
- graph construction
- graph cleaning
- tip removal
- graph traversal
- contig generation
- assembly metrics
- paired-end processing
- CLI behavior
- end-to-end assembly

Current test result:

23 passed
Documentation

Technical algorithm documentation:

docs/algorithm_design.md

Final experimental results:

results/final/final_results.md

Final technical report:

results/final/GenomeAssembler_Final_Report.docx


Reproducibility

The project uses Git for version control.

Large sequencing and reference files are excluded from Git using .gitignore.

The repository contains source code, tests, documentation, benchmark scripts, reproducible commands, summarized results, and the final technical report.


Limitations

The current implementation is an educational and experimental prototype.

Main limitations include:

- high memory overhead from Python graph structures
- limited scalability to large datasets
- limited repeat resolution
- limited use of paired-end distance information
- no multi-k assembly
- limited parallel processing
- Velvet comparison is not fully controlled
- reference validation depends on external alignment tools


Future Improvements

Potential extensions include:

- memory-efficient graph structures
- compact k-mer encoding
- parallel k-mer counting
- multiprocessing
- multi-k assembly
- improved repeat resolution
- paired-end insert-size constraints
- additional reference validation
- controlled comparison with other assemblers
- profiling-guided optimization


Project Status

The current prototype implements:

- FASTQ processing
- single-end and paired-end support
- k-mer generation and counting
- de Bruijn graph construction
- graph cleaning
- graph traversal
- contig generation
- FASTA output
- assembly evaluation
- benchmarking
- reference validation
- command-line interface
- automated testing
- technical documentation
- reproducible experimental results

Current test suite: 23 tests passed.


Author

Dejene Seboka Leta

MSc Bioinformatics
Addis Ababa University


License

This project is developed for academic and educational purposes.
