# 🔬 Simulasi Gaya Pegas - Hooke's Law

Aplikasi interaktif untuk mempelajari **Hukum Hooke** dan **sistem massa-pegas** dengan visualisasi real-time.

> Tugas Akhir Fisika Komputasi - Dimas, Daffa, Dharma

---

## 🎬 Demo

Jalankan aplikasi:
```bash
streamlit run app.py
```

---

## ✨ Fitur

| Fitur | Deskripsi |
|-------|-----------|
| 🎬 Animasi Real-time | Canvas HTML5 60fps dengan pegas vertikal |
| 📊 Grafik Interaktif | Plotly dengan zoom, pan, hover |
| 🔬 Validasi Numerik | Perbandingan dengan solusi analitik |
| 📈 Analisis FFT | Identifikasi frekuensi dominan |
| 🌀 Analisis Resonansi | Kurva respons frekuensi |
| 📥 Ekspor CSV | Download data simulasi |

---

## 📦 Preset Real-Life

| Sistem | Massa | k (N/m) | Tipe Redaman |
|--------|-------|---------|--------------|
| 🚗 Suspensi Mobil | 400 kg | 40000 | Near-critically damped |
| 🤸 Trampolin | 70 kg | 5000 | Underdamped |
| 🔬 Pegas Lab | 0.5 kg | 20 | Underdamped |
| ⚖️ Pegas-Massa | 1 kg | 100 | Underdamped |
| 🚪 Door Closer | 5 kg | 50 | Overdamped |

---

## 🚀 Instalasi

```bash
# Clone repository
git clone https://github.com/Dimm377/Ta-Fisika.git
cd Ta-Fisika

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

---

## 📐 Rumus Fisika

### Hukum Hooke
```
F = -kx
```

### Persamaan Gerak
```
m·x'' + c·x' + k·x = F(t)
```

### Frekuensi Natural
```
ωₙ = √(k/m)
```

### Rasio Redaman
```
ζ = c / (2√km)
```

---

## 📁 Struktur Folder

```
Ta-Fisika/
├── app.py                 # Aplikasi Streamlit utama
├── spring_physics.py      # Logic fisika & solver
├── spring_visualization.py # Fungsi visualisasi
├── requirements.txt       # Dependencies
├── README.md              # Dokumentasi
└── penjelasan_fisika/     # Folder pembelajaran
    ├── 01_kode_gaya_pegas.py
    └── 02_rumus_ringkasan.md
```

---

## 📖 Untuk Pembelajaran

Lihat folder `penjelasan_fisika/` untuk:
- Potongan kode dengan penjelasan detail
- Ringkasan rumus fisika
- Tips presentasi

---

## 👥 Tim

- **Dimas** - Developer  (**Anggota**)
- **Daffa** - Developer  (**Ketua**)
- **Dharma** - Developer (**Anggota**)

---

## 📄 Lisensi

MIT License - Bebas digunakan untuk keperluan edukasi.
