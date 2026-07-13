# DSA / SDE Round — India, ~1 YOE

Product companies (Amazon, Swiggy, PhonePe, Flipkart, Kotak…) still run **1–2 DSA rounds**
even for AI-adjacent SDE roles. Problems below were reported in real 2024–2026 Indian loops
(LeetCode Discuss, Medium writeups). For each: the pattern to recognize, key insight, and
complexity. Write the code yourself — that's the practice.

## How these rounds are graded at 1 YOE
Communicate before coding: restate the problem, walk an example, state brute force, then
optimize out loud. Interviewers explicitly report grading on **correctness, clarity, and
explaining the thought process before coding** — a silent perfect solution scores worse than
a narrated good one.

---

## A. Arrays & hashing

**1. Two Sum** — hash map of value→index while scanning; O(n)/O(n). The warm-up everywhere.

**2. Top K Frequent Elements** *(asked with follow-up)* — Counter + heap of size k:
O(n log k). Follow-up asked in real loops: *"what if the data doesn't fit in memory?"* →
chunk the stream, partial counts per chunk (hash-partition so equal keys land together),
merge counts, then heap; or count-min sketch for approximate counts.

**3. 4Sum** *(reported in DSA rounds)* — sort + fix two indices + two-pointer inner scan;
O(n³). Dedup by skipping equal neighbors. Generalize the k-sum recursion if asked.

**4. Minimum Swaps to Bring K Together** *(reported)* — count elements ≤ K (window size),
slide the window counting "bad" elements, answer = min bad over all windows; O(n).

**5. Kadane's algorithm (max subarray)** — running best-ending-here vs global best; O(n).
Say the DP interpretation out loud.

## B. Stack / monotonic patterns

**6. Valid Parentheses** *(reported)* — stack of openers, match on close; O(n).

**7. Asteroid Collision** *(reported)* — stack; while top is moving right and current moves
left, resolve collisions; O(n). Careful with equal sizes (both explode).

**8. Online Stock Span** *(reported, solved with monotonic stack)* — stack of (price, span);
pop smaller-or-equal prices accumulating spans. Amortized O(1) per query. Know the
monotonic-stack family: next greater element, daily temperatures, largest rectangle.

**9. LRU Cache** — hash map + doubly linked list for O(1) get/put; in Python mention
`OrderedDict.move_to_end`. A staple for 1–3 YOE.

## C. Dynamic programming

**10. House Robber** *(reported, with space follow-up)* — dp[i] = max(dp[i-1], dp[i-2]+a[i]);
the expected follow-up is optimizing O(n) space → two variables, O(1).

**11. Climbing Stairs / Fibonacci-style** — same recurrence family; recognize it fast.

**12. Coin Change** — unbounded knapsack; dp over amounts, O(amount·coins).

**13. Longest Common Subsequence** — 2-D dp; mention rolling-row space optimization.

## D. Trees & graphs

**14. Build a binary tree from level-order input, then print specific traversals**
*(reported)* — queue-based construction; then BFS/DFS variants (zigzag, right view,
level-order by depth). Practice recursive AND iterative inorder.

**15. Graph BFS/DFS questions** *(Swiggy 2025: graph + arrays rounds)* — islands count,
rotten oranges (multi-source BFS), course schedule (cycle detection/topo sort), clone graph.
BFS for shortest-steps problems, DFS/topo for dependency problems.

**16. Lowest Common Ancestor** — recursive: if root is p/q return it; combine left/right
results.

## E. Strings & sliding window

**17. Longest Substring Without Repeating Characters** — sliding window + last-seen map; O(n).

**18. Group Anagrams** — hash by sorted string or 26-count tuple; O(n·k log k).

**19. String compression / run-length** and **first non-repeating character** — easy but
common screeners at services companies.

---

## F. Machine coding round (the new trend)

Swiggy, PhonePe and similar now replace one talk round with a **90–120 min "build a small
library/service" round** on your own laptop. Reported prompts: parking lot, splitwise,
rate limiter, in-memory key-value store with TTL, snake & ladder, cab booking.

How to pass at 1 YOE:
1. Spend 10 min on requirements + entity design *before* code. Confirm scope out loud.
2. Working > complete: a running happy path with 2 of 5 features beats 5 half-wired ones.
3. Show engineering hygiene: small classes, an interface where extension is obvious
   (e.g. `PricingStrategy`), a couple of unit tests, a README with run instructions.
4. Don't gold-plate: no DB, no framework unless asked — in-memory maps are fine.

## G. What to actually grind (1 YOE budget: ~6 weeks)

- NeetCode 150 or Grokking patterns > random problems. Prioritize: arrays/hashing, two
  pointers, sliding window, stack, BFS/DFS, 1-D DP, heap.
- Redo every problem you fail after 3 days. Track patterns, not counts.
- 2–3 timed mocks (Pramp/peers) — the delta between solving and solving-while-talking is
  the whole game.
