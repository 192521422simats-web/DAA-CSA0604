"""
Assignment 2 - Q3: Brute-force string matching - how text/pattern structure affects work.
Run: python q3_string_matching.py
"""


def brute_force_match(text, pattern):
    n, m = len(text), len(pattern)
    comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i, comps
    return -1, comps


if __name__ == "__main__":
    n, m = 10000, 100
    tests = [
        ("Best case: first pattern char never appears in text",
         "A" * n, "B" + "A" * (m - 1),
         f"about n-m+1 = {n - m + 1} comparisons (one per alignment)"),
        ("Worst case: text of all A, pattern A...AB",
         "A" * n, "A" * (m - 1) + "B",
         f"about m*(n-m+1) = {m * (n - m + 1)} comparisons (almost full pattern at every alignment)"),
        ("Own test: pattern found at the very end of a log-like text",
         ("ERROR login ok " * 700)[:n - 12] + "KERNEL_PANIC", "KERNEL_PANIC",
         "about n comparisons - mostly 1 per alignment, plus 12 at the match"),
    ]
    for title, text, pat, pred in tests:
        pos, c = brute_force_match(text, pat)
        print(f"{title}\n  n={len(text)}, m={len(pat)}")
        print(f"  PREDICTION: {pred}")
        print(f"  RESULT    : match position={pos}, character comparisons={c}\n")
    print("""EXPLANATION
Both bad and good inputs have the same n and m, yet the work differs ~100x. Repeated comparisons occur
when the pattern's prefix matches the text for a long stretch before the final mismatch (many partial
matches). Input size alone (n, m) therefore does not determine running time: the CONTENT of the text and
pattern decides the number of character comparisons. This is why we analyse best, average and worst cases.""")
