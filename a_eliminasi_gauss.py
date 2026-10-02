#!/usr/bin/env python3

import argparse
from fractions import Fraction as F

DEFAULT_A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
DEFAULT_B = [3, 9, 4]


# ----------------------------- Utilitas tampilan -----------------------------
def fmt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def show_aug(A, b, title=""):
    if title:
        print(f"\n{title}")
    w = max(len(fmt(x)) for row in A for x in row + [0]) + 1
    wb = max(len(fmt(x)) for x in b) + 1
    for row, bi in zip(A, b):
        print("  [ " + " ".join(fmt(x).rjust(w) for x in row) + " | " + fmt(bi).rjust(wb) + " ]")


def to_frac(A, b):
    return [[F(x) for x in r] for r in A], [F(x) for x in b]


# ----------------------------- Input -----------------------------
def read_manual():
    n = int(input("Jumlah variabel/persamaan (n): "))
    A, b = [], []
    print("Masukkan koefisien tiap baris (a1 a2 ... an b), boleh pecahan seperti 1/2:")
    for i in range(n):
        vals = input(f"  Baris {i+1}: ").split()
        if len(vals) != n + 1:
            raise ValueError(f"Harus {n+1} angka per baris.")
        vals = [F(v) for v in vals]
        A.append(vals[:n])
        b.append(vals[n])
    return A, b


# ----------------------------- Inti algoritma -----------------------------
def forward_elimination(A, b, pivot=False, verbose=True):
    """Ubah [A|b] menjadi segitiga atas. Return U, c, daftar pengali, jumlah swap."""
    n = len(A)
    A = [r[:] for r in A]
    b = b[:]
    mults = {}
    swaps = 0
    show_aug(A, b, "Matriks augmented awal [A | b]:") if verbose else None

    for k in range(n - 1):
        # --- pivoting ---
        if pivot:
            p = max(range(k, n), key=lambda i: abs(A[i][k]))
        else:
            p = next((i for i in range(k, n) if A[i][k] != 0), k)
        if A[p][k] == 0:
            raise ZeroDivisionError(f"Pivot nol pada kolom {k+1}: matriks singular.")
        if p != k:
            A[k], A[p] = A[p], A[k]
            b[k], b[p] = b[p], b[k]
            swaps += 1
            if verbose:
                print(f"\n>> Tukar baris R{k+1} <-> R{p+1}")

        # --- eliminasi ---
        for i in range(k + 1, n):
            if A[i][k] == 0:
                continue
            m = A[i][k] / A[k][k]
            mults[(i + 1, k + 1)] = m
            if verbose:
                print(f"\nm{i+1}{k+1} = {fmt(A[i][k])}/{fmt(A[k][k])} = {fmt(m)}"
                      f"   ->  R{i+1} <- R{i+1} - ({fmt(m)})*R{k+1}")
            for j in range(k, n):
                A[i][j] -= m * A[k][j]
            b[i] -= m * b[k]
        if verbose:
            show_aug(A, b, f"Setelah eliminasi kolom {k+1}:")

    if A[n - 1][n - 1] == 0:
        if b[n - 1] == 0:
            raise ZeroDivisionError("Sistem punya tak hingga solusi (baris nol).")
        raise ZeroDivisionError("Sistem tidak konsisten (tidak ada solusi).")
    return A, b, mults, swaps


def backward_substitution(U, c, verbose=True):
    n = len(U)
    x = [F(0)] * n
    if verbose:
        print("\nSubstitusi mundur:")
    for i in range(n - 1, -1, -1):
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (c[i] - s) / U[i][i]
        if verbose:
            terms = "".join(f" - ({fmt(U[i][j])})({fmt(x[j])})" for j in range(i + 1, n))
            print(f"  x{i+1} = ({fmt(c[i])}{terms}) / {fmt(U[i][i])} = {fmt(x[i])}  (= {float(x[i]):.6f})")
    return x


def determinant(U, swaps):
    d = F(1)
    for i in range(len(U)):
        d *= U[i][i]
    return d * (-1) ** swaps


def residual(A, b, x):
    return [sum(A[i][j] * x[j] for j in range(len(A))) - b[i] for i in range(len(A))]


# ----------------------------- Main -----------------------------
def main():
    ap = argparse.ArgumentParser(description="Eliminasi Gauss")
    ap.add_argument("--pivot", action="store_true", help="aktifkan partial pivoting")
    ap.add_argument("--manual", action="store_true", help="input matriks manual")
    ap.add_argument("--quiet", action="store_true", help="sembunyikan langkah")
    args = ap.parse_args()

    A, b = read_manual() if args.manual else to_frac(DEFAULT_A, DEFAULT_B)
    print("=" * 62)
    print(" ELIMINASI GAUSS (Forward Elimination + Backward Substitution)")
    print("=" * 62)

    try:
        U, c, mults, swaps = forward_elimination(A, b, args.pivot, not args.quiet)
    except ZeroDivisionError as e:
        print("\n[ERROR]", e)
        return

    show_aug(U, c, "Bentuk segitiga atas [U | c]:")
    print("\nDaftar pengali:", {f"m{i}{j}": fmt(m) for (i, j), m in mults.items()})
    x = backward_substitution(U, c, not args.quiet)

    print("\n" + "-" * 62)
    print("HASIL AKHIR")
    for i, v in enumerate(x, 1):
        print(f"  x{i} = {fmt(v):>8}  = {float(v): .6f}")
    print(f"\nDeterminan A = {fmt(determinant(U, swaps))}")
    r = residual(A, b, x)
    print("Residual (Ax - b) =", [fmt(v) for v in r])
    print("Verifikasi:", "BENAR (residual = 0)" if all(v == 0 for v in r) else "ADA GALAT")


if __name__ == "__main__":
    main()
