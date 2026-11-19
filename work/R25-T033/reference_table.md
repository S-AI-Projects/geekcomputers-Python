# R25-T033 — get_players Cross-Check Reference Table

Source: `RandomNumberGame.py` — `get_players` (line 28)

## Source Contract (line 46)

```python
def get_players(n: int) -> List[str]:
    return [input("Enter name of player: ") for _ in range(n)]
```

- **Input**: `n` (int) — number of players
- **Return**: `List[str]` — exactly `n` strings from sequential `input()` calls
- **Mutation**: None (pure aside from I/O)
- **Ordering**: Preserved — list comprehension iterates `range(n)` sequentially
- **External dependency**: `builtins.input`

## Independent Oracle

The oracle constructs the expected result as `names[:n]` — taking the first
`n` items from the input sequence, in order. This matches the contract without
calling `get_players`.

```python
def oracle_get_players(names_sequence, n):
    return list(names_sequence[:n])
```

## Cross-Check Input/Expected Table (25 cases)

| # | n | Input Names | Oracle Expected | Source Citation |
|---|---|-------------|-----------------|-----------------|
| 1 | 0 | `[]` | `[]` | Line 46: `range(0)` → empty |
| 2 | 1 | `["Alice"]` | `["Alice"]` | Line 46: `range(1)` → 1 call |
| 3 | 1 | `["Bob"]` | `["Bob"]` | Line 46: `range(1)` → 1 call |
| 4 | 1 | `[""]` | `[""]` | Line 46: input() returns "" |
| 5 | 1 | `["X"]` | `["X"]` | Line 46: `range(1)` → 1 call |
| 6 | 1 | `["Player 1"]` | `["Player 1"]` | Line 46: `range(1)` → 1 call |
| 7 | 2 | `["Alice", "Bob"]` | `["Alice", "Bob"]` | Line 46: `range(2)` → 2 calls |
| 8 | 2 | `["Zoe", "Amy"]` | `["Zoe", "Amy"]` | Line 46: `range(2)` → 2 calls |
| 9 | 2 | `["", ""]` | `["", ""]` | Line 46: empty strings valid |
| 10 | 2 | `["player-one", "player-two"]` | `["player-one", "player-two"]` | Line 46: `range(2)` → 2 calls |
| 11 | 3 | `["A", "B", "C"]` | `["A", "B", "C"]` | Line 46: `range(3)` → 3 calls |
| 12 | 3 | `["Alice", "Bob", "Charlie"]` | `["Alice", "Bob", "Charlie"]` | Line 46: `range(3)` → 3 calls |
| 13 | 3 | `["foo", "bar", "baz"]` | `["foo", "bar", "baz"]` | Line 46: `range(3)` → 3 calls |
| 14 | 4 | `["P1", "P2", "P3", "P4"]` | `["P1", "P2", "P3", "P4"]` | Line 46: `range(4)` → 4 calls |
| 15 | 5 | `["a", "b", "c", "d", "e"]` | `["a", "b", "c", "d", "e"]` | Line 46: `range(5)` → 5 calls |
| 16 | 1 | `["  spaces  "]` | `["  spaces  "]` | Line 46: no trimming |
| 17 | 1 | `["123"]` | `["123"]` | Line 46: input() returns str |
| 18 | 1 | `["name_with_underscore"]` | `["name_with_underscore"]` | Line 46: any string valid |
| 19 | 1 | `["CamelCase"]` | `["CamelCase"]` | Line 46: case preserved |
| 20 | 2 | `["UPPER", "lower"]` | `["UPPER", "lower"]` | Line 46: case preserved |
| 21 | 3 | `["Same", "Same", "Same"]` | `["Same", "Same", "Same"]` | Line 46: no dedup |
| 22 | 1 | `["日本語"]` | `["日本語"]` | Line 46: Unicode valid |
| 23 | 2 | `["Ñoño", "Ürgen"]` | `["Ñoño", "Ürgen"]` | Line 46: Unicode valid |
| 24 | 6 | `["p1"..."p6"]` | `["p1"..."p6"]` | Line 46: `range(6)` → 6 calls |
| 25 | 7 | `["a"..."g"]` | `["a"..."g"]` | Line 46: `range(7)` → 7 calls |

## Reproducibility

Repeated runs with fresh equivalent inputs produce identical results because
`get_players` uses a deterministic list comprehension with no randomness
(unlike `play_turn` which uses `random.randint`).

