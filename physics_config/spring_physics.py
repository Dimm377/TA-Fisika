"""
 Simulasi Gaya Pegas - Hooke's Law
====================================
Tugas Akhir Fisika Komputasi

Model Fisika:
    m·x'' + c·x' + k·x = F(t)

Dimana:
    m = massa (kg)
    c = koefisien redaman (Ns/m)
    k = konstanta pegas (N/m)
    F(t) = gaya eksternal (N)
    x = posisi (m)

Author: Dimas, Daffa, Dharma
"""

import numpy as np
from scipy.integrate import odeint
from dataclasses import dataclass
from typing import Callable, Tuple, Optional

from enum import Enum


class DampingType(Enum):
    """Klasifikasi sistem berdasarkan rasio redaman"""
    UNDAMPED = "Tanpa Redaman"
    UNDERDAMPED = "Underdamped"
    CRITICALLY_DAMPED = "Critically Damped"
    OVERDAMPED = "Overdamped"


@dataclass
class SpringParameters:
    """Parameter sistem massa-pegas"""
    m: float      # Massa (kg)
    k: float      # Konstanta pegas (N/m)
    c: float      # Koefisien redaman (Ns/m)
    x0: float     # Posisi awal (m)
    v0: float     # Kecepatan awal (m/s)
    name: str = "Custom"
    description: str = ""

    @property
    def omega_n(self) -> float:
        """
        Frekuensi natural (rad/s)

        FISIKA: omega_n = sqrt(k/m)
        - Ini adalah frekuensi osilasi sistem tanpa redaman
        - Semakin besar k (pegas kaku), semakin cepat osilasi
        - Semakin besar m (massa berat), semakin lambat osilasi
        """
        # Rumus: ω_n = √(k/m) - frekuensi natural sistem
        return np.sqrt(self.k / self.m)

    @property
    def zeta(self) -> float:
        """
        Rasio Redaman (Damping Ratio) - ζ

        Menentukan seberapa kuat sistem diredam relatif terhadap redaman kritis.

        LOGIKA FISIKA:
        - ζ = 0   : Tidak ada redaman (Osilasi selamanya)
        - 0 < ζ < 1 : Underdamped (Osilasi lalu perlahan berhenti)
        - ζ = 1   : Critically Damped (Berhenti paling cepat tanpa bablas)
        - ζ > 1   : Overdamped (Kembali ke posisi 0 dengan lambat)
        """
        # Rumus Fisika: ζ = c / (2 * sqrt(k * m))
        return self.c / (2 * np.sqrt(self.k * self.m))

    @property
    def period(self) -> float:
        """Periode osilasi (s)"""
        # Near-critically damped dan overdamped tidak berosilasi
        if self.zeta >= 0.9:
            return float('inf')
        omega_d = self.omega_n * np.sqrt(1 - self.zeta**2)
        return 2 * np.pi / omega_d

    @property
    def damping_type(self) -> DampingType:
        """Klasifikasi tipe redaman"""
        if self.c == 0:
            return DampingType.UNDAMPED
        elif np.isclose(self.zeta, 1, rtol=0.1):  # zeta 0.9 - 1.1 = critically damped
            return DampingType.CRITICALLY_DAMPED
        elif self.zeta < 1:
            return DampingType.UNDERDAMPED
        else:
            return DampingType.OVERDAMPED


# ============================================================
# PRESET REAL-LIFE
# ============================================================

