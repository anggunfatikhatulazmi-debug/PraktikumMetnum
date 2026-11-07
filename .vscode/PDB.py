
import math

# ==========================================
# PENYELESAIAN PERSAMAAN DIFERENSIAL BIASA
# ==========================================

# Persamaan diferensial:
# dy/dx = (4x^3 - 2x + 1) / (2 + y)

def f(x, y):
    return (4*x**3 - 2*x + 1) / (2 + y)


# ==========================================
# PARAMETER AWAL
# ==========================================

x0 = 0
y0 = 1
xn = 2
n = 15

h = (xn - x0) / n

print("PENYELESAIAN PDB")
print("Persamaan: dy/dx = (4x^3 - 2x + 1)/(2+y)")
print("Kondisi awal: y(0) = 1")
print("Jumlah iterasi:", n)
print("Ukuran langkah (h):", h)


# ==========================================
# METODE ANALITIK (EKSAK)
# ==========================================

y_eksak = -2 + math.sqrt(
    2*xn**4 - 2*xn**2 + 2*xn + 9
)

print("\nHASIL METODE ANALITIK")
print("Nilai y(2) =", y_eksak)


# ==========================================
# INISIALISASI METODE NUMERIK
# ==========================================

x = x0

y_euler = y0
y_heun = y0
y_rk4 = y0

hasil = []

hasil.append([0, x, y_euler, y_heun, y_rk4])


# ==========================================
# PERULANGAN 15 ITERASI
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
        i, x, y_euler, y_heun, y_rk4
    ])


# ==========================================
# MENAMPILKAN TABEL HASIL ITERASI
# ==========================================

print("\nTABEL HASIL ITERASI")
print("-" * 85)

print(
    f"{'Iterasi':<10}"
    f"{'x':<15}"
    f"{'Euler':<18}"
    f"{'Heun':<18}"
    f"{'RK4':<18}"
)

print("-" * 85)

for data in hasil:
    print(
        f"{data[0]:<10}"
        f"{data[1]:<15.6f}"
        f"{data[2]:<18.9f}"
        f"{data[3]:<18.9f}"
        f"{data[4]:<18.9f}"
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

print("\nHASIL AKHIR y(2)")
print("-" * 60)

print(f"Analitik : {y_eksak:.9f}")
print(f"Euler    : {y_euler:.9f}")
print(f"Heun     : {y_heun:.9f}")
print(f"RK4      : {y_rk4:.9f}")


print("\nTABEL GALAT")
print("-" * 75)

print(
    f"{'Metode':<15}"
    f"{'Galat Absolut':<25}"
    f"{'Galat Relatif (%)':<20}"
)

print("-" * 75)

print(
    f"{'Euler':<15}"
    f"{galat_euler:<25.9f}"
    f"{relatif_euler:<20.6f}"
)

print(
    f"{'Heun':<15}"
    f"{galat_heun:<25.9f}"
    f"{relatif_heun:<20.6f}"
)

print(
    f"{'RK4':<15}"
    f"{galat_rk4:<25.9f}"
    f"{relatif_rk4:<20.6f}"
)

print("-" * 75)
print("Perhitungan selesai.")
