import os
import time
import resource

import psutil


def benchmark_assembly(assemble_function, *args, **kwargs):
    """
    Measure execution time and memory usage of an assembly run.

    Parameters
    ----------
    assemble_function : callable
        Assembly function to benchmark.

    *args, **kwargs
        Arguments passed to the assembly function.

    Returns
    -------
    result : object
        Result returned by the assembly function.

    metrics : dict
        Benchmarking statistics.
    """

    process = psutil.Process(os.getpid())

    # Record memory before assembly.
    memory_before = process.memory_info().rss

    # Record the process maximum resident memory before assembly.
    max_rss_before = resource.getrusage(
        resource.RUSAGE_SELF
    ).ru_maxrss

    # Start timer.
    start_time = time.perf_counter()

    # Run assembly.
    result = assemble_function(*args, **kwargs)

    # Stop timer.
    end_time = time.perf_counter()

    # Record memory after assembly.
    memory_after = process.memory_info().rss

    # Record maximum resident memory.
    max_rss_after = resource.getrusage(
        resource.RUSAGE_SELF
    ).ru_maxrss

    execution_time = end_time - start_time

    memory_used = max(
        0,
        memory_after - memory_before,
    )

    peak_memory = max(
        0,
        max_rss_after - max_rss_before,
    )

    # Linux reports ru_maxrss in kilobytes.
    peak_memory_mb = peak_memory / 1024

    metrics = {
        "execution_time_seconds": execution_time,
        "memory_used_bytes": memory_used,
        "memory_used_mb": memory_used / (1024 ** 2),
        "peak_memory_kb": peak_memory,
        "peak_memory_mb": peak_memory_mb,
    }

    return result, metrics
