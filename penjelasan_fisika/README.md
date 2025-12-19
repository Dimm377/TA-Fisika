# Folder Penjelasan Fisika Gaya Pegas

Folder ini berisi kode-kode yang berhubungan dengan **gaya pegas** untuk dipelajari dan dijelaskan saat presentasi.

> **CATATAN:** File di folder ini **TIDAK untuk di-run**, hanya untuk referensi pembelajaran.

---

## Isi Folder

| File | Deskripsi |
|------|-----------|
| `01_kode_gaya_pegas.py` | Potongan kode fisika dengan penjelasan lengkap |
| `02_rumus_ringkasan.md` | Ringkasan semua rumus fisika |

---

## Bagian yang Perlu Dijelaskan

### 1. Hukum Hooke
```
F = -kx
```
- `k` = konstanta pegas (N/m)
- `x` = displacement dari posisi kesetimbangan (m)
- Tanda negatif = gaya berlawanan arah displacement

### 2. Persamaan Gerak
```
m·x'' + c·x' + k·x = F(t)
```
- Persamaan diferensial orde-2
- Kombinasi massa, redaman, dan pegas

### 3. Frekuensi Natural
```
ωₙ = √(k/m)
```

### 4. Rasio Redaman
```
ζ = c / (2√km)
```

### 5. Energi
```
KE = ½mv²  (Kinetik)
PE = ½kx²  (Potensial Pegas)
```

---

## Tips Presentasi

1. **Mulai dari Hukum Hooke** - Jelaskan bahwa gaya pegas berbanding lurus dengan displacement
2. **Tunjukkan persamaan gerak** - Gabungan 3 gaya: pegas, redaman, eksternal
3. **Jelaskan implementasi** - Tunjukkan baris 188 di `spring_physics.py`
4. **Demo animasi** - Jalankan aplikasi dan tunjukkan simulasi
5. **Validasi** - Tunjukkan perbandingan numerik vs analitik

---

## File Utama (Untuk Di-run)

- `/home/dimm/Ta-Fisika/app.py` - Aplikasi Streamlit
- `/home/dimm/Ta-Fisika/spring_physics.py` - Logic fisika
