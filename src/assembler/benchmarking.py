import os
import time

import psutil


def benchmark_assembly(assemble_function, *args, **kwargs):
    """
    Measure execution time and peak memory usage of an assembly run.

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

    # Record memory immediately before assembly.
    memory_before = process.memory_info().rss

    # Start execution timer.
    start_time = time.perf_counter()

    # Run the assembly.
    result = assemble_function(*args, **kwargs)

    # Stop execution timer.
    end_time = time.perf_counter()

    # Record memory immediately after assembly.
    memory_after = process.memory_info().rss

    execution_time = end_time - start_time

    memory_used = max(
        0,
        memory_after - memory_before,
    )

    metrics = {
        "execution_time_seconds": execution_time,
        "memory_used_bytes": memory_used,
        "memory_used_mb": memory_used / (1024 ** 2),
    }

    return result, metrics
