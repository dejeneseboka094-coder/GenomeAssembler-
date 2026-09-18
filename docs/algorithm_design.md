# GenomeAssembler Algorithm Design

## 1. Input

The assembler accepts short-read sequencing data in FASTQ format.

The implementation supports:

- uncompressed FASTQ files
- gzip-compressed FASTQ files
- single-end FASTQ input
- paired-end FASTQ input

For paired-end data, R1 and R2 reads are streamed as pairs and both read sequences contribute k-mers to the assembly graph.

## 2. Read Validation and Preprocessing

The FASTQ parser performs basic input validation before assembly.

Validation includes:

- checking that the FASTQ file exists
- validating the four-line FASTQ record structure
- validating the `@` identifier
- validating the `+` separator
- checking sequence/quality length consistency
- converting sequences to uppercase

During k-mer generation, only canonical DNA bases (`A`, `C`, `G`, and `T`) are accepted.

Reads shorter than the selected k-mer size naturally generate no k-mers.

Quality-based trimming and adapter removal are outside the current core assembler and can be added as preprocessing extensions.

## 3. k-mer Generation

For a read of length L and k-mer size k, the number of possible k-mers is:

L - k + 1

Each k-mer is generated using a sliding window across the read.

Invalid k-mers containing bases outside A/C/G/T are skipped.

## 4. k-mer Counting

A Python `Counter` is used as a hash-table-based k-mer index.

For example:

    ATGC -> 20
    TGCG -> 18
    GCGA -> 19

The count represents the number of observed occurrences of each k-mer.

Low-frequency k-mers can represent sequencing errors, although singleton k-mers may also represent genuine low-coverage sequence.

## 5. de Bruijn Graph

The assembly graph is a de Bruijn graph.

- Nodes = (k-1)-mers
- Edges = k-mers
- Edge coverage = k-mer frequency

For example, for:

    ATGC

the prefix and suffix are:

    prefix = ATG
    suffix = TGC

Therefore:

    ATG -> TGC

The implementation stores outgoing edges in adjacency dictionaries and maintains reverse adjacency information for efficient predecessor lookup.

## 6. Graph Cleaning

Graph simplification is performed after graph construction.

The implemented cleaning steps include:

### 6.1 Low-coverage edge filtering

Edges whose k-mer coverage is below the selected minimum coverage threshold are removed.

For the main E. coli experiments:

    minimum coverage = 2

### 6.2 Tip removal

Short dead-end paths are identified and removed when they are shorter than or equal to the configured tip length and have lower coverage than a competing branch.

For the main experiments:

    tip length = 2

These operations are intended to reduce graph structures associated with sequencing errors and low-support branches.

## 7. Graph Traversal

The cleaned graph is traversed using a visited-edge strategy.

The traversal identifies maximal non-branching paths.

A path is extended while the current node has:

- exactly one predecessor
- exactly one outgoing edge

Branching points terminate the current path.

Visited edges are tracked to prevent inappropriate repeated traversal.

Isolated cyclic structures that are not captured by the first traversal stage are subsequently traversed separately.

## 8. Contig Generation

A graph path is converted into a DNA sequence.

The first node contributes the initial (k-1)-mer.

Each subsequent node contributes its final nucleotide.

For example:

    ATG -> TGC -> GCG -> CGA -> GAT

produces:

    ATGCGAT

Each resulting sequence represents an assembled contig.

## 9. Output

The assembled sequences are written to FASTA format.

Each contig receives a unique identifier:

    >contig_1
    SEQUENCE

The CLI allows the user to specify the output FASTA path.

## 10. Assembly Evaluation

The implementation calculates:

- number of contigs
- total assembly length
- N50
- largest contig
- average contig length
- percentage of reads incorporated

The current read-incorporation metric considers a read incorporated when its complete sequence occurs within at least one assembled contig.

This metric is reported separately from reference-based accuracy.

## 11. Reference-Based Validation

When a reference genome is available, assembled contigs can be aligned against the reference using BWA.

Reference-based evaluation includes:

- percentage of contigs mapped
- reference bases covered by assembled contigs
- alignment depth
- mapping quality
- approximate sequence identity using alignment edit distance

For the E. coli MG1655 experiment, the reference genome was:

    NC_000913.3
    4,641,652 bp

The 50,000-pair read dataset produced:

- 98.83% read mapping
- 95.14% reference coverage by reads
- approximately 3.15x mean read depth

For the k=51 assembly:

