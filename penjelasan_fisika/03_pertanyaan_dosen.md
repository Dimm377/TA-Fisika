# Panduan Jawaban Teknis (Untuk Pertanyaan Dosen)

Berikut adalah "Cheat Sheet" jawaban jika dosen bertanya detail tentang kodingan.

---

## 1. **"Metode numerik apa yang kalian pakai?"**

**Jawaban:**
> "Untuk simulasi yang akurat (di grafik dan validasi), kami menggunakan **`scipy.integrate.odeint`** dari library SciPy, Pak."

**Penjelasan Detail (Jika ditanya lagi):**
- `odeint` menggunakan solver **LSODA** (Livermore Solver for Ordinary Differential Equations).
- Solver ini pintar: dia otomatis ganti metode antara **Adams** (untuk masalah non-stiff) dan **BDF** (Backward Differentiation Formula, untuk masalah stiff/kaku).
- Ini jauh lebih akurat dan stabil daripada metode Euler biasa.

---

## 2. **"Kenapa ada kode JavaScript di `app.py`?"**

**Jawaban:**
> "Itu untuk animasi interaktif **Real-time** di browser agar tidak lag, Pak."

**Poin Penting (Technical Trap):**
- **Python (Backend)**: Menghitung fisika berat, solusi analitik, dan validasi data menggunakan `odeint`. Akurasinya tinggi.
- **JavaScript (Frontend)**: Hanya menangani animasi visual saat user men-drag bola. Menggunakan metode **Euler sederhana** supaya ringan dan responsif (60 FPS) tanpa perlu refresh halaman ke server terus-menerus.
- Jadi ada 2 engine: JS untuk *interaksi user*, Python untuk *analisis data ilmiah*.

---

## 3. **"Seberapa akurat simulasi kalian?"**

**Jawaban:**
> "Sangat akurat, Pak. Kami memvalidasi hasil numerik Python dengan **solusi analitik** (rumus eksak fisika)."

**Bukti:**
- Tunjukkan Tab **Validasi**.
- Korelasi (Pearson correlation) antara data simulasi dan rumus teori mencapai **0.9999** (hampir sempurna).
- Error rata-rata (RMS Error) biasanya di bawah **1%**.

---

## 4. **"Coba jelaskan alur data (Flow) programnya."**

**Jawaban:**
1.  User input parameter (Massa `m`, Konstanta `k`) di Sidebar.
2.  Python membuat objek `SpringParameters` (pakai Dataclass biar rapi).
3.  Solver `odeint` menghitung posisi `x` untuk setiap detik (misal 10 detik).
4.  Data dikirim ke **Plotly** untuk jadi grafik interaktif.
5.  Untuk animasi, sampel data dikirim ke **HTML5 Canvas** biar diputar ulang.

---

## 5. **"Kenapa pakai Streamlit?"**

**Jawaban:**
> "Karena Streamlit memungkan kami fokus ke **logic Fisika** (Python) tanpa pusing memikirkan desain web (HTML/CSS) dari nol. Sangat cocok untuk prototyping aplikasi sains/data science."

---

## 6. **"Apa itu `state` di kode?"**

Jika dosen menunjuk kode:
```python
def persamaan_gerak_pegas(state, t, ...):
    x, v = state
```

**Jawaban:**
> "Itu adalah array yang menyimpan kondisi sistem saat ini, isinya sepasang **Posisi (x)** dan **Kecepatan (v)**. Solver butuh ini untuk menghitung kondisi langkah berikutnya."

---

## Tips Codingan di Layar
Jika disuruh buka kode, buka file:
`penjelasan_fisika/01_kode_gaya_pegas.py`

File ini lebih bersih dan penuh komentar bahasa Indonesia, jadi dosen lebih mudah bacanya dibanding `app.py` yang penuh kode UI.
