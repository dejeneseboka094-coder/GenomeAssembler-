# GenomeAssembler Algorithm Design

## 1. Input

The assembler accepts short-read sequencing data in FASTQ format.

The implementation should support both uncompressed FASTQ and gzip-compressed FASTQ files where practical.

## 2. Read Preprocessing

Reads will be checked before assembly.

Basic preprocessing includes:
- validation of DNA sequences
- removal of invalid reads
- removal of reads shorter than the selected k-mer size
- optional quality-based filtering

## 3. k-mer Generation

For a read of length L and k-mer size k, the number of k-mers generated is:

L - k + 1

Each k-mer is generated using a sliding window across the read.

## 4. k-mer Counting

A hash-table/dictionary-based structure will store k-mer frequencies.

Example:

ATGC -> 20
TGCG -> 18
GCGA -> 19

K-mers with very low frequency may represent sequencing errors.

## 5. de Bruijn Graph

The graph will use:

- Nodes = (k-1)-mers
- Edges = k-mers

For a k-mer:

ATGC

the prefix and suffix are:

prefix = ATG
suffix = TGC

Therefore:

ATG -> TGC

The k-mer count can be stored as edge coverage.

## 6. Graph Cleaning

The graph will be simplified by identifying and removing structures likely to result from sequencing errors.

Initial cleaning strategies include:
- low-frequency k-mer removal
- dead-end/tip removal
- removal of short erroneous paths

## 7. Graph Traversal

The cleaned graph will be traversed to identify paths corresponding to genomic sequences.

The traversal must:
- follow graph edges
- track visited edges
- terminate appropriately at dead ends or branching structures
- avoid inappropriate repeated edge usage

## 8. Contig Generation

A graph path will be converted into a DNA sequence.

The first node contributes the initial (k-1)-mer.

Each subsequent node contributes its final nucleotide.

Example:

ATG -> TGC -> GCG -> CGA -> GAT

produces:

ATGCGAT

## 9. Output

The assembled sequences will be written as contigs in FASTA format.

## 10. Evaluation

Assembly evaluation will include:

- number of contigs
- total assembly length
- N50
- largest contig
- average contig length
- percentage of reads incorporated
- execution time
- memory consumption
- accuracy when a reference is available

## 11. Experimental Variables

The effect of k-mer size will be evaluated using multiple k values.

Initial experimental values:

k = 21
k = 31
k = 41
k = 51

## 12. Testing Strategy

Development will begin with a small simulated genome for which the true sequence is known.

The assembler will then be tested on increasingly realistic sequencing data.

## 13. Implementation Principles

The implementation will emphasize:

- object-oriented programming
- hash tables
- graph data structures
- graph traversal
- modular architecture
- memory-efficient processing
- file/stream processing
- exception handling
- unit testing
- integration testing
- profiling and benchmarking
- version control
