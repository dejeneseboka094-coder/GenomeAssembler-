from src.assembler.pipeline import assemble
from src.assembler.benchmarking import benchmark_assembly


result, benchmark_metrics = benchmark_assembly(
    assemble,
    "data/simulated/reads.fastq",
    "results/benchmark_simulated.fasta",
    k=5,
    min_coverage=2,
    tip_length=2,
)

contigs, assembly_metrics = result

print("Assembly metrics:")
for key, value in assembly_metrics.items():
    print(f"{key}: {value}")

print("\nBenchmark metrics:")
for key, value in benchmark_metrics.items():
    print(f"{key}: {value}")
