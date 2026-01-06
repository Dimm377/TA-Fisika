"""
SIMULASI GAYA PEGAS - HUKUM HOOKE
=================================
Tugas Akhir Fisika Komputasi
File ini berisi implementasi inti sistem massa-pegas.
"""

import numpy as np
from scipy.integrate import odeint
from typing import Callable, Optional, Dict
from dataclasses import dataclass


# ==============================================================================
# 1. DEFINISI PARAMETER
# ==============================================================================

@dataclass
class ParameterPegas:
    """Menyimpan konstanta fisik sistem."""
    massa: float                # kg
    konstanta_pegas: float      # N/m
    koefisien_redaman: float    # Ns/m
    posisi_awal: float          # m
    kecepatan_awal: float       # m/s

    @property
    def frekuensi_natural(self) -> float:
        """ωn = √(k/m)"""
        return np.sqrt(self.konstanta_pegas / self.massa)

    @property
    def rasio_redaman(self) -> float:
        """ζ = c / (2√(km))"""
        redaman_kritis = 2 * np.sqrt(self.konstanta_pegas * self.massa)
        return self.koefisien_redaman / redaman_kritis

    @property
    def periode(self) -> float:
        """T = 2π / ωd (Hanya untuk underdamped)"""
        zeta = self.rasio_redaman
        if zeta >= 1.0:
            return float('inf')
        omega_d = self.frekuensi_natural * np.sqrt(1 - zeta**2)
        return 2 * np.pi / omega_d


# ==============================================================================
# 2. PERSAMAAN GERAK (PHYSICS ENGINE)
# ==============================================================================

def hitung_derivatif(state: np.ndarray, t: float, params: ParameterPegas) -> list:
    """
    Menghitung turunan posisi (kecepatan) dan turunan kecepatan (percepatan).

    Persamaan: m·x'' + c·x' + k·x = 0
    Sehingga:  x'' = (-k·x - c·x') / m
    """
    posisi, kecepatan = state

    # Hitung gaya-gaya komponen
    gaya_pegas = -params.konstanta_pegas * posisi
    gaya_redaman = -params.koefisien_redaman * kecepatan

    # Hukum Newton II: a = ΣF / m
    gaya_total = gaya_pegas + gaya_redaman
    percepatan = gaya_total / params.massa

    return [kecepatan, percepatan]


# ==============================================================================
# 3. SOLVER NUMERIK
# ==============================================================================

def jalankan_simulasi(params: ParameterPegas, durasi: float) -> Dict[str, np.ndarray]:
    """Menyelesaikan persamaan diferensial menggunakan odeint (LSODA solver)."""

    # Setup waktu (sampling rate tinggi untuk akurasi)
    t = np.linspace(0, durasi, 1000)

    # Kondisi awal sistem [x0, v0]
    initial_state = [params.posisi_awal, params.kecepatan_awal]

    # PROSES UTAMA: Integrasi numerik
    solusi = odeint(hitung_derivatif, initial_state, t, args=(params,))

    # Ekstrak hasil
    x = solusi[:, 0]  # Posisi
    v = solusi[:, 1]  # Kecepatan

    return hitung_energi(t, x, v, params)


def hitung_energi(t, x, v, params) -> Dict:
    """Menghitung konservasi energi sistem."""
    dt = t[1] - t[0]

    KE = 0.5 * params.massa * v**2              # Energi Kinetik
    PE = 0.5 * params.konstanta_pegas * x**2    # Energi Potensial

    # Hitung energi yang hilang karena gesekan (Dissipated Energy)
    # E_dissipasi = ∫(c·v²) dt
    daya_disipasi = params.koefisien_redaman * v**2
    E_disipasi = np.cumsum(daya_disipasi * dt)  # Integral kumulatif

    return {
        't': t, 'x': x, 'v': v,
        'KE': KE, 'PE': PE,
        'E_total': KE + PE,
        'E_disipasi': E_disipasi
    }


# ==============================================================================
# 4. DEMO / PENGUJIAN
# ==============================================================================

if __name__ == "__main__":
    # Contoh kasus: Sistem Underdamped (berosilasi lalu berhenti)
    sistem = ParameterPegas(
        massa=1.0,
        konstanta_pegas=100,
        koefisien_redaman=2,
        posisi_awal=0.5,
        kecepatan_awal=0
    )

    hasil = jalankan_simulasi(sistem, durasi=5.0)

    print(f"=== SIMULASI SELESAI ===")
    print(f"Sistem: {sistem.massa}kg, {sistem.konstanta_pegas}N/m")
    print(f"Frekuensi Natural: {sistem.frekuensi_natural:.2f} rad/s")
    print(f"Posisi Akhir: {hasil['x'][-1]:.4f} m (Mendekati 0)")

    # Cek kekekalan energi
    E_awal = hasil['E_total'][0]
    E_akhir = hasil['E_total'][-1] + hasil['E_disipasi'][-1]

    print(f"Energi Awal: {E_awal:.4f} J")
    print(f"Energi Akhir (Mekanik + Panas): {E_akhir:.4f} J")
    print(f"Status: {'✅ Valid' if np.isclose(E_awal, E_akhir, rtol=1e-2) else '❌ Error'}")
