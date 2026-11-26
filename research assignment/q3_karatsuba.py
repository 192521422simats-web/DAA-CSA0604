"""
Assignment 3 - Q3: Karatsuba vs standard multiplication.
Numbers are handled as lists of decimal digits so that 'multiplication count' = single-digit multiplications.
Standard (school) multiplication: n^2 digit multiplications.
Karatsuba: x = a*10^m + b, y = c*10^m + d.  xy = ac*10^(2m) + ((a+b)(c+d)-ac-bd)*10^m + bd
           3 recursive multiplications instead of 4:  T(n) = 3T(n/2) + O(n)  ->  Theta(n^log2(3)) ~ n^1.585
Run: python q3_karatsuba.py
"""
import random
import time


def school_multiply(x, y, cnt):
    xs, ys = str(x)[::-1], str(y)[::-1]
    res = [0] * (len(xs) + len(ys) + 1)
    for i, a in enumerate(xs):
        carry = 0
        for j, b in enumerate(ys):
            cnt[0] += 1
            cur = res[i + j] + int(a) * int(b) + carry
            res[i + j] = cur % 10
            carry = cur // 10
        res[i + len(ys)] += carry
    return int("".join(map(str, res[::-1])))


def karatsuba(x, y, cnt, cutoff=1):
    """cutoff = number of digits at/below which standard multiplication is used."""
    nx, ny = len(str(x)), len(str(y))
    n = max(nx, ny)
    if n <= cutoff or x < 10 or y < 10:
        if n <= 1 or x < 10 or y < 10:
            cnt[0] += max(nx, ny) if (x < 10 or y < 10) else 1
            return x * y
        return school_multiply(x, y, cnt)
    m = n // 2
    p = 10 ** m
    a, b = divmod(x, p)
    c, d = divmod(y, p)
    ac = karatsuba(a, c, cnt, cutoff)
    bd = karatsuba(b, d, cnt, cutoff)
    abcd = karatsuba(a + b, c + d, cnt, cutoff)
    return ac * p * p + (abcd - ac - bd) * p + bd


def rand_digits(n):
    return random.randint(10 ** (n - 1), 10 ** n - 1)


if __name__ == "__main__":
    random.seed(8)
    x, y = 1234, 5678
    c1, c2 = [0], [0]
    assert school_multiply(x, y, c1) == karatsuba(x, y, c2) == x * y
    print("Check: 1234 x 5678 =", x * y, "OK\n")
    print(f"{'digits':>7} {'school mults':>13} {'karatsuba mults':>16} {'school time(ms)':>16} {'karat time(ms)':>15} {'faster'}")
    REPEAT = 3
    for n in (4, 8, 16, 32, 64, 128, 256, 512, 1024):
        x, y = rand_digits(n), rand_digits(n)
        cs, ck = [0], [0]
        ts = tk = 0.0
        for _ in range(REPEAT):
            cs[0] = ck[0] = 0
            t0 = time.perf_counter(); r1 = school_multiply(x, y, cs); ts += time.perf_counter() - t0
            t0 = time.perf_counter(); r2 = karatsuba(x, y, ck); tk += time.perf_counter() - t0
        assert r1 == r2 == x * y
        faster = "Karatsuba" if tk < ts else "School"
        print(f"{n:>7} {cs[0]:>13} {ck[0]:>16} {ts / REPEAT * 1000:>16.3f} {tk / REPEAT * 1000:>15.3f} {faster}")
    print("""
Counts: Karatsuba needs far fewer digit multiplications as n grows (n^1.585 vs n^2). The crossover in TIME
appears where the saved multiplications outweigh the extra additions, subtractions, divmod/splitting and
recursion-call overhead (see the 'faster' column for the approximate range in this Python implementation).
Better asymptotic complexity does not guarantee a faster program at every size: constants and overheads
dominate for small inputs. Practical libraries switch to the standard method below a cutoff size.""")
