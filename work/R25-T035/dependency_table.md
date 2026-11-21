# R25-T035 — Dependency Audit & Precondition Table

Target: `get_likes_on_FB.py` — `get_likes_on_FB`

---

## 1. Source Preconditions & Citations

| Line | Code | Contract / Precondition |
|:---|:---|:---|
| Line 7 | `accessToken = "TOKENVALUE"` | Default Facebook Graph API access token. |
| Line 8 | `userId = sys.argv[1]` | Precondition: user ID required as string. |
| Line 9 | `limit = 100` | Precondition: post query limit integer. |
| Lines 11-18 | `url = "https://graph.facebook.com/" + userId + "/posts?access_token=" + accessToken + "&limit=" + str(limit)` | Precondition: URL string construction. |
| Line 19 | `data = json.load(urllib.urlopen(url))` | Network dependency: `urlopen` must return a readable byte stream; `json.load` decodes it into a dictionary. |
| Line 20 | `id = 0` | State: counter initialized to 0. |
| Line 22 | `print(str(id))` | Output: prints initial `"0"`. |
| Line 24 | `for item in data["data"]:` | Precondition: `data` must contain `"data"` key holding a list of post dictionaries. |
| Line 25 | `time = item["created_time"][11:19]` | Precondition: `created_time` must contain time at indices [11:19] (e.g., `"HH:MM:SS"`). |
| Line 26 | `date = item["created_time"][5:10]` | Precondition: `created_time` must contain date at indices [5:10] (e.g., `"MM-DD"`). |
| Line 27 | `year = item["created_time"][0:4]` | Precondition: `created_time` must contain year at indices [0:4] (e.g., `"YYYY"`). |
| Lines 29-32 | `if "shares" in item: num_share = item["shares"]["count"] else: 0` | Precondition: `"shares"` optional; if present, contains `"count"`. Defaults to 0. |
| Lines 33-36 | `if "likes" in item: num_like = item["likes"]["count"] else: 0` | Precondition: `"likes"` optional; if present, contains `"count"`. Defaults to 0. |
| Line 37 | `id += 1` | State: post ID incremented. |
| Lines 38-48 | `print(str(id) + "\t" + time + "\t" + date + "\t" + year + "\t" + str(num_share) + "\t" + str(num_like))` | Output: prints tab-separated row string. |

---

## 2. Dependency Audit & Seam Design

| Observable Dependency | Original Usage | Introduced Seam / Control |
|:---|:---|:---|
| **CLI Arguments (`sys.argv`)** | `userId = sys.argv[1]` executed on import | Moved under `if __name__ == "__main__":`; `userId` passed as function argument. |
| **Network (`urllib.urlopen`)** | Direct call to live Facebook Graph API | Dependency injection parameter `opener=None`. Defaults to standard `urlopen` for existing callers; tests inject mock response. |
| **Console (`print`)** | Hardcoded stdout prints | Preserved; function also returns structured records for programmatic verification. |
| **Mutable State** | None | Pure function once network response is received. Zero global variable leakage. |

---

## 3. Fixture Matrix

| Scenario | Input `userId` | Input Payload `data` | Precondition Citations | Expected Formatted Row |
|:---|:---|:---|:---|:---|
| **Smallest Valid Input** | `"4"` | `{"data": [{"created_time": "2026-01-01T00:00:00"}]}` | Lines 8, 19, 24, 25-27, 32, 36, 37 | `"1\t00:00:00\t01-01\t2026\t0\t0"` |
| **Ordinary Input** | `"4"` | `{"data": [{"created_time": "2026-11-21T15:30:45", "shares": {"count": 25}, "likes": {"count": 150}}]}` | Lines 8, 19, 24, 25-27, 30, 34, 37 | `"1\t15:30:45\t11-21\t2026\t25\t150"` |
| **Multi-Item Input** | `"4"` | Two post items | Lines 24, 37, 38-48 | Rows with `id=1` and `id=2` |

---

## 4. Repeatability & Isolation Verification

- **Repeatability Test**: Fixture executed twice in fresh isolated state -> identical results.
- **Input Isolation Test**: Fixture A executed -> Fixture B executed -> Fixture A executed again -> result identical to initial run. Earlier runs cannot alter subsequent runs.