PRESETS = {
    "car_suspension": SpringParameters(
        m=400,         # 1/4 massa mobil (kg)
        k=40000,       # Konstanta pegas suspensi (N/m)
        c=7200,        # Koefisien redaman shock absorber (Ns/m) - untuk zeta ~ 0.9
        x0=0.05,       # Displacement awal 5cm
        v0=0,
        name=" Suspensi Mobil",
        description="Suspensi mobil sedan. Dirancang near-critically damped untuk kenyamanan."
    ),
    "trampoline": SpringParameters(
        m= 15,          # Massa orang dewasa (kg)
        k=5000,        # Konstanta pegas trampolin (N/m)
        c=100,         # Redaman kecil untuk bouncing (Ns/m)
        x0=0.3,        # Defleksi 30cm
        v0=-2,         # Kecepatan jatuh (m/s)
        name=" Trampolin",
        description="Trampolin rekreasi. Underdamped untuk efek memantul."
    ),
    "lab_spring": SpringParameters(
        m=0.5,         # Massa beban (kg)
        k=20,          # Pegas lab standar (N/m)
        c=0.1,         # Redaman minimal (Ns/m)
        x0=0.1,        # Tarik 10cm
        v0=0,
        name=" Pegas Laboratorium",
        description="Pegas heliks standar untuk praktikum fisika dasar."
    ),
    "spring_mass": SpringParameters(
        m=1.0,         # Massa standar (kg)
        k=100,         # Konstanta pegas standar (N/m)
        c=2,           # Redaman kecil (Ns/m)
        x0=0.2,        # Displacement awal 20cm
        v0=0,          # Diam dari posisi ditarik
        name="️ Sistem Pegas-Massa",
        description="Sistem pegas-massa ideal untuk demonstrasi hukum Hooke dan osilasi harmonik."
    ),
    "door_closer": SpringParameters(
        m=5,           # Massa efektif pintu (kg)
        k=50,          # Konstanta pegas (N/m)
        c=50,          # Redaman tinggi (Ns/m) - c > 2*sqrt(k*m) = 31.6 untuk overdamped
        x0=1.0,        # Sudut buka (dianalogikan)
        v0=0,
        name=" Door Closer",
        description="Mekanisme penutup pintu otomatis. Overdamped untuk menutup pelan."
    ),
}


# ============================================================
# PHYSICS CALCULATIONS
# ============================================================

def calculate_spring_force(spring_constant: float, displacement: float) -> float:
    """
    HUKUM HOOKE (Gaya Pegas)

    Rumus: F = -k * x

    Keterangan:
    - Gaya selalu berlawanan arah dengan perpindahan (tanda negatif).
    - Semakin jauh ditarik (x besar), semakin kuat pegas menarik balik.
    """
    return -spring_constant * displacement


def calculate_damping_force(damping_coefficient: float, velocity: float) -> float:
    """
    GAYA REDAMAN (Damping Force)

    Rumus: F = -c * v

    Keterangan:
    - Gaya gesek yang menghambat gerakan benda.
    - Semakin cepat bergerak (v besar), semakin kuat hambatannya.
    - Selalu berlawanan arah dengan kecepatan (tanda negatif).
    """
    return -damping_coefficient * velocity


def calculate_net_force(spring_constant: float, damping_coefficient: float,
                        displacement: float, velocity: float,
                        external_force: float = 0) -> float:
    """Sum of all forces acting on the mass"""
    spring = calculate_spring_force(spring_constant, displacement)
    damping = calculate_damping_force(damping_coefficient, velocity)
    return external_force + spring + damping


def calculate_acceleration(mass: float, net_force: float) -> float:
    """
    HUKUM II NEWTON

    Rumus: a = F_total / m

    Keterangan:
    - Percepatan benda sebanding dengan total gaya yang bekerja.
    - Berbanding terbalik dengan massa benda.
    """
    return net_force / mass


# ============================================================
# ODE SOLVER
# ============================================================

def spring_system_derivatives(state: np.ndarray, time: float,
                              params: SpringParameters,
                              external_force_function: Optional[Callable] = None) -> np.ndarray:
    """
    Fungsi Utama ODE Solver (Jantung Simulasi)

    Fungsi ini menghitung perubahan state (posisi & kecepatan) pada setiap detik.

    Input:
      - state: [posisi saat ini, kecepatan saat ini]

    Output:
      - derivatives: [kecepatan, percepatan]

    Konsep:
    1. Ambil posisi & kecepatan saat ini.
    2. Hitung semua gaya (Pegas + Redaman + Eksternal).
    3. Cari percepatan pakai Hukum Newton (a = F/m).
    4. Kembalikan [v, a] agar ODE solver bisa memprediksi langkah selanjutnya.
    """
    position, velocity = state

    external_force = external_force_function(time) if external_force_function else 0

    # Hitung Total Gaya (Sigma F)
    net_force = calculate_net_force(
        spring_constant=params.k,
        damping_coefficient=params.c,
        displacement=position,
        velocity=velocity,
        external_force=external_force
    )

    # Hitung Percepatan (a)
    acceleration = calculate_acceleration(params.m, net_force)

    return np.array([velocity, acceleration])


