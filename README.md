# GenomeAssembler

## Project Title

Development of a Genome Assembly Algorithm for Reconstruction of Genomic Sequences from Short-Read Sequencing Data

## Project Description

This project develops a genome assembly algorithm for reconstructing genomic sequences from short-read sequencing data using a de Bruijn graph approach.

The assembler will:
- Read sequencing data in FASTQ format
- Perform basic read preprocessing
- Generate and count k-mers
- Construct a de Bruijn graph
- Remove low-frequency and erroneous graph structures
- Traverse the graph
- Generate assembled contigs
- Write contigs in FASTA format
- Evaluate assembly quality and computational performance

## Core Algorithm

FASTQ reads
    ↓
Read preprocessing
    ↓
k-mer generation
    ↓
k-mer counting
    ↓
Low-frequency k-mer filtering
    ↓
de Bruijn graph construction
    ↓
Graph cleaning
    ↓
Graph traversal
    ↓
Contig generation
    ↓
FASTA output
    ↓
Assembly evaluation

## Experimental Plan

The assembler will initially be tested using simulated small-genome sequencing reads with a known reference sequence.

After validating the implementation, the assembler will be tested on short-read sequencing data.

Multiple k-mer sizes will be evaluated, including:
- k = 21
- k = 31
- k = 41
- k = 51

Assembly results will be evaluated using assembly statistics and computational performance measurements.

Where appropriate, results will be compared with an established assembler.

## Software Architecture

The implementation will use a modular Python architecture:

src/assembler/
    fastq.py
    preprocessing.py
    kmer.py
    graph.py
    cleaning.py
    traversal.py
    assembly.py
    evaluation.py
    benchmarking.py
    cli.py

## Testing

Unit tests and integration tests will be developed throughout implementation.

## Reproducibility

The project is maintained using Git version control.