- 99.90% of contigs mapped to the reference
- 61.47% of reference bases were covered
- approximately 99.9868% sequence identity was observed among aligned contig bases

These metrics distinguish sequence correctness from assembly completeness and contiguity.

## 12. Benchmarking

The project includes a benchmarking module for measuring:

- execution time
- peak resident memory

The benchmark runs assembly in a separate process and monitors the child process using `psutil`.

An independent `/usr/bin/time -v` measurement was also used for the large k=51 experiment.

For the 50,000-pair E. coli dataset with k=51, minimum coverage 2, and tip length 2:

- execution time = 8 min 40.56 sec
- CPU utilization = 99%
- peak resident memory ≈ 5.76 GB
- exit status = 0

## 13. Experimental Variables

The effect of k-mer size was evaluated using:

    k = 21
    k = 31
    k = 41
    k = 51

The main experiments used:

    minimum coverage = 2
    tip length = 2

Using the same parameters across k values allows the effect of k-mer size to be investigated independently.

## 14. Scalability Experiment

The effect of the minimum k-mer coverage threshold was also investigated.

For k=51, the 50,000-pair dataset contained:

    7,034,865 unique k-mers

At minimum coverage 2:

    2,152,496 k-mers were retained.

At minimum coverage 1:

    all 7,034,865 unique k-mers would be retained.

The minimum-coverage-1 experiment was terminated during execution before completion. Because the current graph implementation uses Python dictionaries and sets, retaining millions of additional k-mers substantially increases memory requirements.

This demonstrates an important scalability limitation of the current prototype and motivates future memory optimization.

## 15. Complexity Analysis

Let:

- B = total number of input bases
- U = number of unique k-mers
- V = number of graph nodes
- E = number of graph edges
- C = number of contigs
- R = number of reads
- L = maximum tip length

Approximate complexities are:

| Operation | Time Complexity | Main Memory |
|---|---|---|
| FASTQ parsing | O(B) | O(1) streaming |
| k-mer generation/counting | O(B) average | O(U) |
| Graph construction | O(U) average | O(V + E) |
| Low-coverage filtering | O(E) | O(E) |
| Tip removal | approximately O(E x L) | O(E) |
| Contig traversal | O(V + E) | O(V + E) |
| N50 calculation | O(C log C) | O(C) |
| Read incorporation | O(R x C x L) worst case | O(R + C) |

Hash-table operations are treated as O(1) average-case operations.

## 16. Testing Strategy

The project uses automated unit and integration tests.

The test suite covers:

- FASTQ parsing
- k-mer generation
- k-mer counting
- graph construction
- graph cleaning
- traversal
- FASTA output
- evaluation metrics
- read incorporation
- pipeline integration
- benchmarking
- command-line interface

The final test suite contains 23 tests.

Final verification:

    23 passed

## 17. Command-Line Interface

The assembler can be executed using a Python module command.

Example:

    python -m src.assembler.cli \
        --input reads_R1.fastq \
        --input-r2 reads_R2.fastq \
        --k 51 \
        --min-coverage 2 \
        --tip-length 2 \
        --output contigs.fasta

The CLI provides configurable input files, paired-end support, k-mer size, graph-cleaning parameters, and output path.

## 18. Software Architecture

The implementation is divided into modular components:

    src/assembler/
        fastq.py
        kmer.py
        graph.py
        cleaning.py
        traversal.py
        assembly.py
        evaluation.py
        pipeline.py
        benchmarking.py
        reference_validation.py
        cli.py

This separation allows individual components to be tested and improved independently.

## 19. Implementation Principles

The implementation emphasizes:

- object-oriented programming
- hash-table-based k-mer indexing
- graph data structures
- graph traversal
- modular architecture
- streaming file processing
- exception handling
- unit and integration testing
- command-line execution
- profiling and benchmarking
- version control
- reproducibility

## 20. Current Limitations and Future Extensions

The current implementation is a prototype intended for small genomes and educational/experimental datasets.

Important limitations include:

- high memory overhead from Python graph data structures
- substantial fragmentation on low-depth E. coli data
- limited graph simplification compared with production assemblers
- no sophisticated repeat resolution
- no explicit paired-end distance constraints during graph traversal
- no quality-based trimming within the assembler
- limited error-correction strategies

Potential future improvements include:

- compact k-mer representations
- more memory-efficient graph structures
- Bloom filters or counting filters
- stronger error correction
- bubble resolution
- repeat-aware graph traversal
- explicit paired-end constraints
- parallel k-mer counting
- larger datasets and higher sequencing depth
- comparison with additional established assemblers
