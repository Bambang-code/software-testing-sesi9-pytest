# Tugas Sesi 9 - Unit Testing dengan PyTest

Studi kasus mandiri: **layanan peminjaman buku perpustakaan**. Proyek ini
khusus Sesi 9, dengan kode Python dan test PyTest di repo tersendiri.

## Aturan bisnis

| Fungsi | Aturan |
| --- | --- |
| `hitung_denda(hari_terlambat)` | Hari 1-7: Rp2.000 per hari; hari berikutnya: Rp5.000 per hari tambahan. Hari 0 tidak didenda; hari negatif ditolak. Contoh: 8 hari = Rp19.000. |
| `batas_peminjaman(jenis_anggota)` | Mahasiswa maksimal 3 buku aktif, dosen 5, umum 2. Jenis anggota lain ditolak. |
| `pinjam_buku(...)` | Jumlah pinjaman harus nonnegatif dan masih di bawah batas anggota, email wajib diisi, dan stok buku harus tersedia. Keberhasilan mengurangi stok satu buku. Email gagal atau timeout membatalkan transaksi dan mengembalikan stok. |

`buat_katalog()` adalah helper untuk membuat SQLite dalam memori. Parameter
hari dan jumlah pinjaman berupa bilangan bulat; jenis anggota memakai huruf
kecil: `mahasiswa`, `dosen`, atau `umum`. Jumlah pinjaman aktif disediakan
pemanggil. Validasi email pada contoh ini sebatas tidak kosong.

## Menjalankan

Gunakan Python 3.10 atau lebih baru. Perintah berikut dijalankan dari root repo.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -v --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html
```

### Linux / macOS

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -v --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html
```

Laporan HTML hasil menjalankan ulang berada di `htmlcov/index.html`. Konfigurasi
`.coveragerc` mengukur seluruh paket `perpustakaan`, termasuk branch, dan membuat
perintah gagal jika coverage gabungan turun di bawah 100%.

Untuk membuat ulang bukti eksekusi di folder `laporan/` (teks, JSON, dan HTML):

```powershell
.\.venv\Scripts\python.exe scripts/buat_laporan.py
```

Di Linux/macOS, gunakan `.venv/bin/python scripts/buat_laporan.py`.

## Pemenuhan tugas

| Syarat Sesi 9 | Implementasi |
| --- | --- |
| Minimal 3 fungsi berlogika bersyarat | `hitung_denda`, `batas_peminjaman`, `pinjam_buku` |
| Minimal 8 test | 14 fungsi test; parametrization menghasilkan 36 kasus |
| Minimal 1 `parametrize` berdasarkan BVA | Denda pada 0, 1, 6, 7, 8, 9 hari; pinjaman pada batas-1, batas, dan batas+1 setiap jenis anggota |
| Minimal 2 test `pytest.raises` | Hari negatif, jenis anggota salah, jumlah negatif, batas terlampaui, email kosong, buku tidak tersedia, email gagal, timeout |
| Minimal 1 fixture dengan `yield` dan cleanup | Fixture `katalog` membuat database baru, menyemai data, `yield`, lalu menutup koneksi dalam `finally` |
| Minimal 1 penggunaan mock | `unittest.mock.Mock` mengganti pengirim email; memeriksa argumen, jumlah panggilan, serta tidak dipanggil saat validasi gagal |
| Laporan coverage dan analisis cabang | [Laporan tugas](laporan/LAPORAN.md), [hasil eksekusi](laporan/hasil-pytest.txt), [data coverage](laporan/coverage.json) |

## Struktur

```text
perpustakaan/
  __init__.py
  layanan.py              # Logika yang diuji
tests/
  conftest.py             # Fixture katalog dan mock email
  test_layanan.py         # BVA, negatif, interaksi, dan rollback
laporan/
  LAPORAN.md              # Pembahasan dan analisis coverage
  hasil-pytest.txt         # Output eksekusi aktual
  coverage.json           # Bukti baris dan cabang yang dieksekusi
  html/                   # Laporan HTML eksekusi yang disertakan
contoh/workflow-pytest.yml  # Template CI opsional
scripts/buat_laporan.py    # Membuat ulang bukti dari satu eksekusi test
```

SQLite dalam memori menjadi penyimpanan sementara yang terisolasi. Pengirim
email disuntikkan sebagai callable; selama test selalu diganti mock, sehingga
tidak memerlukan akun, API key, jaringan, atau layanan email asli. Kontrak
pengirim adalah `(alamat_email, pesan) -> bool`; exception diteruskan ke pemanggil.

Template GitHub Actions di `contoh/workflow-pytest.yml` disediakan untuk
menjalankan suite pada Python 3.10 dan 3.12. Template ini belum diaktifkan sebagai
workflow repo. Hasil eksekusi lokal dan batas pengujian dibahas di laporan.

## Dokumen pengumpulan dan screenshot manual

Kesebelas screenshot manual dari pengguna sudah disertakan secara utuh di
`laporan/latex/images/` dan dimasukkan ke [PDF final](laporan/latex/main.pdf).
Seluruh PNG asli dipertahankan tanpa crop.
Seluruh halaman laporan memakai A4 portrait (210 x 297 mm). Screenshot
ditampilkan utuh dengan skala proporsional pada halaman tegak.
Semua screenshot berasal dari hasil eksekusi di terminal: 8 hasil fungsi test
(termasuk BVA dan minimal 2 test negatif), 1 hasil setup/teardown fixture,
1 hasil pengujian mock, dan 1 hasil suite lengkap beserta coverage.
[Panduan screenshot](laporan/PANDUAN_SCREENSHOT.md) menyediakan perintah untuk
mengulangi setiap hasil. Test BVA dan test negatif termasuk dalam minimal 8 test.
[Sumber LaTeX](laporan/latex/main.tex) menggabungkan cover, analisis, dan sebelas
gambar. Cover memuat logo universitas pada `assets/logo-ukwms.png`.
Sertakan folder `images/` dan `assets/` saat memindahkan sumbernya.
[Paket pengumpulan](output/pengumpulan-sesi9.zip) berisi PDF, sumber LaTeX,
sebelas screenshot asli, dan aset logo cover dalam satu arsip.

Untuk mengompilasi ulang laporan, jalankan dari root repo:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\kompilasi_laporan.ps1
```

PDF hasil kompilasi adalah `laporan/latex/main.pdf`. Script memerlukan compiler
Tectonic portabel pada `.tools/tectonic/tectonic.exe` yang tersedia di komputer
kerja ini; compiler tidak dimasukkan ke Git. Pada komputer lain, folder
`laporan/latex` dapat dikompilasi dengan Tectonic/LaTeX atau diunggah ke Overleaf.
Opsi `-Draf` hanya diperlukan untuk pratinjau jika gambar pada pengembangan
berikutnya belum lengkap.

## Referensi

- Materi kuliah: *Sesi 9 - Unit Testing (PyTest)*, bagian **Tugas Sesi 9**, halaman 10.
- [PyTest: fixture dengan yield dan teardown](https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended)
- [PyTest: parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [pytest-cov: laporan coverage](https://pytest-cov.readthedocs.io/en/latest/reporting.html)
- [Python: unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