def solve_spring_system(params: SpringParameters,
                        time_span: Tuple[float, float],
                        time_step: float = 0.001,
                        external_force_function: Optional[Callable] = None) -> dict:
    """
    Menyelesaikan Sistem Persamaan Diferensial (Solving ODE)

    Fungsi ini melakukan simulasi numerik dari waktu ke waktu.

    Output (Dictionary):
    - t: Array waktu
    - x: Array posisi
    - v: Array kecepatan
    - a: Array percepatan
    - KE, PE, E_total: Data energi
    """
    time_array = np.arange(time_span[0], time_span[1], time_step)
    initial_state = [params.x0, params.v0]

    # Solve differential equation
    solution = odeint(
        spring_system_derivatives,
        initial_state,
        time_array,
        args=(params, external_force_function)
    )

    position = solution[:, 0]
    velocity = solution[:, 1]

    # Calculate acceleration at each time point
    acceleration = calculate_acceleration_array(
        params, time_array, position, velocity, external_force_function
    )

    # Calculate energies
    kinetic_energy = calculate_kinetic_energy(params.m, velocity)
    potential_energy = calculate_potential_energy(params.k, position)
    total_energy = kinetic_energy + potential_energy
    dissipated_energy = calculate_dissipated_energy(params.c, velocity, time_step)

    return {
        't': time_array,
        'x': position,
        'v': velocity,
        'a': acceleration,
        'KE': kinetic_energy,
        'PE': potential_energy,
        'E_total': total_energy,
        'E_dissipated': dissipated_energy,
        'params': params
    }


def calculate_acceleration_array(params: SpringParameters, time_array: np.ndarray,
                                 position: np.ndarray, velocity: np.ndarray,
                                 external_force_function: Optional[Callable] = None) -> np.ndarray:
    """Calculate acceleration at each time point"""
    acceleration = np.zeros_like(time_array)

    for i, t in enumerate(time_array):
        external_force = external_force_function(t) if external_force_function else 0
        net_force = calculate_net_force(
            params.k, params.c, position[i], velocity[i], external_force
        )
        acceleration[i] = calculate_acceleration(params.m, net_force)

    return acceleration


def calculate_kinetic_energy(mass: float, velocity: np.ndarray) -> np.ndarray:
    """KE = ½mv²"""
    return 0.5 * mass * velocity**2


def calculate_potential_energy(spring_constant: float, displacement: np.ndarray) -> np.ndarray:
    """PE = ½kx² (Hooke's Law energy)"""
    return 0.5 * spring_constant * displacement**2


def calculate_dissipated_energy(damping_coefficient: float, velocity: np.ndarray,
                                time_step: float) -> np.ndarray:
    """Energy lost to damping over time"""
    dissipated = np.zeros_like(velocity)

    for i in range(1, len(velocity)):
        power_dissipated = damping_coefficient * velocity[i]**2
        dissipated[i] = dissipated[i - 1] + power_dissipated * time_step

    return dissipated


# ============================================================
# GAYA EKSTERNAL PRESETS
# ============================================================

def no_force(t: float) -> float:
    """Tanpa gaya eksternal"""
    return 0


def step_force(amplitude: float = 10, t_start: float = 1) -> Callable:
    """Gaya step (tiba-tiba diterapkan)"""
    def F(t):
        return amplitude if t >= t_start else 0
    return F


