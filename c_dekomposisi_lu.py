#!/usr/bin/env python3
"""
METODE C - DEKOMPOSISI LU
=========================
  A = L U   (tanpa pivot)   atau   P A = L U   (dengan --pivot)
  L : segitiga bawah, diagonal = 1, isinya pengali m_ij dari forward elimination
  U : segitiga atas (hasil forward elimination)
Penyelesaian:  L y = P b (forward substitution),  U x = y (backward substitution)

Fitur: pecahan eksak, pencatatan pengali, verifikasi A = LU (perkalian matriks
ditampilkan), partial pivoting + matriks permutasi P, determinan dari diagonal U,
residual. Bisa menyelesaikan beberapa vektor b sekaligus (--multi) memakai LU yang sama.

Pemakaian:
    python c_dekomposisi_lu.py
    python c_dekomposisi_lu.py --pivot
    python c_dekomposisi_lu.py --manual --multi
"""
import argparse
from fractions import Fraction as F

DEFAULT_A = [[2, 1, -1], [4, 3, 1], [-2, 1, 2]]
DEFAULT_B = [3, 9, 4]


def fmt(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def show_mat(M, name):
    w = max(len(fmt(x)) for r in M for x in r) + 1
    print(f"\n{name} =")
    for r in M:
        print("  [ " + " ".join(fmt(x).rjust(w) for x in r) + " ]")


def matmul(X, Y):
    n, m, p = len(X), len(Y), len(Y[0])
    return [[sum(X[i][k] * Y[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def read_matrix_manual(multi):
    n = int(input("Ukuran n: "))
    A = []
    print("Masukkan matriks A (tiap baris n angka):")
    for i in range(n):
        v = [F(t) for t in input(f"  Baris {i+1}: ").split()]
        if len(v) != n:
            raise ValueError(f"Harus {n} angka.")
        A.append(v)
    bs = []
    k = int(input("Jumlah vektor b: ")) if multi else 1
    for t in range(k):
        v = [F(s) for s in input(f"  Vektor b{t+1} ({n} angka): ").split()]
        if len(v) != n:
            raise ValueError(f"Harus {n} angka.")
        bs.append(v)
    return A, bs


def lu_decompose(A, pivot=False, verbose=True):
    """Return L, U, perm (list indeks baris), swaps, daftar pengali."""
    n = len(A)
    U = [[F(x) for x in r] for r in A]
    L = [[F(0)] * n for _ in range(n)]
    perm = list(range(n))
    swaps = 0
    mults = []
    if verbose:
        show_mat(U, "A (awal)")

    for k in range(n - 1):
        p = max(range(k, n), key=lambda i: abs(U[i][k])) if pivot else \
            next((i for i in range(k, n) if U[i][k] != 0), k)
        if U[p][k] == 0:
            raise ZeroDivisionError(f"Matriks singular (pivot nol kolom {k+1}).")
        if p != k:
            U[k], U[p] = U[p], U[k]
            L[k], L[p] = L[p], L[k]   # tukar pengali yang sudah terbentuk
            perm[k], perm[p] = perm[p], perm[k]
            swaps += 1
            if verbose:
                print(f"\n>> Tukar baris R{k+1} <-> R{p+1}")
        for i in range(k + 1, n):
            m = U[i][k] / U[k][k]
            L[i][k] = m
            mults.append((f"m{i+1}{k+1}", m))
            if m != 0:
                if verbose:
                    print(f"\nm{i+1}{k+1} = {fmt(U[i][k])}/{fmt(U[k][k])} = {fmt(m)}"
                          f" :  R{i+1} <- R{i+1} - ({fmt(m)})*R{k+1}")
                U[i] = [a - m * c for a, c in zip(U[i], U[k])]
        if verbose:
            show_mat(U, f"U sementara (setelah kolom {k+1})")
    if U[n - 1][n - 1] == 0:
        raise ZeroDivisionError("Matriks singular (U[n][n] = 0).")
    for i in range(n):
        L[i][i] = F(1)
    return L, U, perm, swaps, mults


def forward_sub(L, b, verbose=True):
    n = len(L)
    y = [F(0)] * n
    if verbose:
        print("\nForward substitution  L y = b :")
    for i in range(n):
        s = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - s) / L[i][i]
        if verbose:
            t = "".join(f" - ({fmt(L[i][j])})({fmt(y[j])})" for j in range(i))
            print(f"  y{i+1} = {fmt(b[i])}{t} = {fmt(y[i])}")
    return y


def backward_sub(U, y, verbose=True):
    n = len(U)
    x = [F(0)] * n
    if verbose:
        print("\nBackward substitution  U x = y :")
    for i in range(n - 1, -1, -1):
        s = sum(U[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (y[i] - s) / U[i][i]
        if verbose:
            t = "".join(f" - ({fmt(U[i][j])})({fmt(x[j])})" for j in range(i + 1, n))
            print(f"  x{i+1} = ({fmt(y[i])}{t}) / {fmt(U[i][i])} = {fmt(x[i])}  (= {float(x[i]):.6f})")
    return x


def main():
    ap = argparse.ArgumentParser(description="Dekomposisi LU")
    ap.add_argument("--pivot", action="store_true", help="PA = LU (partial pivoting)")
    ap.add_argument("--manual", action="store_true")
    ap.add_argument("--multi", action="store_true", help="banyak vektor b (mode manual)")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    v = not a.quiet

    if a.manual:
        A, bs = read_matrix_manual(a.multi)
    else:
        A, bs = [[F(x) for x in r] for r in DEFAULT_A], [[F(x) for x in DEFAULT_B]]

    print("=" * 62 + "\n DEKOMPOSISI LU\n" + "=" * 62)
    try:
        L, U, perm, swaps, mults = lu_decompose(A, a.pivot, v)
    except ZeroDivisionError as e:
        print("[ERROR]", e); return

    n = len(A)
    print("\nPengali (isi L):", {k: fmt(m) for k, m in mults})
    show_mat(L, "L"); show_mat(U, "U")

    # Matriks permutasi P dan PA
    P = [[F(1) if perm[i] == j else F(0) for j in range(n)] for i in range(n)]
    PA = matmul(P, [[F(x) for x in r] for r in A])
    LU = matmul(L, U)
    if a.pivot:
        show_mat(P, "P")
    show_mat(LU, "L x U")
    show_mat(PA, "P A" if a.pivot else "A")
    ok = LU == PA
    print("\nVerifikasi", "PA = LU" if a.pivot else "A = LU", ":", "TERBUKTI (semua elemen sama)" if ok else "GAGAL")

    det = F(1)
    for i in range(n):
        det *= U[i][i]
    det *= (-1) ** swaps
    print(f"Determinan A = det(U) x (-1)^swap = {fmt(det)}")

    for t, b in enumerate(bs, 1):
        print("\n" + "-" * 62)
        print(f"SISTEM b{t} = [{', '.join(fmt(x) for x in b)}]")
        Pb = [b[perm[i]] for i in range(n)]
        if a.pivot:
            print("P b =", [fmt(x) for x in Pb])
        y = forward_sub(L, Pb, v)
        x = backward_sub(U, y, v)
        print("\nHASIL AKHIR")
        print("  y =", [fmt(t_) for t_ in y])
        for i, val in enumerate(x, 1):
            print(f"  x{i} = {fmt(val):>8}  = {float(val): .6f}")
        r = [sum(A[i][j] * x[j] for j in range(n)) - b[i] for i in range(n)]
        print("  Residual (Ax - b) =", [fmt(q) for q in r])
        print("  Verifikasi:", "BENAR (residual = 0)" if all(q == 0 for q in r) else "ADA GALAT")


if __name__ == "__main__":
    main()
