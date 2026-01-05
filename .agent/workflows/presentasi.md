---
description: Workflow presentasi Tugas Akhir Simulasi Gaya Pegas
---

# Workflow Presentasi

## Sebelum Presentasi (H-1)

// turbo
1. Test simulasi berjalan dengan baik
```bash
cd /home/dimm/Ta-Fisika
source venv/bin/activate
streamlit run app.py
```

2. Siapkan backup:
   - Screenshot semua preset
   - Export PDF grafik
   - Video rekaman demo (jaga-jaga)

3. Check projector/layar:
   - Pastikan resolusi OK
   - Dark mode bagus di layar besar

---

## Hari H - Sebelum Giliran

// turbo
1. Buka terminal dan jalankan:
```bash
cd /home/dimm/Ta-Fisika
source venv/bin/activate
streamlit run app.py
```

2. Buka browser ke `localhost:8501`
3. Pilih preset **Suspensi Mobil** (jangan play dulu)
4. Minimize terminal, fullscreen browser

---

## Saat Presentasi

### Slide 1: Opening (1 menit)
- Perkenalan tim
- Judul: "Simulasi Gaya Pegas - Hukum Hooke"

### Slide 2: Teori (2 menit)
- Rumus Hukum Hooke: F = -kx
- Persamaan gerak: m·x'' + c·x' + k·x = F(t)
- Sebutkan 3 tipe redaman

### Demo 1: Suspensi Mobil (3 menit)
1. Tunjukkan parameter (m, k, c, ζ)
2. Klik **Play**
3. "Perhatikan osilasi teredam, ini near-critically damped"
4. Pause, tunjukkan energi berkurang
5. Buka tab **Grafik** - tunjukkan phase space

### Demo 2: Trampolin (2 menit)
1. Ganti ke preset **Trampolin**
2. Klik **Play**
3. "Ini underdamped - lihat bouncing berulang"
4. Bandingkan dengan suspensi mobil

### Demo 3: Door Closer (2 menit)
1. Ganti ke preset **Door Closer**
2. Klik **Play**
3. "Overdamped - kembali sangat lambat tanpa osilasi"
4. Jelaskan kenapa pintu harus overdamped

### Tab Validasi (2 menit)
1. Buka tab **Validasi & FFT**
2. Tunjukkan korelasi 0.999999
3. "Solusi numerik kami akurat dibanding analitik"

### Tab Kesimpulan (1 menit)
1. Buka tab **Kesimpulan**
2. Baca poin-poin utama

### Closing (1 menit)
- "Kesimpulan: Simulasi berhasil memvalidasi Hukum Hooke"
- "Terima kasih, ada pertanyaan?"

---

## Tips Penting

| Do ✅ | Don't ❌ |
|------|---------|
| Fokus ke fisika dan demo | Jangan jelaskan kode |
| Pause di momen penting | Jangan terlalu cepat |
| Eye contact dengan audiens | Jangan baca layar terus |
| Siapkan jawaban untuk ζ | Jangan panik kalau ada error |

---

## Pertanyaan yang Mungkin Muncul

**Q: Kenapa pakai Python/Streamlit?**
A: Python punya library scipy untuk solve ODE, Streamlit untuk UI interaktif

**Q: Berapa akurasi simulasinya?**
A: Korelasi 99.9999% dengan solusi analitik

**Q: Apa bedanya underdamped vs overdamped?**
A: Underdamped = oscillate dulu, Overdamped = langsung kembali tanpa oscillate

**Q: Kenapa suspensi mobil pakai near-critically damped?**
A: Keseimbangan antara kenyamanan (tidak bouncing) dan response cepat
