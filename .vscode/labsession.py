import math

# =====================================================
# SPNL : f(x) = cos(x) - x = 0, toleransi 0.0001
# =====================================================
def F(x):   return math.cos(x) - x
def dF(x):  return -math.sin(x) - 1
def ddF(x): return -math.cos(x)
toleransi = 0.0001

ringkas = []   # (nama metode, akar, jumlah iterasi)

# ================= FIXED-POINT ITERATION =================
print("=" * 70)
print("FIXED-POINT ITERATION :  x_r+1 = g(x_r),  g(x) = cos(x)")
print("=" * 70)
def g(x):         return math.cos(x)
def turunan_g(x): return -math.sin(x)

x0 = 0.5
turunan_di_x0 = turunan_g(x0)
print("Cek syarat konvergen:  g'(x) = -sin(x)")
print(f"  g'({x0}) = -sin({x0}) = {turunan_di_x0:.5f}   ->  |g'| = {abs(turunan_di_x0):.5f}")
if abs(turunan_di_x0) < 1:
    print("  |g'(x0)| < 1  ->  konvergen, iterasi selanjutnya bakal aman")
    tabel = []
    x_lama, r = x0, 0
    while True:
        x_baru = g(x_lama)
        selisih = abs(x_baru - x_lama)
        turunan = turunan_g(x_baru)
        print(f"\nIterasi {r+1}")
        print(f"  x_{r+1}     = cos(x_{r}) = cos({x_lama:.6f}) = {x_baru:.6f}")
        print(f"  selisih = |{x_baru:.6f} - {x_lama:.6f}| = {selisih:.6f}")
        print(f"  g'(x)   = -sin({x_baru:.6f}) = {turunan:.6f}")
        tabel.append((r+1, x_lama, x_baru, selisih, turunan))
        if selisih < toleransi:
            print(f"  {selisih:.6f} < {toleransi}  ->  BERHENTI")
            break
        print(f"  {selisih:.6f} >= {toleransi}  ->  lanjut")
        x_lama = x_baru
        r += 1
    print("\nTabel Fixed-Point")
    print(f"{'iter':>4} {'x_r':>10} {'x_r+1':>10} {'selisih':>10} {'g_prime':>10}")
    for it, xl, xb, s, tg in tabel:
        print(f"{it:>4} {xl:10.6f} {xb:10.6f} {s:10.6f} {tg:10.6f}")
    print(f"\nf({x_baru:.5f}) = cos({x_baru:.5f}) - {x_baru:.5f} = {F(x_baru):.5f}")
    print(f"Hampiran Akar: {x_baru:.5f}")
    ringkas.append(("Fixed-Point", x_baru, len(tabel)))
else:
    print("  |g'(x0)| >= 1  ->  skip, divergen")

# ================== NEWTON-RAPHSON ==================
print("\n" + "=" * 70)
print("NEWTON-RAPHSON :  x_k+1 = x_k - f(x_k)/f'(x_k)")
print("  f(x) = cos(x) - x,  f'(x) = -sin(x) - 1,  f''(x) = -cos(x)")
print("=" * 70)
x0 = 0.5
print("Cek syarat awal:")
print(f"  f'({x0}) = -sin({x0}) - 1 = {dF(x0):.6f}  (harus != 0)")
uji = abs(F(x0) * ddF(x0) / dF(x0)**2)
print("Uji kekonvergenan  |f(x)*f''(x) / [f'(x)]^2| < 1 :")
print(f"  f({x0})  = {F(x0):.6f}")
print(f"  f''({x0}) = {ddF(x0):.6f}")
print(f"  |{F(x0):.6f} * {ddF(x0):.6f} / ({dF(x0):.6f})^2| = {uji:.5f}",
      " < 1 -> konvergen" if uji < 1 else " >= 1 -> berisiko divergen")