def harmonic_force(amplitude: float = 10, omega: float = 5) -> Callable:
    """Gaya harmonik (sinusoidal)"""
    def F(t):
        return amplitude * np.sin(omega * t)
    return F


def impulse_force(amplitude: float = 100, t_center: float = 1, width: float = 0.1) -> Callable:
    """Gaya impuls (Gaussian pulse)"""
    def F(t):
        return amplitude * np.exp(-((t - t_center) / width)**2)
    return F


# ============================================================
# PHYSICS EXPLANATION
# ============================================================

PHYSICS_EXPLANATION = """
##  Model Fisika

### Persamaan Gerak

Sistem massa-pegas dengan redaman dideskripsikan oleh persamaan diferensial orde-2:

$$m\\ddot{x} + c\\dot{x} + kx = F(t)$$

**Komponen gaya:**
- $-kx$: Gaya pegas (Hooke's Law) - restoring force
- $-c\\dot{x}$: Gaya redaman - proporsional kecepatan
- $F(t)$: Gaya eksternal

### Frekuensi Natural

$$\\omega_n = \\sqrt{\\frac{k}{m}}$$

Frekuensi ini menentukan seberapa cepat sistem berosilasi tanpa redaman.

### Rasio Redaman (Damping Ratio)

$$\\zeta = \\frac{c}{2\\sqrt{km}}$$

| Nilai ζ | Tipe | Perilaku |
|---------|------|----------|
| ζ = 0 | Undamped | Osilasi terus tanpa berhenti |
| 0 < ζ < 1 | Underdamped | Osilasi teredam |
| ζ = 1 | Critically Damped | Kembali tercepat tanpa osilasi |
| ζ > 1 | Overdamped | Kembali lambat tanpa osilasi |

### Energi Sistem

- **Energi Kinetik**: $KE = \\frac{1}{2}mv^2$
- **Energi Potensial**: $PE = \\frac{1}{2}kx^2$
- **Disipasi**: $P_{diss} = c v^2$ (daya yang hilang)

Untuk sistem tanpa redaman, $E_{total} = KE + PE = konstan$
"""


# ============================================================
# SOLUSI ANALITIK (UNTUK VALIDASI NUMERIK)
# ============================================================

