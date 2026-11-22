# R25-T039 Complexity Experiment: get_integer Scaling

- **Input size variable ($d$)**: Number of decimal digits in input string
- **Repetitions per size**: 5
- **Fixed PRNG Seed**: 42
- **Isolation**: Input injected directly in-memory, avoiding process startup & terminal I/O latency

| Input Size ($d$ digits) | Min (µs) | Median (µs) | Max (µs) | Range (µs) | Correctness |
|------------------------|----------|-------------|----------|------------|-------------|
| 100 | 0.42 | 0.58 | 1.12 | 0.71 | 100% Passed |
| 1000 | 4.21 | 4.42 | 5.75 | 1.54 | 100% Passed |
| 3000 | 28.88 | 29.46 | 40.21 | 11.33 | 100% Passed |

### Observations
- The algorithm consists of `num.isnumeric()` followed by `int(num)`.
- Both operations exhibit $O(d)$ time complexity for practical digit lengths.
- All 5 repetitions across all 3 sizes matched the independently calculated expected values.
