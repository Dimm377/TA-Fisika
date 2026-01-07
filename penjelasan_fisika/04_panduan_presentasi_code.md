# Panduan Presentasi Kode: Simulasi Gaya Pegas

Dokumen ini berisi daftar bagian kode yang **wajib** ditunjukkan saat presentasi untuk menjelaskan bagaimana logika fisika bekerja di balik layar.

## 1. "Otak" Fisika (`physics_config/spring_physics.py`)

Ini adalah file paling penting. Jika ditanya "di mana rumus fisikanya?", buka file ini.

### A. Definisi Benda (Class `SpringParameters`)
**Lokasi:** Baris 36 - 45
**Apa yang dijelaskan:**
- Tunjukkan bahwa kita menggunakan `class` untuk membungkus variabel fisika: Massa ($m$), Konstanta Pegas ($k$), dan Redaman ($c$).
- Ini membuktikan kode kita terstruktur rapi (Object-Oriented).

### B. Rumus Fisika Turunan (Properties)
**Lokasi:** Baris 47 - 71
**Apa yang dijelaskan:**
- Tunjukkan fungsi `omega_n` (Frekuensi Natural) dan `zeta` (Rasio Redaman).
- Jelaskan bahwa kode ini *otomatis* menghitung sifat sistem dari $m$, $k$, dan $c$.

### C. Hukum Hooke & Newton (Fungsi Force)
**Lokasi:** Baris 152 - 168
**Apa yang dijelaskan:**
- `calculate_spring_force`: Implementasi $F = -kx$.
- `calculate_damping_force`: Implementasi $F = -cv$.
- `calculate_net_force`: Penjumlahan semua gaya (Hukum 2 Newton $F_{total} = ma$).

### D. Mesin Simulasi (Solver)
**Lokasi:** Baris 206 - 224
**Apa yang dijelaskan:**
- Tunjukkan fungsi `solve_spring_system`.
- Jelaskan kita menggunakan **`odeint`** dari library `scipy`. Ini adalah standar ilmiah untuk menyelesaikan persamaan diferensial, sehingga hasilnya **sangat akurat** (bukan sekedar animasi game biasa).

---

## 2. Integrasi ke Aplikasi (`app.py`)

Tunjukkan ini jika ditanya "bagaimana cara physics-nya nyambung ke tampilan?".

### A. Menggunakan Library Fisika Kita
**Lokasi:** Baris 20-25 (Import) & Baris 600 (Pemanggilan)
**Apa yang dijelaskan:**
- Tunjukkan kita meng-import fungsi dari file `spring_physics.py`.
- Tunjukkan baris `solution_auto = solve_spring_system(...)` yang membuktikan tampilan grafik dihitung langsung dari rumus fisika tadi.

### B. Animasi Interaktif (JavaScript) - Optional
**Lokasi:** Baris 264 - 284 (Dalam string `interactive_html`)
**Apa yang dijelaskan:**
- Jika penguji bertanya "kok bisa ditarik-tarik?", tunjukkan bagian ini.
- Ini adalah fisika versi *ringan* (Euler Integration) yang berjalan di browser agar responsif saat di-drag, berbeda dengan perhitungan grafik yang menggunakan Scientific Python (`odeint`).

---

## Tips Menjawab Pertanyaan:

1.  **"Validasi codingannya gimana?"**
    - Buka `spring_physics.py` baris 370 (`analytical_solution`). Jelaskan kita punya solusi analitik (rumus eksak matematika) untuk memverifikasi hasil simulasi komputer.

2.  **"Kenapa dipisah folder-nya?"**
    - Agar rapi: `physics_config` khusus hitungan matematika murni, `app.py` khusus tampilan/UI. Konsep ini disebut **Separation of Concerns**.
