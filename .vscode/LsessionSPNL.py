import math

# ==========================================
# PENYELESAIAN SISTEM PERSAMAAN NON-LINEAR
# LAB SESSION METODE NUMERIK KELAS 3B
# ==========================================

# Persamaan: f(x) = cos(x) - x = 0

def f(x):
    return math.cos(x) - x

def turunan_f(x):
    return -math.sin(x) - 1

def g(x):                    # untuk Fixed-Point: x = cos(x)
    return math.cos(x)

def turunan_g(x):
    return -math.sin(x)


# ==========================================
# PARAMETER AWAL
# ==========================================

x0 = 0.5                     # syarat: 0 < x0 < 1.4
x1 = 1.0                     # tebakan kedua untuk Secant
toleransi = 0.0001
maks_iterasi = 100

print("PENYELESAIAN f(x) = cos(x) - x = 0")
print("Tebakan awal x0 :", x0)
print("Tebakan kedua x1 (Secant) :", x1)
print("Toleransi :", toleransi)


# ==========================================
# METODE 1 : FIXED-POINT ITERATION
# ==========================================

print("\n" + "=" * 70)
print("METODE FIXED-POINT ITERATION  (g(x) = cos(x))")
print("=" * 70)

print(f"Cek syarat: |g'({x0})| = {abs(turunan_g(x0)):.6f}")

hasil_fp = []

if abs(turunan_g(x0)) < 1:
    print("|g'(x0)| < 1 -> konvergen, iterasi dilanjutkan\n")

    x_lama = x0
    for i in range(1, maks_iterasi + 1):
        x_baru = g(x_lama)
        selisih = abs(x_baru - x_lama)
        hasil_fp.append([i, x_lama, x_baru, selisih, turunan_g(x_baru)])
        if selisih < toleransi:
            break
        x_lama = x_baru

    print("-" * 70)
    print(f"{'Iterasi':<10}{'x_r':<15}{'x_r+1':<15}{'Selisih':<15}{'g prime':<15}")
    print("-" * 70)
    for d in hasil_fp:
        print(f"{d[0]:<10}{d[1]:<15.6f}{d[2]:<15.6f}{d[3]:<15.6f}{d[4]:<15.6f}")

    akar_fp = x_baru
    print(f"\nHampiran akar = {akar_fp:.6f}")
    print(f"f(akar)       = {f(akar_fp):.9f}")
else:
    print("|g'(x0)| >= 1 -> divergen, iterasi dihentikan")
    akar_fp = None


# ==========================================
# METODE 2 : NEWTON-RAPHSON
# ==========================================

print("\n" + "=" * 70)
print("METODE NEWTON-RAPHSON  (f'(x) = -sin(x) - 1)")
print("=" * 70)

print(f"Cek syarat: f'({x0}) = {turunan_f(x0):.6f}")

hasil_nr = []

if turunan_f(x0) != 0:
    print("f'(x0) != 0 -> iterasi dilanjutkan\n")

    x_lama = x0
    for i in range(1, maks_iterasi + 1):
        fx = f(x_lama)
        dfx = turunan_f(x_lama)
        x_baru = x_lama - fx / dfx
        selisih = abs(x_baru - x_lama)
        hasil_nr.append([i, x_lama, fx, dfx, x_baru, selisih])
        if selisih < toleransi:
            break
        x_lama = x_baru

    print("-" * 85)
    print(f"{'Iterasi':<10}{'x_k':<15}{'f(x_k)':<15}{'df(x_k)':<15}{'x_k+1':<15}{'Selisih':<15}")
    print("-" * 85)
    for d in hasil_nr:
        print(f"{d[0]:<10}{d[1]:<15.6f}{d[2]:<15.6f}{d[3]:<15.6f}{d[4]:<15.6f}{d[5]:<15.6f}")

    akar_nr = x_baru
    print(f"\nHampiran akar = {akar_nr:.6f}")
    print(f"f(akar)       = {f(akar_nr):.9f}")
else:
    print("f'(x0) = 0 -> iterasi dihentikan")
    akar_nr = None


# ==========================================
# METODE 3 : SECANT
# ==========================================

print("\n" + "=" * 70)
print("METODE SECANT")
print("=" * 70)

print(f"Cek syarat: f({x0}) = {f(x0):.6f},  f({x1}) = {f(x1):.6f}")

hasil_sc = []

if f(x0) != f(x1):
    print("f(x0) != f(x1) -> iterasi dilanjutkan\n")

    xa, xb = x0, x1
    for i in range(1, maks_iterasi + 1):
        fa, fb = f(xa), f(xb)
        x_baru = xb - fb * (xb - xa) / (fb - fa)
        selisih = abs(x_baru - xb)
        hasil_sc.append([i, xa, xb, x_baru, f(x_baru), selisih])
        if selisih < toleransi:
            break
        xa, xb = xb, x_baru

    print("-" * 85)
    print(f"{'Iterasi':<10}{'x0':<15}{'x1':<15}{'x_baru':<15}{'f(x_baru)':<15}{'Selisih':<15}")
    print("-" * 85)
    for d in hasil_sc:
        print(f"{d[0]:<10}{d[1]:<15.6f}{d[2]:<15.6f}{d[3]:<15.6f}{d[4]:<15.6f}{d[5]:<15.6f}")

    akar_sc = x_baru
    print(f"\nHampiran akar = {akar_sc:.6f}")
    print(f"f(akar)       = {f(akar_sc):.9f}")
else:
    print("f(x0) = f(x1) -> iterasi dihentikan")
    akar_sc = None


# ==========================================
# PERBANDINGAN
# ==========================================

print("\n" + "=" * 70)
print("PERBANDINGAN METODE")
print("=" * 70)

print(f"{'Metode':<20}{'Akar':<15}{'Iterasi':<10}")
print("-" * 45)
print(f"{'Fixed-Point':<20}{akar_fp:<15.6f}{len(hasil_fp):<10}")
print(f"{'Newton-Raphson':<20}{akar_nr:<15.6f}{len(hasil_nr):<10}")
print(f"{'Secant':<20}{akar_sc:<15.6f}{len(hasil_sc):<10}")