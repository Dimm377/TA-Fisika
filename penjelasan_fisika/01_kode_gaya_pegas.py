"""
SIMULASI GAYA PEGAS - HUKUM HOOKE
=================================
Tugas Akhir Fisika Komputasi
Tim: Dimas, Daffa, Dharma

File ini berisi implementasi dasar sistem massa-pegas
dengan penjelasan lengkap untuk keperluan pembelajaran.

Persamaan Gerak:
    m·x'' + c·x' + k·x = F(t)

Dimana:
    m = massa (kg)
    c = koefisien redaman (Ns/m)
    k = konstanta pegas (N/m)
    F(t) = gaya eksternal (N)
    x = posisi dari titik kesetimbangan (m)
"""

import numpy as np
from scipy.integrate import odeint
from typing import Callable, Optional, Dict
from dataclasses import dataclass


# ==============================================================================
# PARAMETER SISTEM
# ==============================================================================

@dataclass
class ParameterPegas:
    """
    Kelas untuk menyimpan parameter sistem massa-pegas.

    Attributes:
        massa: Massa benda (kg)
        konstanta_pegas: Konstanta pegas k (N/m) - kekakuan pegas
        koefisien_redaman: Koefisien redaman c (Ns/m) - hambatan gerak
        posisi_awal: Posisi awal x₀ dari titik kesetimbangan (m)
        kecepatan_awal: Kecepatan awal v₀ (m/s)
    """
    massa: float                # m (kg)
    konstanta_pegas: float      # k (N/m)
    koefisien_redaman: float    # c (Ns/m)
    posisi_awal: float          # x₀ (m)
    kecepatan_awal: float       # v₀ (m/s)

    @property
    def frekuensi_natural(self) -> float:
        """
        Menghitung frekuensi natural sistem (omega_n).

        Rumus: ωₙ = √(k/m)

        Interpretasi:
        - Frekuensi osilasi sistem TANPA redaman
        - Semakin besar k (pegas kaku) → osilasi semakin cepat
        - Semakin besar m (massa berat) → osilasi semakin lambat

        Returns:
            float: Frekuensi natural dalam rad/s
        """
        k = self.konstanta_pegas
        m = self.massa
        omega_n = np.sqrt(k / m)
        return omega_n

    @property
    def rasio_redaman(self) -> float:
        """
        Menghitung rasio redaman (zeta/ζ).

        Rumus: ζ = c / (2√(k·m))

        Interpretasi:
        - ζ = 0     : Tanpa redaman (osilasi terus selamanya)
        - 0 < ζ < 1 : Underdamped (osilasi teredam)
        - ζ = 1     : Critically damped (kembali tercepat tanpa osilasi)
        - ζ > 1     : Overdamped (kembali lambat tanpa osilasi)

        Returns:
            float: Rasio redaman (dimensionless)
        """
        c = self.koefisien_redaman
        k = self.konstanta_pegas
        m = self.massa

        redaman_kritis = 2 * np.sqrt(k * m)
        zeta = c / redaman_kritis
        return zeta


# ==============================================================================
# PERSAMAAN DIFERENSIAL (ODE)
# ==============================================================================

def persamaan_gerak_pegas(
    state: np.ndarray,
    waktu: float,
    params: ParameterPegas,
    gaya_eksternal: Optional[Callable[[float], float]] = None
) -> list:
    """
    Persamaan gerak sistem massa-pegas (ODE).

    Persamaan dasar dari Hukum Newton II dan Hukum Hooke:
        m·a = ΣF = F_eksternal - F_pegas - F_redaman
        m·x'' = F(t) - k·x - c·x'

    Diubah ke sistem ODE orde-1:
        dx/dt = v           (definisi kecepatan)
        dv/dt = (F - c·v - k·x) / m

    Args:
        state: Array [posisi, kecepatan] saat ini
        waktu: Waktu t dalam detik
        params: Parameter sistem (m, k, c, dst)
        gaya_eksternal: Fungsi F(t) untuk gaya luar (opsional)

    Returns:
        list: [dx/dt, dv/dt] - turunan posisi dan kecepatan
    """
    # Unpack state saat ini
    posisi = state[0]     # x (m)
    kecepatan = state[1]  # v (m/s)

    # Hitung gaya eksternal (jika ada)
    F_eksternal = gaya_eksternal(waktu) if gaya_eksternal else 0

    # ========================================
    # HITUNG GAYA-GAYA YANG BEKERJA
    # ========================================

    # 1. Gaya Pegas (Hukum Hooke): F = -k·x
    #    Tanda negatif = selalu melawan displacement
    F_pegas = -params.konstanta_pegas * posisi

    # 2. Gaya Redaman: F = -c·v
    #    Tanda negatif = selalu melawan arah gerak
    F_redaman = -params.koefisien_redaman * kecepatan

    # ========================================
    # HUKUM NEWTON II: ΣF = m·a
    # ========================================

    # Total gaya = F_eksternal + F_pegas + F_redaman
    gaya_total = F_eksternal + F_pegas + F_redaman

    # Percepatan = F / m
    percepatan = gaya_total / params.massa

    # ========================================
    # RETURN TURUNAN
    # ========================================

    dx_dt = kecepatan    # Turunan posisi = kecepatan
    dv_dt = percepatan   # Turunan kecepatan = percepatan

    return [dx_dt, dv_dt]


# ==============================================================================
# SOLVER (PENYELESAI PERSAMAAN)
# ==============================================================================