tabel = []
xk, k = x0, 0
while True:
    fx, dfx = F(xk), dF(xk)
    x_next = xk - fx / dfx
    selisih = abs(x_next - xk)
    print(f"\nIterasi {k+1}")
    print(f"  f(x_{k})  = cos({xk:.6f}) - {xk:.6f} = {fx:.6f}")
    print(f"  f'(x_{k}) = -sin({xk:.6f}) - 1 = {dfx:.6f}")
    print(f"  x_{k+1}   = {xk:.6f} - ({fx:.6f}) / ({dfx:.6f}) = {x_next:.6f}")
    print(f"  selisih = |{x_next:.6f} - {xk:.6f}| = {selisih:.6f}")
    tabel.append((k, xk, fx, dfx, x_next, selisih))
    xk, k = x_next, k + 1
    if selisih < toleransi:
        print(f"  {selisih:.6f} < {toleransi}  ->  BERHENTI")
        break
    print(f"  {selisih:.6f} >= {toleransi}  ->  lanjut")

print("\nTabel Newton-Raphson")
print(f"{'k':>2} {'x_k':>10} {'f(x_k)':>10} {'f_prime':>10} {'x_k+1':>10} {'|x_k+1-x_k|':>12}")
for kk, xx, fx, dfx, xn, s in tabel:
    print(f"{kk:>2} {xx:10.6f} {fx:10.6f} {dfx:10.6f} {xn:10.6f} {s:12.6f}")
print(f"\nf({xk:.5f}) = {F(xk):.8f}")
print(f"Hampiran Akar: {xk:.5f}")
ringkas.append(("Newton-Raphson", xk, len(tabel)))

# ======================== SECANT ========================
print("\n" + "=" * 70)
print("SECANT :  x_i+1 = x_i - f(x_i) * (x_i - x_i-1) / (f(x_i) - f(x_i-1))")
print("=" * 70)
x0, x1 = 0.5, 1.0
print("Cek syarat awal:")
print(f"  f({x0}) = {F(x0):.6f}")
print(f"  f({x1}) = {F(x1):.6f}")
print(f"  f(x0) != f(x1)  ->  lanjut" if F(x0) != F(x1) else "  f(x0) == f(x1)  ->  STOP")

tabel = []
maks_iterasi, r = 100, 1
while r <= maks_iterasi:
    f_x0, f_x1 = F(x0), F(x1)
    x_hasil = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
    selisih = abs(x_hasil - x1)
    print(f"\nIterasi {r}   (x0 = {x0:.6f}, x1 = {x1:.6f})")
    print(f"  f(x0) = {f_x0:.6f}")
    print(f"  f(x1) = {f_x1:.6f}")
    print(f"  x_hasil = {x1:.6f} - ({f_x1:.6f}) * ({x1:.6f} - {x0:.6f}) / ({f_x1:.6f} - {f_x0:.6f})")
    print(f"          = {x_hasil:.6f}")
    print(f"  f(x_hasil) = {F(x_hasil):.6f}")
    print(f"  selisih = |{x_hasil:.6f} - {x1:.6f}| = {selisih:.6f}")
    tabel.append((r, x0, x1, x_hasil, F(x_hasil), selisih))
    if selisih < toleransi:
        print(f"  {selisih:.6f} < {toleransi}  ->  BERHENTI")
        break
    print(f"  {selisih:.6f} >= {toleransi}  ->  lanjut")
    x0, x1 = x1, x_hasil
    r += 1

print("\nTabel Secant")
print(f"{'iter':>4} {'x0':>10} {'x1':>10} {'x_hasil':>10} {'f(x_hasil)':>11} {'selisih':>10}")
for it, a0, a1, xh, fxh, s in tabel:
    print(f"{it:>4} {a0:10.6f} {a1:10.6f} {xh:10.6f} {fxh:11.6f} {s:10.6f}")
print(f"\nf({x_hasil:.5f}) = {F(x_hasil):.5f}")
print(f"Hampiran akar: {x_hasil:.5f}")
ringkas.append(("Secant", x_hasil, len(tabel)))

# ===================== PERBANDINGAN =====================
print("\n" + "=" * 70)
print("PERBANDINGAN")
print("=" * 70)
print(f"{'Metode':<16} {'Akar':>10} {'Iterasi':>8}")
for nama, akar, it in ringkas:
    print(f"{nama:<16} {akar:10.6f} {it:8d}")