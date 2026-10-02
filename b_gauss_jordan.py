#!/usr/bin/env python3
"""
METODE B - ELIMINASI GAUSS-JORDAN
=================================
Tahap 1: Forward elimination (sama seperti Gauss) -> segitiga atas
Tahap 2: Backward elimination -> matriks diagonal
Tahap 3: Normalisasi -> matriks identitas, solusi langsung terbaca di kolom b

Fitur: pecahan eksak, partial pivoting opsional, log pengali, invers matriks A
       (opsional --inverse, [A|I] -> [I|A^-1]), determinan, residual, verifikasi.

Pemakaian:
    python b_gauss_jordan.py
    python b_gauss_jordan.py --pivot --inverse
    python b_gauss_jordan.py --manual
"""
import argparse
from fractions import Fraction as F

DEFAULT_A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
DEFAULT_B = [3, 9, 4]


def fmt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def show(M, n, title=""):
    """Cetak matriks augmented M (n baris), kolom ke-n adalah pemisah '|'."""
    if title:
        print(f"\n{title}")
    w = max(len(fmt(x)) for r in M for x in r) + 1
    for r in M:
        left = " ".join(fmt(x).rjust(w) for x in r[:n])
        right = " ".join(fmt(x).rjust(w) for x in r[n:])
        print(f"  [ {left} | {right} ]")


def read_manual():
    n = int(input("Jumlah variabel/persamaan (n): "))
    A, b = [], []
    print("Masukkan tiap baris: a1 ... an b (boleh pecahan, mis. 1/2)")
    for i in range(n):
        v = [F(t) for t in input(f"  Baris {i+1}: ").split()]
        if len(v) != n + 1:
            raise ValueError(f"Harus {n+1} angka.")
        A.append(v[:n]); b.append(v[n])
    return A, b


def gauss_jordan(A, b, pivot=False, with_inverse=False, verbose=True):
    n = len(A)
    # Bangun matriks augmented [A | b (| I)]
    M = []
    for i in range(n):
        row = [F(x) for x in A[i]] + [F(b[i])]
        if with_inverse:
            row += [F(1) if i == j else F(0) for j in range(n)]
        M.append(row)
    ncoef = n  # kolom pemisah ditampilkan setelah n kolom pertama
    det = F(1)
    mults = []

    if verbose:
        show(M, ncoef, "Matriks augmented awal:")

    # ---------------- TAHAP 1: Forward elimination ----------------
    if verbose:
        print("\n" + "=" * 20 + " TAHAP 1: FORWARD ELIMINATION " + "=" * 20)
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(M[i][k])) if pivot else \
            next((i for i in range(k, n) if M[i][k] != 0), k)
        if M[p][k] == 0:
            raise ZeroDivisionError(f"Matriks singular (pivot nol kolom {k+1}).")
        if p != k:
            M[k], M[p] = M[p], M[k]
            det = -det
            if verbose:
                print(f"\n>> Tukar R{k+1} <-> R{p+1}")
        for i in range(k + 1, n):
            if M[i][k] == 0:
                continue
            m = M[i][k] / M[k][k]
            mults.append(((i + 1, k + 1), m))
            if verbose:
                print(f"\nm{i+1}{k+1} = {fmt(m)} :  R{i+1} <- R{i+1} - ({fmt(m)})*R{k+1}")
            M[i] = [a - m * c for a, c in zip(M[i], M[k])]
        if verbose:
            show(M, ncoef, f"Setelah kolom {k+1}:")
    if verbose:
        show(M, ncoef, "Hasil forward elimination (segitiga atas):")

    # ---------------- TAHAP 2: Backward elimination ----------------
    if verbose:
        print("\n" + "=" * 20 + " TAHAP 2: BACKWARD ELIMINATION " + "=" * 19)
    for k in range(n - 1, 0, -1):
        for i in range(k - 1, -1, -1):
            if M[i][k] == 0:
                continue
            m = M[i][k] / M[k][k]
            if verbose:
                print(f"\nR{i+1} <- R{i+1} - ({fmt(m)})*R{k+1}")
            M[i] = [a - m * c for a, c in zip(M[i], M[k])]
        if verbose:
            show(M, ncoef, f"Setelah menghapus elemen di atas pivot {k+1}:")
    if verbose:
        show(M, ncoef, "Hasil backward elimination (diagonal):")

    # ---------------- TAHAP 3: Normalisasi ----------------
    if verbose:
        print("\n" + "=" * 20 + " TAHAP 3: NORMALISASI " + "=" * 28)
    for i in range(n):
        d = M[i][i]
        det *= d
        if verbose:
            print(f"R{i+1} <- R{i+1} / ({fmt(d)})")
        M[i] = [v / d for v in M[i]]
    if verbose:
        show(M, ncoef, "Matriks identitas [I | x]:")

    x = [M[i][n] for i in range(n)]
    inv = [row[n + 1:] for row in M] if with_inverse else None
    return x, det, inv, mults


def main():
    ap = argparse.ArgumentParser(description="Eliminasi Gauss-Jordan")
    ap.add_argument("--pivot", action="store_true")
    ap.add_argument("--manual", action="store_true")
    ap.add_argument("--inverse", action="store_true", help="hitung juga invers A")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if a.manual:
        A, b = read_manual()
    else:
        A, b = [[F(x) for x in r] for r in DEFAULT_A], [F(x) for x in DEFAULT_B]

    print("=" * 62)
    print(" ELIMINASI GAUSS-JORDAN")
    print("=" * 62)
    try:
        x, det, inv, _ = gauss_jordan(A, b, a.pivot, a.inverse, not a.quiet)
    except ZeroDivisionError as e:
        print("[ERROR]", e); return

    print("\n" + "-" * 62 + "\nHASIL AKHIR (langsung dibaca dari kolom b)")
    for i, v in enumerate(x, 1):
        print(f"  x{i} = {fmt(v):>8}  = {float(v): .6f}")
    print(f"\nDeterminan A = {fmt(det)}")
    if inv:
        print("\nInvers A:")
        for r in inv:
            print("  [ " + "  ".join(fmt(v).rjust(7) for v in r) + " ]")
    res = [sum(A[i][j] * x[j] for j in range(len(A))) - b[i] for i in range(len(A))]
    print("Residual (Ax - b) =", [fmt(v) for v in res])
    print("Verifikasi:", "BENAR (residual = 0)" if all(v == 0 for v in res) else "ADA GALAT")


if __name__ == "__main__":
    main()
