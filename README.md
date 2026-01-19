# Chatbot Toko Alat Pertanian (Toko Tani Suka Maju)

Proyek ini adalah aplikasi Chatbot berbasis AI untuk **Toko Tani Suka Maju**, yang dibangun menggunakan **Streamlit**, **Google Gemini AI**, dan **Supabase**. Chatbot ini dirancang untuk membantu pelanggan mendapatkan informasi mengenai produk pertanian, stok, harga, serta informasi umum toko secara interaktif dan real-time.

## 🌟 Fitur Utama

- **AI Chatbot Cerdas**: Menggunakan model `gemini-2.5-flash` untuk memberikan respons yang natural dan relevan.
- **Integrasi Database Real-time**: Terhubung dengan **Supabase** untuk menampilkan data produk (stok, harga, deskripsi) yang selalu terupdate.
- **Informasi Toko**: Memberikan informasi statis seperti alamat, jam operasional, dan kontak.
- **Antarmuka Pengguna (UI) Kustom**: Desain bertema pertanian yang bersih dan responsif dengan mode malam dimatikan (force light mode).
- **Riwayat Chat**: Menyimpan konteks percakapan selama sesi berlangsung.
- **Tombol Cepat**: Fitur pertanyaan populer untuk akses informasi cepat.

## 🛠️ Teknologi yang Digunakan

- [Streamlit](https://streamlit.io/) - Framework untuk antarmuka web.
- [Google Generative AI (Gemini)](https://ai.google.dev/) - Otak kecerdasan buatan chatbot.
- [Supabase](https://supabase.com/) - Database backend untuk manajemen produk.
- [Python Dotenv](https://pypi.org/project/python-dotenv/) - Manajemen variabel lingkungan.

## 📋 Prasyarat

Sebelum menjalankan aplikasi, pastikan Anda memiliki:
1.  **Python 3.8+** terinstal di komputer.
2.  **API Key Google Gemini** (Dapatkan di [Google AI Studio](https://aistudio.google.com/)).
3.  **Proyek Supabase** dengan tabel `products` yang memiliki kolom:
    - `nama_produk`
    - `kategori_produk`
    - `jenis_produk`
    - `harga`
    - `satuan_jual`
    - `stok`
    - `deskripsi`, `fungsi_produk`, `peruntukan_produk` (Opsional)

## 🚀 Cara Instalasi

1.  **Clone repositori ini** (atau download filenya):
    ```bash
    git clone https://github.com/username/project-name.git
    cd project-name
    ```

2.  **Buat Virtual Environment (Opsional tapi disarankan):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Konfigurasi Environment

Buat file bernama `.env` di direktori utama proyek dan tambahkan konfigurasi berikut:

```env
GEMINI_API_KEY=masukkan_api_key_gemini_anda_disini
SUPABASE_URL=masukkan_url_project_supabase_anda
SUPABASE_KEY=masukkan_anon_public_key_supabase_anda
```

> **Catatan:** Jangan bagikan file `.env` atau kunci API Anda ke publik.

## ▶️ Cara Menjalankan Aplikasi

Jalankan aplikasi menggunakan perintah Streamlit:

```bash
streamlit run appdeploy.py
```

Aplikasi akan otomatis terbuka di browser default Anda (biasanya di `http://localhost:8501`).

## 📂 Struktur Project

- `appdeploy.py`: File utama aplikasi (logic chatbot & UI).
- `requirements.txt`: Daftar pustaka Python yang dibutuhkan.
- `.env`: File konfigurasi sensitif (tidak diupload ke git).

## 📝 Lisensi

[Tuliskan lisensi Anda di sini, misal: MIT License]
