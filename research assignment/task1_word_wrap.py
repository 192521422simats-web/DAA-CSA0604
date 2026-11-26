"""
Assignment 4B - Task 1: Word wrap with Dynamic Programming.
Line width M. A non-final line with k unused spaces has penalty k^PENALTY_POWER (the question paper's
formula did not come through in the .doc text - change PENALTY_POWER to 3 if your sheet says k^3).
The final line carries no penalty.

DP definition: best[i] = minimum total penalty for arranging words i..n-1 (word i starts a line).
    best[n] = 0
    best[i] = min over j (i < j <= n, words i..j-1 fit on one line) of
              (0 if j == n else (M - length(i..j-1))^p) + best[j]
Run: python task1_word_wrap.py
"""
PENALTY_POWER = 2


def word_wrap(words, M, show_states=False):
    n = len(words)
    if any(len(w) > M for w in words):
        raise ValueError(f"A word is longer than the line width {M}")
    INF = float("inf")
    best = [INF] * (n + 1)
    nxt = [n] * (n + 1)
    best[n] = 0
    if show_states:
        print(f"  best[{n}] = 0   (no words left)")
    for i in range(n - 1, -1, -1):
        length = -1
        for j in range(i + 1, n + 1):          # line holds words i..j-1
            length += len(words[j - 1]) + 1
            if length > M:
                break
            unused = M - length
            pen = 0 if j == n else unused ** PENALTY_POWER
            if pen + best[j] < best[i]:
                best[i] = pen + best[j]
                nxt[i] = j
            if show_states:
                print(f"    try line words[{i}:{j}] unused={unused} penalty={pen} + best[{j}]={best[j]} "
                      f"= {pen + best[j]}")
        if show_states:
            print(f"  best[{i}] = {best[i]}  (best next line start = word {nxt[i]})")
    lines, i = [], 0
    while i < n:
        j = nxt[i]
        text = " ".join(words[i:j])
        unused = M - len(text)
        pen = 0 if j == n else unused ** PENALTY_POWER
        lines.append((words[i:j], unused, pen))
        i = j
    return best[0], lines


def report(text, M, show_states=False):
    words = text.split()
    print(f"\n=== Width M = {M} ===")
    if not words:
        print("Empty text -> 0 lines, penalty 0")
        return 0
    total, lines = word_wrap(words, M, show_states)
    for idx, (w, unused, pen) in enumerate(lines, 1):
        print(f"Line {idx}: '{' '.join(w)}'  words={len(w)}  unused={unused}  penalty={pen}")
    print(f"Minimum total penalty = {total}")
    assert total == sum(l[2] for l in lines)
    return total


if __name__ == "__main__":
    text = "Dynamic programming solves overlapping subproblems by storing answers to smaller problems"
    print("Baseline run:")
    report(text, 25, show_states=False)
    print("\nIntermediate DP states (width M = 6), small text for readability:")
    small = "aaa bb cc ddddd"
    word_wrap(small.split(), 6, show_states=True)
    print("Meaning: best[i] is the minimum penalty to lay out words i..end; 'try line' rows are the candidate")
    print("first-lines starting at word i; the cheapest candidate (penalty + best[j]) becomes best[i].")

    print("\n--- Requirement change: three more line widths (predictions made before running) ---")
    print("Write your own prediction for each width BEFORE running (arrangement change? where first? penalty up/down?).")
    print("Reference reasoning: fewer words fit per line when M shrinks, so line breaks move; but the penalty does NOT")
    print("simply grow or shrink with M - it depends on how well the word lengths happen to fit the width.")
    print("For very wide lines only a few lines exist, and the final line is free, so only the non-final lines can add penalty.")
    for M in (20, 35, 60):
        report(text, M)

    print("\n--- Boundary tests ---")
    report("abcdef abcdef abcdef", 6)                       # every word exactly fills the line (0 unused)
    report("a", 1)                                          # single word, width 1
    try:
        report("tiny extraordinarily", 5)                   # word longer than width -> must be reported
    except ValueError as e:
        print("Handled error:", e)
    print("Why chosen: words that exactly fill the width test the off-by-one in length (sum + spaces); a word")
    print("longer than the width tests the failure path; a single-word text tests the free-final-line rule.")
