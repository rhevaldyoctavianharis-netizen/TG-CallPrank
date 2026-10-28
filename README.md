<div align="center">

# 👻 Prank Call Userbot

**Telepon masuk → _"nomor yang anda tuju tidak aktif"_ → lalu suara-suara aneh menyusul…**

Userbot Telegram berbasis **Telethon** + **PyTgCalls** khusus untuk bercanda dengan teman.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Telethon](https://img.shields.io/badge/Telethon-userbot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![PyTgCalls](https://img.shields.io/badge/PyTgCalls-2.x-8A2BE2?style=for-the-badge)
![Heroku](https://img.shields.io/badge/Heroku-ready-430098?style=for-the-badge&logo=heroku&logoColor=white)
![Purpose](https://img.shields.io/badge/Purpose-Prank%20Only-ff69b4?style=for-the-badge)

<br>

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/rhevaldyoctavianharis-netizen/TG-CallPrank)

</div>

---

## ✨ Fitur

| | Fitur | Keterangan |
|---|---|---|
| 📞 | **Auto-angkat telepon** | Telepon masuk langsung diangkat otomatis |
| 🔇 | **Audio utama** | `assets/main.mp3` diputar pertama (_"nomor yang anda tuju tidak aktif"_) |
| 🎲 | **Audio seram acak** | Dipilih acak (sistem kocok kartu, tanpa pengulangan beruntun) dan terus looping |
| ⏱️ | **Batas durasi** | Maksimal 5 menit, atur lewat `MAX_CALL_SECONDS` |
| 💬 | **Prank chat** | Delay acak → "mengetik…" → berhenti → offline lagi (tanpa balasan, tanpa dibaca) |
| 🎯 | **Target terbatas** | `ALLOWED_IDS` supaya hanya teman tertentu yang kena |

---

## 🗂️ Struktur Proyek

```
prank-userbot/
├── main.py             # entry point
├── config.py           # pengaturan (.env) + daftar audio
├── audio_manager.py    # pemilih audio acak
├── call_handler.py     # logika telepon
├── chat_handler.py     # prank mengetik
├── presence.py         # status online/offline
├── generate_session.py # pembuat SESSION_STRING
├── assets/             # taruh audio di sini
│   └── main.mp3        # ← WAJIB
├── app.json            # konfigurasi Heroku
└── Procfile            # worker Heroku
```

---

## 🚀 Deploy ke Heroku

1. **Ambil API ID & API HASH** di [my.telegram.org](https://my.telegram.org).
2. **Buat SESSION_STRING** di komputer/Termux sendiri:
   ```bash
   pip install telethon
   python generate_session.py
   ```
3. **Fork repo ini**, lalu taruh `main.mp3` dan audio seram kamu di folder `assets/` (audio harus ikut ter-commit karena Heroku tidak menyimpan file upload).
4. Daftarkan nama file audio seram di `config.py` → `DISTURBING_AUDIOS` (atau kosongkan agar semua audio di `assets/` dipakai otomatis).
5. Ganti `GANTI_USERNAME/GANTI_REPO` di `app.json` dan tombol di atas dengan repo kamu.
6. Klik tombol **Deploy to Heroku**, isi variabel yang diminta, lalu deploy.
7. Setelah selesai, buka **Resources** dan aktifkan dyno **worker** (bukan web).

> 💡 Buildpack **ffmpeg** sudah otomatis ditambahkan lewat `app.json`.

---

## 💻 Jalankan Lokal (Linux / Termux)

```bash
git clone https://github.com/rhevaldyoctavianharis-netizen/TG-CallPrank
cd GANTI_REPO
sudo apt install ffmpeg          # Termux: pkg install ffmpeg
pip install -r requirements.txt
cp .env.example .env             # lalu isi API_ID dan API_HASH
python main.py
```

Login pertama akan meminta nomor HP dan kode OTP.

---

## ⚙️ Variabel Konfigurasi

| Variabel | Default | Fungsi |
|---|---|---|
| `API_ID` / `API_HASH` | – | Kredensial Telegram (wajib) |
| `SESSION_STRING` | – | Wajib di Heroku |
| `ALLOWED_IDS` | kosong | ID target prank, pisahkan koma |
| `MAX_CALL_SECONDS` | `300` | Durasi maksimal telepon |
| `GAP_MIN` / `GAP_MAX` | `1` / `4` | Jeda hening antar audio |
| `CHAT_DELAY_MIN` / `MAX` | `5` / `40` | Delay sebelum mengetik |
| `TYPING_MIN` / `MAX` | `4` / `12` | Lama sekali mengetik |
| `BURSTS_MIN` / `MAX` | `1` / `3` | Jumlah ketikan berulang |
| `CHAT_COOLDOWN` | `120` | Cooldown prank chat per orang |

---

## ⚠️ Disclaimer

Proyek ini dibuat **hanya untuk hiburan dan prank antar teman**, **bukan** untuk penipuan, teror, pelecehan, penyamaran, atau tindakan melanggar hukum lainnya.

- Gunakan hanya pada orang yang kamu kenal dan yang akan memahami bahwa ini bercanda.
- Jangan dipakai pada orang yang rentan, anak-anak, atau orang yang punya kondisi jantung/kecemasan.
- Menjalankan userbot dapat melanggar Terms of Service Telegram dan berisiko akunnya dibatasi atau diblokir. Disarankan memakai akun cadangan.
- **Seluruh tanggung jawab penggunaan sepenuhnya ada pada pengguna.** Pembuat tidak bertanggung jawab atas penyalahgunaan, kerugian, atau konsekuensi apa pun.

---

## 💖 Credit

<div align="center">

**Dibuat oleh Rhevaldy**

[![Telegram](https://img.shields.io/badge/Telegram-@rapaldy-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/rapaldy)
[![Channel](https://img.shields.io/badge/Channel-youlittleboy-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/youlittleboy)
[![Website](https://img.shields.io/badge/Website-rhevaldy.my.id-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://rhevaldy.my.id)

<sub>Kalau suka, kasih ⭐ di repo ini ya!</sub>

</div>
