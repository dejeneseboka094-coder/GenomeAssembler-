from src.assembler.benchmarking import benchmark_assembly


def test_benchmark_assembly():
    def dummy_assembly():
        return ["ATGC", "CGTA"]

    result, metrics = benchmark_assembly(dummy_assembly)

    assert result == ["ATGC", "CGTA"]

    assert "execution_time_seconds" in metrics
    assert "peak_memory_bytes" in metrics
    assert "peak_memory_mb" in metrics

    assert metrics["execution_time_seconds"] >= 0
    assert metrics["peak_memory_bytes"] > 0
    assert metrics["peak_memory_mb"] > 0
