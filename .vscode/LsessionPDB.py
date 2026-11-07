import math

# ==========================================
# PENYELESAIAN PERSAMAAN DIFERENSIAL BIASA
# LAB SESSION METODE NUMERIK KELAS 3B
# ==========================================

# Persamaan diferensial:
# dy/dx = x * sqrt(y)

def f(x, y):
    return x * math.sqrt(y)


# ==========================================
# PARAMETER AWAL
# ==========================================

x0 = 0
y0 = 1          # asumsi: soal tidak memberi nilai awal
xn = 1.2
h = 0.1

n = round((xn - x0) / h)

print("PENYELESAIAN PDB")
print("Persamaan: dy/dx = x * sqrt(y)")
print("Kondisi awal: y(0) = 1")
print("Jumlah iterasi:", n)
print("Ukuran langkah (h):", h)


# ==========================================
# METODE ANALITIK (EKSAK)
# ==========================================
# sqrt(y) = x^2/4 + 1  ->  y = (1 + x^2/4)^2

def eksak(x):
    return (1 + x**2 / 4) ** 2

y_eksak = eksak(xn)

print("\nHASIL METODE ANALITIK")
print(f"Nilai y(1.2) = {y_eksak:.6f}")


# ==========================================
# INISIALISASI METODE NUMERIK
# ==========================================

x = x0

y_euler = y0
y_heun = y0
y_rk4 = y0

hasil = []

hasil.append([0, x, y_euler, y_heun, y_rk4, eksak(x)])


# ==========================================
# PERULANGAN 12 ITERASI
# ==========================================

for i in range(1, n + 1):

    # --------------------------------------
    # METODE EULER
    # --------------------------------------

    y_euler_baru = y_euler + h * f(x, y_euler)


    # --------------------------------------
    # METODE HEUN
    # --------------------------------------

    k1 = f(x, y_heun)

    yp = y_heun + h * k1

    k2 = f(x + h, yp)

    y_heun_baru = y_heun + (h / 2) * (k1 + k2)


    # --------------------------------------
    # METODE RUNGE-KUTTA ORDE 4
    # --------------------------------------

    k1 = f(x, y_rk4)

    k2 = f(x + h/2, y_rk4 + h/2*k1)

    k3 = f(x + h/2, y_rk4 + h/2*k2)

    k4 = f(x + h, y_rk4 + h*k3)

    y_rk4_baru = y_rk4 + (h/6) * (
        k1 + 2*k2 + 2*k3 + k4
    )


    # --------------------------------------
    # UPDATE NILAI
    # --------------------------------------

    x = x + h

    y_euler = y_euler_baru
    y_heun = y_heun_baru
    y_rk4 = y_rk4_baru

    hasil.append([
        i, x, y_euler, y_heun, y_rk4, eksak(x)
    ])


# ==========================================
# MENAMPILKAN TABEL HASIL ITERASI
# ==========================================

print("\nTABEL HASIL ITERASI")
print("-" * 85)

print(
    f"{'Iterasi':<10}"
    f"{'x':<10}"
    f"{'Euler':<15}"
    f"{'Heun':<15}"
    f"{'RK4':<15}"
    f"{'Eksak':<15}"
)

print("-" * 85)

for data in hasil:
    print(
        f"{data[0]:<10}"
        f"{data[1]:<10.1f}"
        f"{data[2]:<15.6f}"
        f"{data[3]:<15.6f}"
        f"{data[4]:<15.6f}"
        f"{data[5]:<15.6f}"
    )


# ==========================================
# MENGHITUNG GALAT ABSOLUT
# ==========================================

galat_euler = abs(y_eksak - y_euler)
galat_heun = abs(y_eksak - y_heun)
galat_rk4 = abs(y_eksak - y_rk4)


# ==========================================
# MENGHITUNG GALAT RELATIF
# ==========================================

relatif_euler = (galat_euler / abs(y_eksak)) * 100
relatif_heun = (galat_heun / abs(y_eksak)) * 100
relatif_rk4 = (galat_rk4 / abs(y_eksak)) * 100


# ==========================================
# MENAMPILKAN HASIL AKHIR DAN GALAT
# ==========================================

print("\nHASIL AKHIR y(1.2)")
print("-" * 60)

print(f"Analitik : {y_eksak:.6f}")
print(f"Euler    : {y_euler:.6f}")
print(f"Heun     : {y_heun:.6f}")
print(f"RK4      : {y_rk4:.6f}")


print("\nTABEL GALAT")
print("-" * 75)

print(
    f"{'Metode':<15}"
    f"{'Galat Absolut':<25}"
    f"{'Galat Relatif (%)':<20}"
    f"{'< 0.0001 ?':<15}"
)

print("-" * 75)

epsilon = 0.0001

for nama, ga, gr in [
    ("Euler", galat_euler, relatif_euler),
    ("Heun", galat_heun, relatif_heun),
    ("RK4", galat_rk4, relatif_rk4),
]:
    status = "Ya" if ga < epsilon else "Tidak"
    print(
        f"{nama:<15}"
        f"{ga:<25.9f}"
        f"{gr:<20.6f}"
        f"{status:<15}"
    )