def analytical_solution(params: SpringParameters, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Solusi analitik untuk osilator harmonik teredam (tanpa gaya eksternal).

    Digunakan untuk memvalidasi akurasi metode numerik.

    Returns:
    --------
    (x_analytical, v_analytical) - tuple array posisi dan kecepatan
    """
    omega_n = params.omega_n
    zeta = params.zeta
    x0 = params.x0
    v0 = params.v0

    if params.c == 0:  # Undamped
        # x(t) = A*cos(ωt) + B*sin(ωt)
        A = x0
        B = v0 / omega_n
        x = A * np.cos(omega_n * t) + B * np.sin(omega_n * t)
        v = -A * omega_n * np.sin(omega_n * t) + B * omega_n * np.cos(omega_n * t)

    elif zeta < 1:  # Underdamped
        omega_d = omega_n * np.sqrt(1 - zeta**2)  # Damped frequency
        alpha = zeta * omega_n

        A = x0
        B = (v0 + alpha * x0) / omega_d

        x = np.exp(-alpha * t) * (A * np.cos(omega_d * t) + B * np.sin(omega_d * t))
        v = np.exp(-alpha * t) * (
            (-alpha * A + omega_d * B) * np.cos(omega_d * t)
            + (-alpha * B - omega_d * A) * np.sin(omega_d * t)
        )

    elif np.isclose(zeta, 1, rtol=0.1):  # Critically damped (zeta 0.9 - 1.1)
        A = x0
        B = v0 + omega_n * x0

        x = np.exp(-omega_n * t) * (A + B * t)
        v = np.exp(-omega_n * t) * (B - omega_n * (A + B * t))

    else:  # Overdamped
        r1 = -omega_n * (zeta + np.sqrt(zeta**2 - 1))
        r2 = -omega_n * (zeta - np.sqrt(zeta**2 - 1))

        A = (r2 * x0 - v0) / (r2 - r1)
        B = (v0 - r1 * x0) / (r2 - r1)

        x = A * np.exp(r1 * t) + B * np.exp(r2 * t)
        v = A * r1 * np.exp(r1 * t) + B * r2 * np.exp(r2 * t)

    return x, v


def validate_numerical_solution(solution: dict) -> dict:
    """
    Validasi solusi numerik dengan membandingkan ke solusi analitik.

    Returns:
    --------
    dict dengan metrik error:
        - max_error: Error maksimum posisi
        - rms_error: Root Mean Square error
        - relative_error: Error relatif rata-rata
        - correlation: Korelasi antara numerik dan analitik
    """
    params = solution['params']
    t = solution['t']
    x_numerical = solution['x']

    # Dapatkan solusi analitik
    x_analytical, _ = analytical_solution(params, t)

    # Hitung berbagai metrik error
    error = x_numerical - x_analytical
    max_error = np.max(np.abs(error))
    rms_error = np.sqrt(np.mean(error**2))

    # Relative error (hindari division by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_error = np.abs(error) / np.abs(x_analytical)
        rel_error = np.nan_to_num(rel_error, nan=0, posinf=0, neginf=0)
    relative_error = np.mean(rel_error) * 100  # Dalam persen

    # Korelasi
    correlation = np.corrcoef(x_numerical, x_analytical)[0, 1]

    return {
        'x_analytical': x_analytical,
        'max_error': max_error,
        'rms_error': rms_error,
        'relative_error': relative_error,
        'correlation': correlation,
        'is_accurate': rms_error < 0.01 * np.max(np.abs(x_analytical))
    }


# ============================================================
# ANALISIS FREKUENSI (FFT)
# ============================================================

def frequency_analysis(solution: dict) -> dict:
    """
    Analisis frekuensi menggunakan Fast Fourier Transform.

    Berguna untuk mengidentifikasi frekuensi dominan dalam sistem
    dan memvalidasi frekuensi natural teoritis.

    Returns:
    --------
    dict dengan:
        - frequencies: array frekuensi (Hz)
        - amplitudes: amplitudo spektrum
        - dominant_freq: frekuensi dominan (Hz)
        - theoretical_freq: frekuensi teoritis (Hz)
        - freq_error: perbedaan (%)
    """
    t = solution['t']
    x = solution['x']
    params = solution['params']

    # Sampling parameters
    dt = t[1] - t[0]
    N = len(t)

    # FFT
    fft_result = np.fft.fft(x)
    frequencies = np.fft.fftfreq(N, dt)
    amplitudes = np.abs(fft_result) / N * 2  # Normalize

    # Hanya ambil frekuensi positif
    positive_mask = frequencies > 0
    frequencies = frequencies[positive_mask]
    amplitudes = amplitudes[positive_mask]

    # Frekuensi dominan
    dominant_idx = np.argmax(amplitudes)
    dominant_freq = frequencies[dominant_idx]

    # Frekuensi teoritis - hanya untuk underdamped (zeta < 0.9)
    if params.zeta < 0.9:
        omega_d = params.omega_n * np.sqrt(1 - params.zeta**2)
        theoretical_freq = omega_d / (2 * np.pi)
    else:
        theoretical_freq = 0  # Near-critical dan overdamped tidak berosilasi

    # Error
    if theoretical_freq > 0:
        freq_error = abs(dominant_freq - theoretical_freq) / theoretical_freq * 100
    else:
        freq_error = 0

    return {
        'frequencies': frequencies,
        'amplitudes': amplitudes,
        'dominant_freq': dominant_freq,
        'theoretical_freq': theoretical_freq,
        'freq_error': freq_error
    }


# ============================================================
# ANALISIS RESONANSI
# ============================================================

def resonance_analysis(params: SpringParameters,
                       omega_range: Optional[Tuple[float, float]] = None,
                       n_points: int = 100) -> dict:
    """
    Analisis respons frekuensi untuk menentukan kurva resonansi.

    Menghitung amplitudo steady-state sebagai fungsi frekuensi driving.

    Returns:
    --------
    dict dengan:
        - omega: array frekuensi driving (rad/s)
        - amplitude: amplitudo respons
        - resonance_omega: frekuensi resonansi
        - Q_factor: Quality factor
        - bandwidth: lebar bandwidth 3dB
    """
    omega_n = params.omega_n
    zeta = params.zeta

    # Default range: 0.1 to 3x natural frequency
    if omega_range is None:
        omega_range = (0.1 * omega_n, 3 * omega_n)

    omega = np.linspace(omega_range[0], omega_range[1], n_points)

    # Amplitudo respons (normalized)
    # |H(ω)| = 1 / sqrt((1 - r²)² + (2ζr)²) where r = ω/ωn
    r = omega / omega_n
    amplitude = 1 / np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2)

    # Frekuensi resonansi
    if zeta < 1 / np.sqrt(2):
        resonance_omega = omega_n * np.sqrt(1 - 2 * zeta**2)
    else:
        resonance_omega = 0  # No resonance peak

    # Quality factor
    if zeta > 0:
        Q_factor = 1 / (2 * zeta)
    else:
        Q_factor = float('inf')

    # Bandwidth (3dB)
    bandwidth = 2 * zeta * omega_n

    return {
        'omega': omega,
        'amplitude': amplitude,
        'resonance_omega': resonance_omega,
        'Q_factor': Q_factor,
        'bandwidth': bandwidth
    }


# ============================================================
# KESIMPULAN OTOMATIS
# ============================================================

def generate_conclusions(solution: dict, validation: Optional[dict] = None,
                         fft_result: Optional[dict] = None) -> str:
    """
    Generate kesimpulan ilmiah otomatis berdasarkan hasil simulasi.

    Returns:
    --------
    str - Kesimpulan dalam format markdown
    """
    params = solution['params']
    # t = solution['t']  # Unused
    x = solution['x']
    # v = solution['v']  # Unused
    E_total = solution['E_total']

    conclusions = []

    # 1. Karakteristik Sistem
    conclusions.append("##  Kesimpulan Analisis")
    conclusions.append("")
    conclusions.append("### 1. Karakteristik Sistem")
    conclusions.append(f"- **Tipe sistem**: {params.damping_type.value}")
    conclusions.append(f"- **Frekuensi natural (ωₙ)**: {params.omega_n:.4f} rad/s")
    conclusions.append(f"- **Rasio redaman (ζ)**: {params.zeta:.4f}")

    if params.zeta < 1:
        omega_d = params.omega_n * np.sqrt(1 - params.zeta**2)
        conclusions.append(f"- **Frekuensi teredam (ωd)**: {omega_d:.4f} rad/s")
        conclusions.append(f"- **Periode osilasi**: {params.period:.4f} s")

    # 2. Perilaku Dinamis
    conclusions.append("")
    conclusions.append("### 2. Perilaku Dinamis")

    x_max = np.max(np.abs(x))
    # v_max = np.max(np.abs(v))  # Unused

    if params.damping_type == DampingType.UNDAMPED:
        conclusions.append(f"- Sistem berosilasi dengan amplitudo konstan **{x_max:.4f} m**")
        conclusions.append("- Tidak ada kehilangan energi (konservasi energi)")
    elif params.damping_type == DampingType.UNDERDAMPED:
        # Hitung decay rate
        decay_time = 1 / (params.zeta * params.omega_n)
        conclusions.append(f"- Amplitudo awal: **{abs(params.x0):.4f} m**")
        conclusions.append(f"- Konstanta waktu decay (τ): **{decay_time:.4f} s**")
        conclusions.append(f"- Sistem mencapai ~37% amplitudo awal setelah **{decay_time:.2f} s**")
    elif params.damping_type == DampingType.CRITICALLY_DAMPED:
        conclusions.append("- Sistem kembali ke equilibrium **secepat mungkin tanpa osilasi**")
        conclusions.append("- Ini adalah kondisi optimal untuk sistem kontrol")
    else:  # Overdamped
        conclusions.append("- Sistem kembali ke equilibrium **sangat lambat tanpa osilasi**")
        conclusions.append("- Cocok untuk aplikasi yang membutuhkan gerakan halus")

    # 3. Analisis Energi
    conclusions.append("")
    conclusions.append("### 3. Analisis Energi")

    E_initial = E_total[0]
    E_final = E_total[-1]
    energy_loss = (E_initial - E_final) / E_initial * 100

    conclusions.append(f"- Energi awal: **{E_initial:.6f} J**")
    conclusions.append(f"- Energi akhir: **{E_final:.6f} J**")
    conclusions.append(f"- Energi terdisipasi: **{energy_loss:.2f}%**")

    if energy_loss < 1:
        conclusions.append("-  Sistem mendekati **konservasi energi** (losses < 1%)")
    elif energy_loss < 50:
        conclusions.append("- ️ Terjadi **disipasi energi moderat** akibat redaman")
    else:
        conclusions.append("-  Terjadi **disipasi energi signifikan** (sistem heavily damped)")

    # 4. Validasi Numerik (jika tersedia)
    if validation:
        conclusions.append("")
        conclusions.append("### 4. Validasi Numerik")
        conclusions.append(f"- Max error vs analitik: **{validation['max_error']:.2e} m**")
        conclusions.append(f"- RMS error: **{validation['rms_error']:.2e} m**")
        conclusions.append(f"- Korelasi: **{validation['correlation']:.6f}**")

        if validation['is_accurate']:
            conclusions.append("-  Solusi numerik **tervalidasi akurat**")
        else:
            conclusions.append("- ️ Error numerik melebihi toleransi, pertimbangkan dt lebih kecil")

    # 5. Analisis Frekuensi (jika tersedia)
    if fft_result and params.zeta < 1:
        conclusions.append("")
        conclusions.append("### 5. Analisis Spektral")
        conclusions.append(f"- Frekuensi dominan (FFT): **{fft_result['dominant_freq']:.4f} Hz**")
        conclusions.append(f"- Frekuensi teoritis: **{fft_result['theoretical_freq']:.4f} Hz**")
        conclusions.append(f"- Perbedaan: **{fft_result['freq_error']:.2f}%**")

        if fft_result['freq_error'] < 5:
            conclusions.append("-  FFT **konsisten** dengan teori")

    # 6. Implikasi Praktis
    conclusions.append("")
    conclusions.append("### 6. Implikasi Praktis")

    if "Suspensi" in params.name:
        conclusions.append("- Untuk suspensi kendaraan, ζ ~ 0.3-0.5 memberikan keseimbangan kenyamanan dan handling")
    elif "Lab" in params.name:
        conclusions.append("- Pegas laboratorium cocok untuk demonstrasi Hooke's Law dan osilasi harmonik sederhana")
    elif "Pegas-Massa" in params.name:
        conclusions.append("- Sistem pegas-massa klasik mendemonstrasikan osilasi harmonik teredam")

    return "\n".join(conclusions)


# ============================================================
# EKSPOR DATA
# ============================================================

def export_to_csv(solution: dict, filename: str = "simulation_data.csv") -> str:
    """
    Ekspor hasil simulasi ke format CSV.

    Returns:
    --------
    str - CSV content
    """
    import io

    t = solution['t']
    x = solution['x']
    v = solution['v']
    a = solution['a']
    KE = solution['KE']
    PE = solution['PE']
    E_total = solution['E_total']

    output = io.StringIO()
    output.write("t(s),x(m),v(m/s),a(m/s2),KE(J),PE(J),E_total(J)\n")

    for i in range(len(t)):
        output.write(f"{t[i]:.6f},{x[i]:.6f},{v[i]:.6f},{a[i]:.6f},{KE[i]:.6f},{PE[i]:.6f},{E_total[i]:.6f}\n")

    return output.getvalue()