def simulasi_pegas(
    params: ParameterPegas,
    durasi: float = 10.0,
    jumlah_titik: int = 1000,
    gaya_eksternal: Optional[Callable[[float], float]] = None
) -> Dict[str, np.ndarray]:
    """
    Menjalankan simulasi sistem massa-pegas.

    Menggunakan scipy.odeint (metode numerik) untuk menyelesaikan
    persamaan diferensial biasa (ODE).

    Args:
        params: Parameter sistem pegas
        durasi: Durasi simulasi dalam detik
        jumlah_titik: Jumlah titik data yang dihasilkan
        gaya_eksternal: Fungsi gaya luar F(t) (opsional)

    Returns:
        dict: Dictionary berisi:
            - 't': Array waktu
            - 'x': Array posisi
            - 'v': Array kecepatan
            - 'KE': Energi kinetik (½mv²)
            - 'PE': Energi potensial pegas (½kx²)
            - 'E_total': Energi total (KE + PE)

    Contoh penggunaan:
        >>> params = ParameterPegas(massa=1.0, konstanta_pegas=100,
        ...                         koefisien_redaman=2, posisi_awal=0.5,
        ...                         kecepatan_awal=0)
        >>> hasil = simulasi_pegas(params, durasi=10)
        >>> print(f"Posisi maksimum: {hasil['x'].max():.3f} m")
    """
    # Buat array waktu
    waktu = np.linspace(0, durasi, jumlah_titik)

    # Kondisi awal [x₀, v₀]
    kondisi_awal = [params.posisi_awal, params.kecepatan_awal]

    # Selesaikan ODE menggunakan odeint
    solusi = odeint(
        func=persamaan_gerak_pegas,
        y0=kondisi_awal,
        t=waktu,
        args=(params, gaya_eksternal)
    )

    # Extract hasil
    posisi = solusi[:, 0]     # Kolom pertama = posisi
    kecepatan = solusi[:, 1]  # Kolom kedua = kecepatan

    # ========================================
    # HITUNG ENERGI
    # ========================================

    # Energi Kinetik: KE = ½mv²
    # Energi karena GERAK benda
    energi_kinetik = 0.5 * params.massa * kecepatan**2

    # Energi Potensial: PE = ½kx²
    # Energi yang TERSIMPAN dalam pegas terdeformasi
    # (Berasal dari integral gaya Hooke: ∫kx dx = ½kx²)
    energi_potensial = 0.5 * params.konstanta_pegas * posisi**2

    # Energi Total = KE + PE
    # Untuk sistem tanpa redaman: E_total = KONSTAN (konservasi energi)
    # Untuk sistem dengan redaman: E_total BERKURANG seiring waktu
    energi_total = energi_kinetik + energi_potensial

    return {
        't': waktu,
        'x': posisi,
        'v': kecepatan,
        'KE': energi_kinetik,
        'PE': energi_potensial,
        'E_total': energi_total
    }


# ==============================================================================
# RINGKASAN RUMUS UTAMA
# ==============================================================================
"""
RUMUS-RUMUS PENTING:

1. HUKUM HOOKE (Gaya Pegas):
   F = -k·x
   - k = konstanta pegas (N/m)
   - x = displacement dari posisi kesetimbangan (m)
   - Tanda negatif = gaya selalu menuju kesetimbangan

2. PERSAMAAN GERAK (Newton II + Hooke + Redaman):
   m·x'' + c·x' + k·x = F(t)

3. FREKUENSI NATURAL:
   ωₙ = √(k/m)

4. RASIO REDAMAN:
   ζ = c / (2√(k·m))

5. ENERGI KINETIK:
   KE = ½·m·v²

6. ENERGI POTENSIAL PEGAS:
   PE = ½·k·x²

7. KONSERVASI ENERGI (tanpa redaman):
   E_total = KE + PE = konstan
"""


# ==============================================================================
# CONTOH PENGGUNAAN
# ==============================================================================

if __name__ == "__main__":
    # Buat parameter sistem
    pegas = ParameterPegas(
        massa=1.0,              # 1 kg
        konstanta_pegas=100,    # 100 N/m
        koefisien_redaman=2,    # 2 Ns/m (underdamped)
        posisi_awal=0.5,        # 50 cm dari kesetimbangan
        kecepatan_awal=0        # Diam di awal
    )

    # Tampilkan karakteristik sistem
    print("=== KARAKTERISTIK SISTEM ===")
    print(f"Frekuensi natural (ωₙ): {pegas.frekuensi_natural:.2f} rad/s")
    print(f"Rasio redaman (ζ): {pegas.rasio_redaman:.3f}")

    if pegas.rasio_redaman == 0:
        print("Tipe: Tanpa Redaman (osilasi terus)")
    elif pegas.rasio_redaman < 1:
        print("Tipe: Underdamped (osilasi teredam)")
    elif pegas.rasio_redaman == 1:
        print("Tipe: Critically Damped")
    else:
        print("Tipe: Overdamped")

    # Jalankan simulasi
    hasil = simulasi_pegas(pegas, durasi=10)

    print(f"\n=== HASIL SIMULASI ===")
    print(f"Posisi maksimum: {hasil['x'].max():.4f} m")
    print(f"Kecepatan maksimum: {abs(hasil['v']).max():.4f} m/s")
    print(f"Energi awal: {hasil['E_total'][0]:.4f} J")
    print(f"Energi akhir: {hasil['E_total'][-1]:.4f} J")
