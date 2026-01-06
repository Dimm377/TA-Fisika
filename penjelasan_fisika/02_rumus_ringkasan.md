# Ringkasan Rumus Fisika (Cheat Sheet)
**Tugas Akhir Simulasi Gaya Pegas**

---

## 1. Hukum Dasar

### Hukum Hooke dan Gaya Pegas
Hukum Hooke menyatakan bahwa gaya yang diberikan oleh pegas sebanding dengan perubahan panjangnya. Gaya ini disebut **Gaya Pemulih** (*Restoring Force*) karena selalu berusaha mengembalikan pegas ke posisi setimbangnya.

```math
F_{pegas} = -k \cdot x
```

**Penjelasan Variabel:**
- **$F_{pegas}$**: Gaya pegas (Newton, N).
- **$k$**: Konstanta pegas (N/m). Menunjukkan tingkat "kekakuan" pegas.
  - Nilai $k$ besar = Pegas kaku (mobil, suspensi).
  - Nilai $k$ kecil = Pegas lunak (per pulpen).
- **$x$**: Simpangan atau perubahan panjang dari posisi setimbang (meter).
- **tanda negatif (-)**: Menunjukkan arah gaya selalu berlawanan dengan arah simpangan $x$.
  - Jika ditarik ke bawah ($x$ positif), gaya menarik ke atas ($F$ negatif).
  - Jika ditekan ke atas ($x$ negatif), gaya mendorong ke bawah ($F$ positif).

### Hukum Newton II (Persamaan Gerak)
Total gaya menentukan percepatan benda.
```math
\sum F = m \cdot a
```
$$ m \ddot{x} + c \dot{x} + k x = F_{eksternal} $$

---

## 2. Parameter Kunci

| Parameter | Simbol | Rumus | Keterangan |
| :--- | :---: | :--- | :--- |
| **Frekuensi Natural** | $\omega_n$ | $\sqrt{\frac{k}{m}}$ | Kecepatan sudut osilasi tanpa redaman |
| **Rasio Redaman** | $\zeta$ (zeta) | $\frac{c}{2\sqrt{km}}$ | Menentukan seberapa cepat osilasi mati |
| **Frekuensi Teredam** | $\omega_d$ | $\omega_n \sqrt{1 - \zeta^2}$ | Frekuensi aktual saat underdamped |
| **Periode Osilasi** | $T$ | $\frac{2\pi}{\omega_d}$ | Waktu untuk satu siklus penuh |

---

## 3. Klasifikasi Redaman

Nilai $\zeta$ menentukan perilaku sistem:

| Nilai $\zeta$ | Tipe Sistem | Perilaku Fisik | Contoh |
| :--- | :--- | :--- | :--- |
| **$\zeta = 0$** | **Undamped** | Berosilasi selamanya (tidak berhenti). | Pegas ideal di ruang hampa |
| **$0 < \zeta < 1$** | **Underdamped** | Berosilasi tapi amplitudonya mengecil secara eksponensial. | Trampolin, senar gitar |
| **$\zeta = 1$** | **Critically Damped** | Tidak berosilasi. Kembali ke titik 0 secepat mungkin. | Shockbreaker motor balap |
| **$\zeta > 1$** | **Overdamped** | Tidak berosilasi. Kembali ke titik 0 dengan sangat lambat. | Pintu otomatis (door closer) |

---

## 4. Solusi Matematis (Posisi $x$ terhadap waktu $t$)

Untuk kasus **Underdamped** ($0 < \zeta < 1$):
$$ x(t) = e^{-\zeta \omega_n t} \left( A \cos(\omega_d t) + B \sin(\omega_d t) \right) $$

- **$e^{-\zeta \omega_n t}$**: Bagian *decay* (peluruhan eksponensial).
- **$\cos / \sin$**: Bagian *osilasi*.

---

## 5. Energi Sistem

Total energi selalu berkurang jika ada redaman (diubah menjadi panas).

1. **Energi Kinetik (Gerak)**
   $$ EK = \frac{1}{2} m v^2 $$

2. **Energi Potensial (Pegas)**
   $$ EP = \frac{1}{2} k x^2 $$

3. **Energi Mekanik Total**
   $$ E_{total} = EK + EP $$

4. **Energi Terdisipasi (Hilang)**
   Daya yang hilang akibat gesekan: $P = c \cdot v^2$
   $$ E_{hilang} = \int (c \cdot v^2) dt $$

---

## 6. Fenomena Resonansi

Terjadi jika gaya eksternal $F (t) = F_0 \sin(\omega t)$ frekuensinya mendekati frekuensi natural sistem.

- **Frekuensi Resonansi Puncak**: $\omega_{res} = \omega_n \sqrt{1 - 2\zeta^2}$
- **Amplifikasi Maksimum (Q-Factor)**: Seberapa kuat getarannya saat resonansi.
  $$ Q \approx \frac{1}{2\zeta} $$
  *(Semakin kecil redaman, semakin "gila" getarannya saat resonansi)*
