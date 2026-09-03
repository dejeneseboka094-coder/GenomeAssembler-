import multiprocessing
import os
import time

import psutil


def _run_assembly(assemble_function, args, kwargs, result_queue):
    """Run assembly in a separate process."""
    try:
        result = assemble_function(*args, **kwargs)
        result_queue.put(("success", result))
    except Exception as error:
        result_queue.put(("error", repr(error)))


def benchmark_assembly(assemble_function, *args, **kwargs):
    """
    Measure execution time and peak memory usage of an assembly run.

    The assembly is executed in a separate process so that its
    memory usage can be measured independently.
    """

    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_run_assembly,
        args=(
            assemble_function,
            args,
            kwargs,
            result_queue,
        ),
    )

    start_time = time.perf_counter()

    process.start()

    child = psutil.Process(process.pid)

    peak_memory_bytes = 0

    while process.is_alive():
        try:
            memory = child.memory_info().rss
            peak_memory_bytes = max(
                peak_memory_bytes,
                memory,
            )
        except psutil.NoSuchProcess:
            break

    process.join()

    end_time = time.perf_counter()

    # Capture final memory reading as well.
    try:
        memory = child.memory_info().rss
        peak_memory_bytes = max(
            peak_memory_bytes,
            memory,
        )
    except psutil.NoSuchProcess:
        pass

    if not result_queue.empty():
        status, result = result_queue.get()

        if status == "error":
            raise RuntimeError(
                f"Assembly failed: {result}"
            )
    else:
        raise RuntimeError(
            "Assembly process terminated without returning a result."
        )

    execution_time = end_time - start_time

    metrics = {
        "execution_time_seconds": execution_time,
        "peak_memory_bytes": peak_memory_bytes,
        "peak_memory_mb": peak_memory_bytes / (1024 ** 2),
    }

    return result, metrics
