import numpy as np
import matplotlib.pyplot as plt
import math

# ==========================================================
# FUNGSI
# ==========================================================

def f1(x):
    return 3*x**3 - 5*x**2 + 4*x - 8

def f2(x):
    return np.exp(x) - x**2

def f3(x):
    return np.log(x + 2) + 2*x - 3


# ==========================================================
# GRAFIK TUNGGAL
# ==========================================================

# ---------- Persamaan 1 ----------
x = np.linspace(1, 2, 500)

plt.figure(figsize=(8, 5))
plt.plot(x, f1(x), label='f(x) = 3x³ - 5x² + 4x - 8')
plt.axhline(0, linewidth=1, label='y = 0')

plt.scatter(1.7664, 0, s=60, label='Akar ≈ 1.7664')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Grafik Tunggal Persamaan 1')
plt.grid(True)
plt.legend()
plt.show()


# ---------- Persamaan 2 ----------
x = np.linspace(-1, 0, 500)

plt.figure(figsize=(8, 5))
plt.plot(x, f2(x), label='f(x) = eˣ - x²')
plt.axhline(0, linewidth=1, label='y = 0')

plt.scatter(-0.7035, 0, s=60, label='Akar ≈ -0.7035')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Grafik Tunggal Persamaan 2')
plt.grid(True)
plt.legend()
plt.show()


# ---------- Persamaan 3 ----------
x = np.linspace(0, 1, 500)

plt.figure(figsize=(8, 5))
plt.plot(x, f3(x), label='f(x) = ln(x+2) + 2x - 3')
plt.axhline(0, linewidth=1, label='y = 0')

plt.scatter(0.9578, 0, s=60, label='Akar ≈ 0.9578')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Grafik Tunggal Persamaan 3')
plt.grid(True)
plt.legend()
plt.show()


# ==========================================================
# GRAFIK GANDA
# ==========================================================

# ---------- Persamaan 1 ----------
x = np.linspace(1, 2, 500)

y_kiri = 3*x**3 - 5*x**2 + 4*x - 7
y_kanan = np.ones_like(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y_kiri, label='y = 3x³ - 5x² + 4x - 7')
plt.plot(x, y_kanan, label='y = 1')

plt.scatter(1.7664, 1, s=60, label='Titik potong ≈ 1.7664')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Grafik Ganda Persamaan 1')
plt.grid(True)
plt.legend()
plt.show()


# ---------- Persamaan 2 ----------
x = np.linspace(-1, 0, 500)

y_kiri = np.exp(x) - x**2
y_kanan = np.zeros_like(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y_kiri, label='y = eˣ - x²')
plt.plot(x, y_kanan, label='y = 0')

plt.scatter(-0.7035, 0, s=60, label='Titik potong ≈ -0.7035')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Grafik Ganda Persamaan 2')
plt.grid(True)
plt.legend()
plt.show()


# ---------- Persamaan 3 ----------
x = np.linspace(0, 1, 500)

y_kiri = np.log(x + 2) + 2*x
y_kanan = np.full_like(x, 3)

plt.figure(figsize=(8, 5))
plt.plot(x, y_kiri, label='y = ln(x+2) + 2x')
plt.plot(x, y_kanan, label='y = 3')

plt.scatter(0.9578, 3, s=60, label='Titik potong ≈ 0.9578')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Grafik Ganda Persamaan 3')
plt.grid(True)
plt.legend()
plt.show()