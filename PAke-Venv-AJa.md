# Panduan Virtual Environment (venv) di Windows

## 📋 Apa itu Virtual Environment?

Virtual Environment adalah lingkungan Python yang terisolasi, memungkinkan Anda menginstal package secara terpisah untuk setiap proyek tanpa mempengaruhi instalasi Python global.

---

## 🚀 Instalasi dan Pembuatan venv

### 1. Buka Command Prompt atau PowerShell

Tekan `Win + R`, ketik `cmd` atau `powershell`, lalu tekan Enter.

### 2. Navigasi ke Folder Proyek

```cmd
cd path\ke\folder\proyek
```

Contoh:
```cmd
cd C:\Users\Dimm\Ta-Fisika
```

### 3. Buat Virtual Environment

```cmd
python -m venv venv
```

> **Catatan:** `venv` di akhir adalah nama folder untuk virtual environment. Anda bisa menggantinya dengan nama lain seperti `.venv` atau `env`.

---

## ⚡ Mengaktifkan Virtual Environment

### Command Prompt (CMD)

```cmd
venv\Scripts\activate
```

### PowerShell

```powershell
venv\Scripts\Activate.ps1
```

> **Jika ada error di PowerShell**, jalankan perintah ini terlebih dahulu:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Tanda venv Aktif

Setelah aktivasi berhasil, Anda akan melihat nama environment di awal prompt:

```
(venv) C:\Users\Dimm\Ta-Fisika>
```

---

## 📦 Menginstal Package

Setelah venv aktif, instal package menggunakan pip:

```cmd
pip install nama_package
```

Contoh untuk proyek ini:
```cmd
pip install streamlit numpy matplotlib scipy
```

### Menginstal dari requirements.txt

```cmd
pip install -r requirements.txt
```

---

## 📝 Menyimpan Daftar Package

Untuk menyimpan semua package yang terinstal:

```cmd
pip freeze > requirements.txt
```

---

## 🛑 Menonaktifkan Virtual Environment

Untuk keluar dari virtual environment:

```cmd
deactivate
```

---

## 🗑️ Menghapus Virtual Environment

Cukup hapus folder `venv`:

```cmd
rmdir /s /q venv
```

Atau hapus manual melalui File Explorer.

---

## 💡 Tips Berguna

| Perintah | Fungsi |
|----------|--------|
| `python --version` | Cek versi Python |
| `pip list` | Lihat semua package terinstal |
| `pip show nama_package` | Lihat detail package |
| `pip uninstall nama_package` | Hapus package |

---

## ⚠️ Troubleshooting

### Error: 'python' is not recognized

Python belum ditambahkan ke PATH. Solusi:
1. Reinstall Python dan centang **"Add Python to PATH"**
2. Atau tambahkan manual melalui Environment Variables

### Error: Execution Policy di PowerShell

Jalankan PowerShell sebagai Administrator, lalu:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: pip not found

Coba gunakan:
```cmd
python -m pip install nama_package
```

---

## 📁 Struktur Folder dengan venv

```
Ta-Fisika/
├── venv/                     # Folder virtual environment (jangan di-commit ke Git)
│   ├── Scripts/              # File aktivasi dan executables
│   ├── Lib/                  # Package Python terinstal
│   └── ...
├── app.py                    # Entry point aplikasi
├── physics_config/           # Physics engine & config
│   ├── config.py
│   ├── spring_physics.py
│   └── spring_visualization.py
├── styles/
│   └── styles.css
├── requirements.txt          # Daftar dependencies
└── ...
```

> **Penting:** Tambahkan `venv/` ke file `.gitignore` agar tidak terupload ke repository.

---

## 🔄 Workflow Lengkap

```cmd
# 1. Buat venv (sekali saja)
python -m venv venv

# 2. Aktifkan venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Jalankan aplikasi
streamlit run app.py

# 5. Selesai? Deactivate
deactivate
```
