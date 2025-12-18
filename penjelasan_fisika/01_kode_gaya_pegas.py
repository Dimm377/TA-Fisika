# ============================================================
# 📚 KODE FISIKA GAYA PEGAS - UNTUK DIPELAJARI & DIJELASKAN
# ============================================================
# File ini berisi potongan kode yang berhubungan dengan gaya pegas
# Tujuan: Untuk memahami dan menjelaskan implementasi fisika
# TIDAK untuk di-run, hanya untuk referensi pembelajaran
# ============================================================


# ============================================================
# BAGIAN 1: DEFINISI PARAMETER SISTEM PEGAS
# ============================================================
"""
Parameter yang mendefinisikan sistem massa-pegas:
- m: Massa benda (kg)
- k: Konstanta pegas (N/m) - dari Hukum Hooke
- c: Koefisien redaman (Ns/m)
- x0: Posisi awal (m)
- v0: Kecepatan awal (m/s)
"""

@dataclass
class SpringParameters:
    m: float      # Massa (kg)
    k: float      # Konstanta pegas (N/m) ← HUKUM HOOKE: F = -kx
    c: float      # Koefisien redaman (Ns/m)
    x0: float     # Posisi awal (m)
    v0: float     # Kecepatan awal (m/s)


# ============================================================
# BAGIAN 2: FREKUENSI NATURAL (ωₙ)
# ============================================================
"""
Frekuensi natural adalah frekuensi osilasi sistem tanpa redaman.

RUMUS: ωₙ = √(k/m)

Penjelasan:
- Semakin besar k (pegas kaku) → osilasi semakin cepat
- Semakin besar m (massa berat) → osilasi semakin lambat
"""

@property
def omega_n(self) -> float:
    # Implementasi rumus: ωₙ = √(k/m)
    return np.sqrt(self.k / self.m)


# ============================================================
# BAGIAN 3: RASIO REDAMAN (ζ - ZETA)
# ============================================================
"""
Rasio redaman menentukan perilaku sistem:

RUMUS: ζ = c / (2√km)

Klasifikasi:
- ζ = 0     : Tidak ada redaman (osilasi terus)
- 0 < ζ < 1 : Underdamped (osilasi teredam)
- ζ = 1     : Critically damped (kembali tercepat tanpa osilasi)
- ζ > 1     : Overdamped (kembali lambat tanpa osilasi)
"""

@property
def zeta(self) -> float:
    # Implementasi rumus: ζ = c / (2√km)
    return self.c / (2 * np.sqrt(self.k * self.m))


# ============================================================
# ⭐ BAGIAN 4: PERSAMAAN GERAK - INTI FISIKA ⭐
# ============================================================
"""
Ini adalah INTI dari simulasi gaya pegas!

HUKUM NEWTON II untuk sistem pegas:
    ΣF = ma
    
Gaya-gaya yang bekerja:
    1. Gaya pegas (Hukum Hooke): F_pegas = -kx
       → Tanda negatif karena berlawanan arah displacement
       
    2. Gaya redaman: F_redaman = -cv
       → Tanda negatif karena berlawanan arah gerak
       
    3. Gaya eksternal: F_ext = F(t)

Persamaan diferensial:
    m·x'' + c·x' + k·x = F(t)
    
Diubah ke sistem orde-1:
    x' = v           (kecepatan = turunan posisi)
    v' = (F - cv - kx) / m   (percepatan dari Newton II)
"""

def spring_ode(state, t, params, F_ext):
    x, v = state  # x = posisi (m), v = kecepatan (m/s)
    
    # Gaya eksternal F(t)
    F = F_ext(t) if F_ext else 0
    
    # ============================================
    # IMPLEMENTASI HUKUM HOOKE DAN NEWTON II
    # ============================================
    
    # dx/dt = v (definisi kecepatan)
    dxdt = v
    
    # dv/dt = a = (ΣF) / m
    # ΣF = F_ext - k*x - c*v
    # 
    # Penjelasan setiap komponen:
    #   F        → Gaya eksternal
    #   params.c * v → Gaya redaman (melawan gerak)
    #   params.k * x → GAYA PEGAS (Hukum Hooke: F = -kx)
    #   params.m     → Massa benda
    
    dvdt = (F - params.c * v - params.k * x) / params.m
    #       ↑        ↑              ↑              ↑
    #    F_ext   F_redaman    F_pegas(Hooke)    massa
    
    return [dxdt, dvdt]


# ============================================================
# BAGIAN 5: ENERGI DALAM SISTEM PEGAS
# ============================================================
"""
Energi mekanik dalam sistem pegas:

1. ENERGI KINETIK: KE = ½mv²
   → Energi karena gerak benda
   
2. ENERGI POTENSIAL PEGAS: PE = ½kx²
   → Energi tersimpan dalam pegas yang terdeformasi
   → Berasal dari integral gaya pegas: ∫F dx = ∫kx dx = ½kx²
   
3. ENERGI TOTAL: E = KE + PE
   → Untuk sistem tanpa redaman (c=0): E = konstan (konservasi energi)
   → Untuk sistem dengan redaman (c>0): E berkurang seiring waktu
"""

# Energi Kinetik: KE = ½mv²
KE = 0.5 * params.m * v**2

# Energi Potensial Pegas: PE = ½kx² (HUKUM HOOKE)
PE = 0.5 * params.k * x**2

# Energi Total
E_total = KE + PE


# ============================================================
# BAGIAN 6: SOLUSI ANALITIK UNTUK VALIDASI
# ============================================================
"""
Solusi analitik digunakan untuk memvalidasi solusi numerik.

UNDERDAMPED (0 < ζ < 1):
    x(t) = e^(-αt) [A·cos(ωd·t) + B·sin(ωd·t)]
    
    Dimana:
    - α = ζ·ωₙ (konstanta decay)
    - ωd = ωₙ·√(1-ζ²) (frekuensi teredam)
    
CRITICALLY DAMPED (ζ = 1):
    x(t) = e^(-ωₙ·t) (A + Bt)
    
OVERDAMPED (ζ > 1):
    x(t) = A·e^(r₁t) + B·e^(r₂t)
"""

# Underdamped case
omega_d = omega_n * np.sqrt(1 - zeta**2)  # Frekuensi teredam
alpha = zeta * omega_n                      # Konstanta decay

x = np.exp(-alpha * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))


# ============================================================
# BAGIAN 7: ANALISIS RESONANSI
# ============================================================
"""
Resonansi terjadi ketika frekuensi gaya paksa mendekati 
frekuensi natural sistem.

FUNGSI TRANSFER (normalized):
    |H(ω)| = 1 / √[(1-r²)² + (2ζr)²]
    
    Dimana r = ω/ωₙ (rasio frekuensi)

FREKUENSI RESONANSI:
    ω_res = ωₙ·√(1 - 2ζ²)  untuk ζ < 1/√2

QUALITY FACTOR:
    Q = 1/(2ζ)
    
BANDWIDTH (3dB):
    Δω = 2ζ·ωₙ
"""

r = omega / omega_n  # Rasio frekuensi
amplitude = 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)
