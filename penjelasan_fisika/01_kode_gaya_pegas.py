# KODE GAYA PEGAS
# Tugas Akhir - Dimas, Daffa, Dharma

import numpy as np
from scipy.integrate import odeint


# Parameter Sistem
class SpringParameters:
    def __init__(self, m, k, c, x0, v0):
        self.m = m      # Massa (kg)
        self.k = k      # Konstanta pegas (N/m)
        self.c = c      # Koefisien redaman (Ns/m)
        self.x0 = x0    # Posisi awal (m)
        self.v0 = v0    # Kecepatan awal (m/s)
    
    # Frekuensi Natural: omega_n = sqrt(k/m)
    @property
    def omega_n(self):
        return np.sqrt(self.k / self.m)
    
    # Rasio Redaman: zeta = c / (2*sqrt(k*m))
    @property
    def zeta(self):
        return self.c / (2 * np.sqrt(self.k * self.m))


# Persamaan Gerak (Hukum Hooke + Newton II)
# m*x'' + c*x' + k*x = F(t)
def spring_ode(state, t, params, F_ext=None):
    x, v = state
    F = F_ext(t) if F_ext else 0
    
    dxdt = v                                          # dx/dt = v
    dvdt = (F - params.c*v - params.k*x) / params.m   # F = ma
    
    return [dxdt, dvdt]


# Solver
def solve(params, t_max, F_ext=None):
    t = np.linspace(0, t_max, 1000)
    sol = odeint(spring_ode, [params.x0, params.v0], t, args=(params, F_ext))
    x, v = sol[:,0], sol[:,1]
    
    # Energi
    KE = 0.5 * params.m * v**2   # Kinetik
    PE = 0.5 * params.k * x**2   # Potensial
    
    return {'t': t, 'x': x, 'v': v, 'KE': KE, 'PE': PE}


# RUMUS:
# F = -kx                   (Hukum Hooke)
# m*x'' + c*x' + k*x = F(t) (Persamaan Gerak)
# omega_n = sqrt(k/m)       (Frekuensi Natural)
# zeta = c / (2*sqrt(k*m))  (Rasio Redaman)
# KE = 0.5*m*v^2            (Energi Kinetik)
# PE = 0.5*k*x^2            (Energi Potensial)
