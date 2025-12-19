# Ringkasan Rumus Fisika Gaya Pegas

## 1. Hukum Hooke (Gaya Pegas)
```
F = -kx
```
| Simbol | Satuan | Keterangan |
|--------|--------|------------|
| F | N | Gaya pegas |
| k | N/m | Konstanta pegas |
| x | m | Displacement |

---

## 2. Persamaan Gerak (Newton II)
```
m·x'' + c·x' + k·x = F(t)
```
atau dalam bentuk standar:
```
x'' + 2ζωₙx' + ωₙ²x = F(t)/m
```

---

## 3. Frekuensi Natural
```
ωₙ = √(k/m)
```
```
f = ωₙ/(2π)  [Hz]
T = 2π/ωₙ   [s]
```

---

## 4. Rasio Redaman (Damping Ratio)
```
ζ = c / (2√km) = c / (2mωₙ)
```

| Nilai ζ | Tipe | Perilaku |
|---------|------|----------|
| ζ = 0 | Undamped | Osilasi terus |
| 0 < ζ < 1 | Underdamped | Osilasi teredam |
| ζ = 1 | Critically Damped | Kembali tercepat |
| ζ > 1 | Overdamped | Kembali lambat |

---

## 5. Frekuensi Teredam (Underdamped)
```
ωd = ωₙ√(1 - ζ²)
```

---

## 6. Solusi Underdamped
```
x(t) = e^(-ζωₙt) [A·cos(ωd·t) + B·sin(ωd·t)]
```

---

## 7. Energi Mekanik
```
Energi Kinetik:    KE = ½mv²
Energi Potensial:  PE = ½kx²
Energi Total:      E = KE + PE
```

---

## 8. Resonansi
```
Fungsi Transfer: |H(ω)| = 1/√[(1-r²)² + (2ζr)²]
dimana r = ω/ωₙ

Frekuensi Resonansi: ω_res = ωₙ√(1-2ζ²)
Quality Factor:      Q = 1/(2ζ)
Bandwidth:           Δω = 2ζωₙ
```

---

## 9. Implementasi di Kode
```python
# Percepatan (Hukum Newton II)
a = (F_ext - c*v - k*x) / m

# Frekuensi natural
omega_n = sqrt(k/m)

# Rasio redaman  
zeta = c / (2*sqrt(k*m))

# Energi
KE = 0.5 * m * v**2
PE = 0.5 * k * x**2
```
