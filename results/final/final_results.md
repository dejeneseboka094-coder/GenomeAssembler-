# GenomeAssembler Final Experimental Results

## Dataset

- Organism: *Escherichia coli* K-12 MG1655
- Dataset: 50,000 paired-end read pairs
- R1 reads: 50,000
- R2 reads: 50,000
- Total reads: 100,000
- Read length: 151 bp
- Reference: NC_000913.3
- Reference length: 4,641,652 bp

## Assembly parameters

- Minimum k-mer coverage: 2
- Tip length: 2
- Tested k-mer sizes: 21, 31, 41, 51

## k-mer-size experiment

| k | Contigs | Total length (bp) | Largest contig (bp) | Average length (bp) | N50 (bp) |
|---:|---:|---:|---:|---:|---:|
| 21 | 42,024 | 4,084,017 | 786 | 97.18 | 151 |
| 31 | 37,805 | 3,996,942 | 846 | 105.73 | 146 |
| 41 | 35,767 | 3,932,085 | 846 | 109.94 | 139 |
| 51 | 34,418 | 3,873,375 | 1,038 | 112.54 | 133 |

## k=51 computational performance

- Execution time: 8 min 40.56 sec
- CPU utilization: 99%
- Peak resident memory: approximately 5.76 GB
- Exit status: 0

## Read-level reference validation

- Primary reads: 100,000
- Mapped reads: 98,907
- Read mapping rate: 98.83%
- Properly paired: 97.95%
- Singletons: 0.40%
- Reference coverage by reads: 95.14%
- Mean read depth: approximately 3.15x

## k=51 contig reference validation

- Primary contigs: 34,418
- Mapped contigs: 34,387
- Contig mapping rate: 99.90%
- Reference coverage by contigs: 61.47%
- Mean alignment depth: 0.834x
- Approximate sequence identity among aligned contig bases: 99.9868%

The approximate identity is calculated from aggregate alignment edit distance and is not a formal global assembly accuracy metric.

## Scalability experiment

For k=51:

- Unique k-mers: 7,034,865
- Total k-mer occurrences: 10,100,000
- K-mers retained at minimum coverage 2: 2,152,496
- Singleton k-mers removed at minimum coverage 2: 4,882,369

The minimum-coverage-1 assembly was started but terminated before completion. The exact cause could not be confirmed from available system diagnostics.

## Existing Velvet baseline

An existing Velvet assembly baseline was available:

- Contigs >500 bp: 203
- Total assembly length: 4,536,804 bp
- Largest contig: 132,857 bp
- N50: 53,779 bp
- N90: 11,001 bp
- L50: 30
- L90: 101
- GC: 50.74%

The exact Velvet command and settings could not be recovered, so this is not treated as a controlled apples-to-apples benchmark.

## Main observations

1. Increasing k reduced the number of contigs.
2. Increasing k increased average contig length.
3. Increasing k increased the largest contig from 786 bp to 1,038 bp.
4. Total assembly length decreased as k increased.
5. N50 decreased from 151 bp at k=21 to 133 bp at k=51.
6. The k-mer experiment therefore demonstrates a trade-off rather than a universally optimal k-mer size.
7. The k=51 assembly showed high mapping and approximate sequence identity among aligned contig bases but covered only 61.47% of the reference.
8. The prototype has substantial memory overhead because graph and k-mer structures use Python dictionaries and sets.
