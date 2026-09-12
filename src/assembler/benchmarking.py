import multiprocessing
import time

import psutil


def _run_assembly(assemble_function, args, kwargs, result_queue):
    """Run the assembly function in a separate process."""
    try:
        result = assemble_function(*args, **kwargs)
        result_queue.put(("success", result))
    except Exception as error:
        result_queue.put(("error", repr(error)))


def benchmark_assembly(assemble_function, *args, **kwargs):
    """
    Benchmark an assembly function.

    The assembly runs in a separate process so that its execution time
    and peak resident memory usage can be measured independently.

    Returns
    -------
    result : object
        Return value produced by the assembly function.

    metrics : dict
        Execution time and peak memory statistics.
    """

    result_queue = multiprocessing.Queue()

    process = multiprocessing.Process(
        target=_run_assembly,
        args=(assemble_function, args, kwargs, result_queue),
    )

    start_time = time.perf_counter()
    process.start()

    child = psutil.Process(process.pid)

    peak_memory_bytes = 0

    while process.is_alive():
        try:
            memory = child.memory_info().rss
            peak_memory_bytes = max(peak_memory_bytes, memory)
        except psutil.NoSuchProcess:
            break

        time.sleep(0.01)

    process.join()

    end_time = time.perf_counter()

    # Capture the final RSS value if the process has not disappeared yet.
    try:
        memory = child.memory_info().rss
        peak_memory_bytes = max(peak_memory_bytes, memory)
    except psutil.NoSuchProcess:
        pass

    if process.exitcode != 0 and result_queue.empty():
        raise RuntimeError(
            f"Assembly process exited with code {process.exitcode}."
        )

    try:
        status, result = result_queue.get(timeout=5)
    except Exception as error:
        raise RuntimeError(
            "Assembly process terminated without returning a result."
        ) from error

    if status == "error":
        raise RuntimeError(f"Assembly failed: {result}")

    metrics = {
        "execution_time_seconds": end_time - start_time,
        "peak_memory_bytes": peak_memory_bytes,
        "peak_memory_mb": peak_memory_bytes / (1024 ** 2),
    }

    return result, metrics
