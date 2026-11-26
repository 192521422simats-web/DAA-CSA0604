"""
Assignment 3 - Q4: Conventional vs Strassen matrix multiplication.
Conventional block method: 8 block multiplications of size n/2.   T(n) = 8T(n/2) + O(n^2) = Theta(n^3)
Strassen: 7 block multiplications (M1..M7) + 18 block additions/subtractions.
          T(n) = 7T(n/2) + O(n^2) = Theta(n^log2(7)) ~ n^2.807
  M1=(A11+A22)(B11+B22)  M2=(A21+A22)B11  M3=A11(B12-B22)  M4=A22(B21-B11)
  M5=(A11+A12)B22        M6=(A21-A11)(B11+B12)  M7=(A12-A22)(B21+B22)
  C11=M1+M4-M5+M7  C12=M3+M5  C21=M2+M4  C22=M1-M2+M3+M6
Padding: if n is not a power of 2, the matrices are padded with zeros up to the next power of 2 and the
result is cropped back (extra cost: up to ~8x more work in the worst case).
Run: python q4_strassen.py
"""
import random
import time

STATS = {"mults": 0, "adds": 0}


def add(A, B):
    n = len(A); STATS["adds"] += n * n
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub(A, B):
    n = len(A); STATS["adds"] += n * n
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def conventional(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    STATS["mults"] += n ** 3
    STATS["adds"] += n ** 2 * (n - 1)
    return C


def split(M):
    h = len(M) // 2
    return ([r[:h] for r in M[:h]], [r[h:] for r in M[:h]],
            [r[:h] for r in M[h:]], [r[h:] for r in M[h:]])


def join(C11, C12, C21, C22):
    return [a + b for a, b in zip(C11, C12)] + [a + b for a, b in zip(C21, C22)]


def strassen(A, B, cutoff=1):
    n = len(A)
    if n <= cutoff:
        if n == 1:
            STATS["mults"] += 1
            return [[A[0][0] * B[0][0]]]
        return conventional(A, B)
    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)
    M1 = strassen(add(A11, A22), add(B11, B22), cutoff)
    M2 = strassen(add(A21, A22), B11, cutoff)
    M3 = strassen(A11, sub(B12, B22), cutoff)
    M4 = strassen(A22, sub(B21, B11), cutoff)
    M5 = strassen(add(A11, A12), B22, cutoff)
    M6 = strassen(sub(A21, A11), add(B11, B12), cutoff)
    M7 = strassen(sub(A12, A22), add(B21, B22), cutoff)
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(sub(add(M1, M3), M2), M6)
    return join(C11, C12, C21, C22)


def pad(M, size):
    n = len(M)
    return [row + [0] * (size - n) for row in M] + [[0] * size for _ in range(size - n)]


def strassen_any(A, B, cutoff=1):
    n = len(A)
    size = 1
    while size < n:
        size *= 2
    if size == n:
        return strassen(A, B, cutoff)
    C = strassen(pad(A, size), pad(B, size), cutoff)
    return [row[:n] for row in C[:n]]


def rand_matrix(n):
    return [[random.randint(-9, 9) for _ in range(n)] for _ in range(n)]


def timed(fn, *args):
    STATS["mults"] = STATS["adds"] = 0
    t0 = time.perf_counter()
    r = fn(*args)
    return r, time.perf_counter() - t0, STATS["mults"], STATS["adds"]


if __name__ == "__main__":
    random.seed(9)
    print("Correctness: 2x2 example and a 5x5 (needs padding)")
    A = [[1, 2], [3, 4]]; B = [[5, 6], [7, 8]]
    print("  Strassen 2x2 :", strassen(A, B), " conventional:", conventional(A, B))
    A5, B5 = rand_matrix(5), rand_matrix(5)
    assert strassen_any(A5, B5) == conventional(A5, B5)
    print("  5x5 padded Strassen == conventional: True\n")

    print(f"{'n':>4} | {'conv mults':>11} {'conv adds':>10} {'conv ms':>9} | {'str mults':>10} {'str adds':>10} {'str ms':>9} | faster")
    for n in (2, 4, 8, 16, 32, 64, 128):
        A, B = rand_matrix(n), rand_matrix(n)
        c, tc, mc, ac = timed(conventional, A, B)
        s, ts, ms, as_ = timed(strassen, A, B)
        assert c == s
        print(f"{n:>4} | {mc:>11} {ac:>10} {tc * 1000:>9.2f} | {ms:>10} {as_:>10} {ts * 1000:>9.2f} | "
              f"{'Strassen' if ts < tc else 'Conventional'}")
    print("\nStrassen with a cutoff (switch to conventional multiplication for blocks of size <= 32)")
    for n in (64, 128, 256):
        A, B = rand_matrix(n), rand_matrix(n)
        c, tc, mc, ac = timed(conventional, A, B)
        s, ts, ms, as_ = timed(strassen, A, B, 32)
        assert c == s
        print(f"  n={n:>4}: conventional {tc * 1000:>8.1f} ms / {mc} mults | Strassen(cutoff 32) {ts * 1000:>8.1f} ms / {ms} mults")
    print("\nEffect of padding: n=65 is padded to 128")
    A, B = rand_matrix(65), rand_matrix(65)
    _, t65, m65, _ = timed(strassen_any, A, B)
    print(f"  Strassen on 65x65 -> {m65} mults, {t65 * 1000:.1f} ms  (same cost as a 128x128 matrix)")
    print("""
Strassen needs fewer multiplications (7^k vs 8^k, e.g. 823,543 vs 2,097,152 at n=128) but many more
additions/subtractions, matrix copies and recursion calls, plus extra memory for temporaries and padding.
In the pure recursion-to-size-1 version, conventional multiplication was faster for every size tested; using a
cutoff (see second table) Strassen only reaches roughly break-even at n of about 128-256 in this Python prototype. In optimised libraries the cache-friendly
conventional method typically wins until n is in the hundreds or thousands.
JOINT DECISION: use conventional multiplication for small or non-power-of-2 matrices, memory-limited or
numerically sensitive work (Strassen is slightly less stable); use Strassen (with a cutoff to the
conventional method) only for very large matrices.""")
