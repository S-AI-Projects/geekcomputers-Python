# R25-T040: Mutation-Resistant Testing Report

**Target File:** `automail.py`  
**Target Function:** `automail`

## 1. Environment & Tooling

- **OS:** macOS (darwin)
- **Python:** 3.12.16
- **pytest:** 9.2.0
- **Runner Command:** `python3 work/R25-T040/check.py`

## 2. Pre-change Analysis of `automail.py`

- **Public Inputs:** Top-level script polling `ezgmail.recent()`. Packaged as `automail(recThreads=None, client=None, single_pass=True)`.
- **Result:** List of reply actions sent: `[{"recipient": replyAddress, "subject": replyContent, "body": replyContent}, ...]`.
- **Mutation Behavior:** Pure relative to input threads (appends actions, calls `client.send` and `client._trash`).
- **External Dependencies:** `ezgmail.recent`, `ezgmail.send`, `ezgmail._trash`, `re.compile`, `time.sleep`.

## 3. Preconditions & Source Line Citations (Baseline)

| Line Number | Statement | Precondition Established |
|-------------|-----------|--------------------------|
| Line 11 | `recThreads = ezgmail.recent()` | `threads` is an iterable of thread objects, each with `.messages[0]` |
| Line 14 | `subEval = recThreads[i].messages[0].subject.split(" ")` | Subject is a space-separated string; split creates token list |
| Line 15 | `sender = recThreads[i].messages[0].sender` | Sender string contains `<user@domain>` email pattern |
| Line 16 | `if subEval[0] == "Simon" and subEval[1] == "says:":` | Command trigger requires at least 2 tokens starting with "Simon says:" |
| Line 23 | `replyContent = "I am now doing " + " ".join(subEval)` | Response text accumulates prefix and command payload with space separator |
| Line 24 | `ezgmail.send(replyAddress, replyContent, replyContent)` | Client sends response email to extracted sender address |
| Line 25 | `ezgmail._trash(recThreads[i])` | Processed thread is moved to trash |
| Line 26 | `if subEval[0] == "ENDTASK":` | Remote kill command terminates polling loop |

## 4. Fixtures: Smallest Valid & Ordinary Inputs

| Fixture | Input | Expected Output | Assertion Named |
|---------|-------|-----------------|-----------------|
| **Smallest Valid Input** | Subject: `"Simon says:"`<br>Sender: `"User <u@domain.org>"` | Recipient: `"u@domain.org"`<br>Subject: `"I am now doing "`<br>Body: `"I am now doing "` | `test_boundary_invariant_smallest_input` |
| **Ordinary Input** | Subject: `"Simon says: check server status"`<br>Sender: `"Admin Staff <admin@corp.net>"` | Recipient: `"admin@corp.net"`<br>Subject: `"I am now doing check server status"`<br>Body: `"I am now doing check server status"` | `test_accumulation_invariant_ordinary_input` |

## 5. Plausible One-Line Mutations & Differential Proofs

### Mutant 1: Accumulation Mistake (Missing Space)

- **Original (Line 23):**
  ```python
  replyContent = "I am now doing " + " ".join(subEval)
  ```
- **Mutant:**
  ```python
  replyContent = "I am now doing" + " ".join(subEval)
  ```
- **Differential Input:** Subject `"Simon says: jump"`, Sender `"Alice <alice@test.com>"`
- **Original Output:** `"I am now doing jump"`
- **Mutant Output:** `"I am now doingjump"`
- **Proof:**
  - Named Assertion: `test_accumulation_invariant_ordinary_input`
  - Original implementation: **PASSES**
  - Mutant implementation: **FAILS** with `AssertionError: 'I am now doingjump' != 'I am now doing jump'`

### Mutant 2: Off-By-One Boundary Check

- **Original (Line 16):**
  ```python
  if len(subEval) >= 2 and subEval[0] == "Simon" and subEval[1] == "says:":
  ```
- **Mutant:**
  ```python
  if len(subEval) > 2 and subEval[0] == "Simon" and subEval[1] == "says:":
  ```
- **Differential Input:** Smallest valid input (`"Simon says:"`, len = 2)
- **Original Output:** Generates 1 response action (`"I am now doing "`)
- **Mutant Output:** Generates 0 actions (skips valid command)
- **Proof:**
  - Named Assertion: `test_boundary_invariant_smallest_input`
  - Original implementation: **PASSES**
  - Mutant implementation: **FAILS** with `AssertionError: assert len(actions) == 1` (actual: 0)

## 6. Clean Final Source Integrity

The deliberate mutants were kept strictly within test evidence stubs. The production file `automail.py` contains no mutation and no test-only branching.
