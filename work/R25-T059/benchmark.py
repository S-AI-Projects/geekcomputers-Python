import builtins
import importlib.util
import itertools
import statistics
import time
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[2] / "Type_of_angles_of_triangle.py"


def load_module():
    original_input = builtins.input
    original_print = builtins.print

    try:
        builtins.input = lambda prompt="": "60"
        builtins.print = lambda *args, **kwargs: None

        spec = importlib.util.spec_from_file_location("angle_benchmark", SOURCE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        builtins.input = original_input
        builtins.print = original_print


def run_batch(function, count):
    # Prepare mocked I/O before timing. Each call receives three fresh values.
    values = itertools.cycle(("60", "60", "60"))
    original_input = builtins.input
    original_print = builtins.print

    try:
        builtins.input = lambda prompt="": next(values)
        builtins.print = lambda *args, **kwargs: None

        start = time.perf_counter_ns()
        for _ in range(count):
            result = function()
            assert result is None
        elapsed = time.perf_counter_ns() - start
        return elapsed / count
    finally:
        builtins.input = original_input
        builtins.print = original_print


def run_benchmark():
    module = load_module()
    function = module.angle_type

    # Correctness check before collecting timings.
    assert run_batch(function, 1) > 0

    sizes = (100, 500, 1000)
    repetitions = 5

    print("Benchmark: angle_type()")
    print("Input per call: (60, 60, 60)")
    print("Calls per batch:", sizes)
    print("Repetitions per size:", repetitions)
    print("Import, startup, and real terminal I/O are excluded.")
    print("Mocked input/print function-call overhead remains included.")
    print()

    for size in sizes:
        durations = [run_batch(function, size) for _ in range(repetitions)]

        median = statistics.median(durations)
        minimum = min(durations)
        maximum = max(durations)

        print(
            f"{size} calls: median={median:.1f} ns/call, "
            f"range={minimum:.1f}–{maximum:.1f} ns/call"
        )


if __name__ == "__main__":
    run_benchmark()
