import numpy as np
import pandas as pd

# ==========================================
# 1. DEFINISI PERSAMAAN
# ==========================================

def f(x, y):
    return (4*x**3 - 2*x + 1) / (2 + y)

# Parameter awal
x0 = 0
y0 = 1
b = 2
N = 15

h = (b - x0) / N

# Solusi analitik
def exact(x):
    return -2 + np.sqrt(2*x**4 - 2*x**2 + 2*x + 9)

y_exact = exact(b)

# Menyimpan hasil iterasi
hasil_euler = [y0]
hasil_heun = [y0]
hasil_rk4 = [y0]

# ==========================================
# 2. METODE EULER
# ==========================================

x = x0
y = y0

for i in range(N):
    y = y + h * f(x, y)
    x = x + h
    hasil_euler.append(y)

# ==========================================
# 3. METODE HEUN (RK2)
# ==========================================

x = x0
y = y0

for i in range(N):
    k1 = f(x, y)
    k2 = f(x + h, y + h*k1)

    y = y + (h/2) * (k1 + k2)
    x = x + h

    hasil_heun.append(y)

# ==========================================
# 4. METODE RUNGE-KUTTA ORDE 4
# ==========================================

x = x0
y = y0

for i in range(N):
    k1 = f(x, y)
    k2 = f(x + h/2, y + h*k1/2)
    k3 = f(x + h/2, y + h*k2/2)
    k4 = f(x + h, y + h*k3)

    y = y + (h/6) * (
        k1 + 2*k2 + 2*k3 + k4
    )

    x = x + h
    hasil_rk4.append(y)

# ==========================================
# 5. TABEL ITERASI
# ==========================================

data = []

for i in range(N+1):
    x = x0 + i*h

    data.append([
        i,
        x,
        hasil_euler[i],
        hasil_heun[i],
        hasil_rk4[i]
    ])

tabel = pd.DataFrame(
    data,
    columns=[
        "Iterasi",
        "x",
        "Euler",
        "Heun",
        "RK4"
    ]
)

print("TABEL HASIL ITERASI")
print(tabel.to_string(index=False))

# ==========================================
# 6. MENGHITUNG GALAT
# ==========================================

metode = {
    "Analitik": y_exact,
    "Euler": hasil_euler[-1],
    "Heun": hasil_heun[-1],
    "RK4": hasil_rk4[-1]
}

print("\nHASIL AKHIR DAN GALAT")

for nama, nilai in metode.items():

    galat_absolut = abs(y_exact - nilai)

    galat_relatif = (
        galat_absolut / abs(y_exact)
    ) * 100

    print("\nMetode:", nama)
    print("Nilai y(2):", nilai)
    print("Galat absolut:", galat_absolut)
    print("Galat relatif (%):", galat_relatif)

# ==========================================
# 7. KESIMPULAN
# ==========================================

print("\nNILAI EKSAK =", y_exact)
print("NILAI EULER =", hasil_euler[-1])
print("NILAI HEUN  =", hasil_heun[-1])
print("NILAI RK4   =", hasil_rk4[-1])
