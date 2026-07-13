# Python + ML-Basics Coding Round — India, ~1 YOE

Indian GenAI L1 rounds mix **easy Python programs** (yes, really — even/odd and primes were
asked at Capgemini for a GenAI role), **Python language questions**, **pandas**, and **basic
classical ML**. Don't skip the easy stuff; fumbling it is an instant red flag.

---

## A. Warm-up programs (asked verbatim in real loops)

**1. Print even and odd numbers from a list.** *(Capgemini)*
```python
nums = [1, 2, 3, 4, 5, 6]
evens = [n for n in nums if n % 2 == 0]
odds  = [n for n in nums if n % 2 != 0]
```

**2. Print prime numbers between 0 and 100.** *(Capgemini)*
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

primes = [n for n in range(101) if is_prime(n)]
```
Mention the √n optimization unprompted; for many queries, mention Sieve of Eratosthenes (O(n log log n)).

**3. Check whether two strings are anagrams.** *(Capgemini, Infosys)*
```python
from collections import Counter
def is_anagram(a, b):
    return Counter(a) == Counter(b)   # O(n); sorted(a) == sorted(b) is O(n log n)
```

**4. Reverse a string / check palindrome.**
```python
s[::-1]                      # reverse
s == s[::-1]                 # palindrome
```
Follow-up they like: do it without slicing (two pointers).

**5. Remove duplicates from a list, preserving order.**
```python
list(dict.fromkeys(items))   # dicts preserve insertion order (3.7+)
```

**6. Fibonacci (iterative + memoized).**
```python
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```
Say why naive recursion is O(2^n) and how `functools.lru_cache` fixes it.

**7. Word frequency in a sentence / find the second largest number / FizzBuzz** — all still
appear. Practice writing them without a syntax stumble.

---

## B. Python language questions

**8. List vs tuple?**
List: mutable, slightly more memory. Tuple: immutable, hashable (usable as dict key/set
member), signals fixed structure. Immutability = safety + dict-key eligibility.

**9. Shallow vs deep copy?**
`copy.copy` copies the outer container only — nested objects are shared; `copy.deepcopy`
recursively copies everything. Classic bug: mutating a nested list through a shallow copy.

**10. What are generators? Why use them?**
Functions with `yield` producing values lazily one at a time. Constant memory for large
streams (read a 10 GB file line by line), and they compose into pipelines. `(x*x for x in
nums)` is a generator expression; iterating exhausts it.

**11. Explain decorators with an example.**
A function that wraps another to add behavior without changing it:
```python
import functools, time
def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.time() - t0:.2f}s")
        return result
    return wrapper
```
Real uses: logging, retries, auth checks, caching (`lru_cache`).

**12. What is the GIL?**
A mutex letting only one thread execute Python bytecode at a time per process. Threads are
fine for I/O-bound work (network calls release the GIL); use `multiprocessing` for CPU-bound
work. Bonus: mention Python 3.13's experimental free-threaded build if asked what's changing.

**13. `*args` / `**kwargs`? Mutable default argument bug?**
`*args` collects positional, `**kwargs` keyword arguments. The classic bug:
`def f(x, acc=[])` — the list is created once at definition time and shared across calls;
use `acc=None` + `acc = acc or []`.

**14. How does Python manage memory?**
Reference counting frees objects at zero refs, plus a cyclic garbage collector for reference
cycles. Objects live on a private heap; small-int and string interning exist — explains the
`is` vs `==` gotcha.

**15. `is` vs `==`?**
`==` compares values, `is` compares identity (same object). Use `is` only for `None`/
sentinels.

**16. Exception handling best practice?**
Catch specific exceptions, keep `try` blocks small, use `finally`/context managers for
cleanup, raise with context (`raise X from e`). Catching bare `Exception` and passing
silently is the anti-pattern they want you to call out.

**17. What is `async`/`await`? When does it help an LLM app?**
Cooperative concurrency on one thread via an event loop — ideal for I/O-bound workloads like
concurrent LLM/API calls (`asyncio.gather` to fan out embedding or completion requests).
Doesn't speed up CPU-bound code.

**18. How do you call an external API properly in Python?**
`requests`/`httpx` with: timeouts (always), retries with exponential backoff + jitter on
429/5xx, session reuse, and error handling on status + parse. For LLM APIs add: token/cost
logging and streaming handling.

---

## C. pandas / data handling (asked when the role touches data)

**19. `merge` vs `join` vs `concat`?**
`merge`: SQL-style joins on columns (how=inner/left/outer). `join`: convenience merge on
index. `concat`: stack DataFrames along an axis. Know `how=` semantics cold.

**20. How do you handle missing values?**
Inspect first (`df.isna().sum()`), then per column: drop (if few/random), impute
(mean/median/mode or domain default), or flag with an indicator column. Never blind-fill;
say the choice depends on *why* data is missing.

**21. `groupby` example.**
```python
df.groupby("city")["amount"].agg(["sum", "mean", "count"])
```
Follow-ups: `transform` (broadcast back to original shape) vs `agg` (reduce).

**22. Remove duplicate rows from a table / DataFrame.** *(Capgemini L2)*
`df.drop_duplicates(subset=["col1", "col2"], keep="first")`. In SQL:
`ROW_NUMBER() OVER (PARTITION BY col1 ORDER BY updated_at DESC)` then keep rn=1 — they
asked exactly this pattern (see also SCD below).

**23. What are Slowly Changing Dimensions (SCD)?** *(Capgemini L2 — data-flavored GenAI roles)*
How warehouses track changing attributes. Type 1: overwrite (no history). Type 2: add a new
row with validity dates/current flag (full history). Type 3: extra column for previous
value. Type 2 is the default answer for "we need history".

---

## D. Classical ML basics (still on every Indian checklist)

**24. Precision vs recall? When do you optimize which?**
Precision = TP/(TP+FP): of what I flagged, how much was right. Recall = TP/(TP+FN): of what
existed, how much I caught. Fraud/cancer screening → recall (missing is costly); spam
filter → precision (false alarms are costly). F1 balances both.

**25. What is an imbalanced dataset and how do you deal with it?** *(Capgemini)*
Class ratios are skewed (e.g. 1% fraud) so accuracy is misleading. Fixes: better metrics
(precision/recall, PR-AUC, F1), resampling (undersample majority / oversample minority /
SMOTE), class weights in the loss, threshold tuning, and collecting more minority data.

**26. Linear vs logistic regression?**
Linear predicts continuous values by fitting a line minimizing squared error. Logistic
passes the linear output through a sigmoid to model class probability, trained with
log-loss — classification, not regression, despite the name.

**27. Overfitting — detection and fixes?**
Train metric ≫ validation metric. Fixes: more data, regularization (L1/L2, dropout),
simpler model, early stopping, cross-validation for honest estimates. For LLM fine-tuning:
fewer epochs, LoRA rank down, held-out eval set.

**28. What is gradient descent (intuition)?**
Iteratively step weights in the direction that most reduces loss (negative gradient), step
size = learning rate. Variants: batch/mini-batch/SGD; Adam adds momentum + per-parameter
learning rates and is the default.

**29. Bias–variance trade-off?**
Bias: error from oversimplified assumptions (underfit). Variance: error from sensitivity to
training noise (overfit). Total error is minimized between the extremes; regularization and
data size move the balance.

**30. Train/validation/test split — why three?**
Train fits weights; validation tunes hyperparameters (and gets indirectly overfit through
your choices); test is touched once for the final honest number. Leaking test into decisions
invalidates it — say "data leakage" out loud, interviewers love it.
