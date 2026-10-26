# Laporan Tugas Sesi 9 - Unit Testing dengan PyTest

**Studi kasus:** layanan peminjaman buku perpustakaan

**Repository:** [software-testing-sesi9-pytest](https://github.com/Bambang-code/software-testing-sesi9-pytest)

**Tanggal pengujian:** 26 Oktober 2026

## 1. Tujuan dan ruang lingkup

Tugas ini menerapkan unit testing pada modul Python yang mempunyai minimal tiga
fungsi bersyarat. Suite menggunakan Boundary Value Analysis (BVA),
`pytest.mark.parametrize`, `pytest.raises`, fixture dengan cleanup memakai
`yield`, mock dependensi email, serta pengukuran statement dan branch coverage.

Modul yang diuji adalah [`perpustakaan/layanan.py`](../perpustakaan/layanan.py).
Aturan bisnis berikut ditetapkan untuk studi kasus mandiri Sesi 9:

1. **Denda:** hari 1-7 dikenai Rp2.000 per hari, lalu Rp5.000 per hari tambahan.
   Hari 0 tidak dikenai denda; nilai negatif ditolak. Misalnya 8 hari menghasilkan
   `(7 x 2.000) + (1 x 5.000) = Rp19.000`.
2. **Batas peminjaman:** mahasiswa 3, dosen 5, dan umum 2 buku aktif. Jenis anggota
   yang tidak dikenal ditolak.
3. **Peminjaman:** jumlah pinjaman saat ini harus nonnegatif dan kurang dari
   batas anggota. Email harus diisi dan buku harus memiliki stok. Peminjaman
   yang berhasil mengurangi stok satu; kegagalan email atau timeout membatalkan
   perubahan stok.

Tiga fungsi bersyaratnya adalah `hitung_denda`, `batas_peminjaman`, dan
`pinjam_buku`. Helper `buat_katalog` membuat tabel `buku` dalam SQLite sementara.
Hari dan jumlah pinjaman menggunakan bilangan bulat; jenis anggota memakai
huruf kecil. Pemanggil memberikan jumlah pinjaman aktif anggota.

## 2. Desain skenario uji

### Boundary Value Analysis

| Area | Input | Hasil yang diharapkan |
| --- | --- | --- |
| Batas bawah hari | `-1`, `0`, `1` | `ValueError`, Rp0, Rp2.000 |
| Perubahan tarif hari ke-7 | `6`, `7`, `8` | Rp12.000, Rp14.000, Rp19.000 |
| Tarif lanjutan | `9` | Rp24.000 |
| Batas mahasiswa | Pinjaman aktif `2`, `3`, `4` | Berhasil, ditolak, ditolak |
| Batas dosen | Pinjaman aktif `4`, `5`, `6` | Berhasil, ditolak, ditolak |
| Batas umum | Pinjaman aktif `1`, `2`, `3` | Berhasil, ditolak, ditolak |
| Batas stok | Stok `1`, kemudian `0` | Peminjaman terakhir berhasil, peminjaman selanjutnya ditolak |

Data BVA denda dan batas pinjaman dimasukkan ke `@pytest.mark.parametrize`.
Expected value ditulis eksplisit, sehingga test tidak menyalin rumus yang sedang
diuji. Pengujian juga memeriksa kondisi awal pinjaman `0`, anggota tidak dikenal,
email kosong atau spasi, kode buku tidak ada, dan stok habis.

### Daftar fungsi test

| Fungsi di `tests/test_layanan.py` | Kasus | Fokus |
| --- | ---: | --- |
| `test_hitung_denda_bva` | 6 | Nilai batas hari dan perubahan tarif |
| `test_hari_terlambat_negatif_ditolak` | 2 | `pytest.raises(ValueError)` dan pesan error |
| `test_batas_peminjaman_per_jenis` | 3 | Semua jenis anggota yang valid |
| `test_jenis_anggota_tidak_dikenal_ditolak` | 2 | Jenis salah dan string kosong |
| `test_pinjam_sukses_di_bawah_batas` | 6 | Hasil, pengurangan stok, dan interaksi email |
| `test_pinjam_pada_dan_di_atas_batas_ditolak` | 6 | Tepat pada batas dan satu di atasnya |
| `test_jumlah_pinjaman_negatif_ditolak` | 2 | Jumlah negatif tanpa efek samping |
| `test_pinjam_dengan_jenis_anggota_tidak_dikenal` | 1 | Validasi anggota pada alur peminjaman |
| `test_email_kosong_ditolak` | 2 | Email kosong dan hanya spasi |
| `test_buku_tidak_tersedia_ditolak` | 2 | Stok nol dan buku tidak ditemukan |
| `test_email_gagal_mengembalikan_stok` | 1 | Rollback ketika pengirim mengembalikan `False` |
| `test_email_timeout_mengembalikan_stok` | 1 | Exception dependensi diteruskan dan stok pulih |
| `test_stok_terakhir_habis_setelah_dipinjam` | 1 | Tidak terjadi peminjaman melebihi stok |
| `test_rollback_tidak_membatalkan_peminjaman_sebelumnya` | 1 | Commit sebelumnya tetap ada setelah kegagalan baru |
| **Total: 14 fungsi test** | **36** | Seluruhnya memiliki assertion hasil, exception, state, atau interaksi |

### Fixture dengan cleanup

Fixture `katalog` di [`tests/conftest.py`](../tests/conftest.py) menggunakan scope
`function` bawaan PyTest. Setiap kasus memperoleh SQLite dalam memori yang baru,
dengan buku `B001` berstok 2 dan `B002` berstok 0. Data awal di-commit sebelum
`yield`, sehingga rollback hanya membatalkan transaksi yang sedang diuji.

Setelah test selesai, blok `finally` menjalankan `koneksi.close()`, termasuk
ketika assertion gagal. Database sementara tidak dipakai ulang oleh test lain.
Fixture diperlukan karena pengujian peminjaman menggunakan sumber daya dan
state yang dapat berubah; test fungsi denda murni cukup memakai data parameter.

### Mock dan isolasi

Fixture `pengirim_email` menyediakan `unittest.mock.Mock(return_value=True)`.
Objek ini disuntikkan ke parameter `kirim_email`, menggantikan dependensi layanan
email. Tidak ada pengiriman sungguhan atau panggilan jaringan selama test.

| Skenario | Konfigurasi mock | Assertion utama |
| --- | --- | --- |
| Peminjaman berhasil | `return_value=True` | Pesan sukses, stok 2 menjadi 1, `assert_called_once_with` alamat dan pesan yang benar |
| Validasi gagal / stok kosong | Mock tetap tersedia | Exception yang sesuai, stok tetap, `assert_not_called()` |
| Pengiriman gagal | `return_value=False` | `RuntimeError`, stok kembali menjadi 2, pengirim dipanggil sekali |
| Layanan timeout | `side_effect=TimeoutError(...)` | `TimeoutError`, stok kembali menjadi 2, argumen pengirim benar |
| Dua transaksi berturut-turut | `side_effect=[True, False]` | Stok akhir 1; hanya transaksi kedua yang di-rollback; dua panggilan sesuai |

SQLite dalam memori berfungsi sebagai penyimpanan sementara lokal. Fungsi
perhitungan denda dan batas anggota diuji langsung. Fokus pengujian tetap pada
hasil aturan bisnis dan efek samping yang terlihat oleh pemanggil.

## 3. Eksekusi dan hasil aktual

Lingkungan pengujian lokal: Windows, Python **3.10.11**, PyTest **8.4.2**,
pytest-cov **7.0.0**, dan coverage.py **7.16.2**. Dependensi pengujian utama
dipatok dalam [`requirements-dev.txt`](../requirements-dev.txt).

Perintah PyTest yang digunakan oleh `scripts/buat_laporan.py`:

```text
python -m pytest -v --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html:laporan/html --cov-report=json:laporan/coverage.json --color=no
```

Hasil eksekusi aktual: **36 passed**, tanpa test gagal, skip, atau xfail.
Ringkasan coverage dari eksekusi yang sama:

```text
Name                       Stmts   Miss Branch BrPart    Cover   Missing
------------------------------------------------------------------------
perpustakaan\__init__.py       0      0      0      0  100.00%
perpustakaan\layanan.py       36      0     20      0  100.00%
------------------------------------------------------------------------
TOTAL                         36      0     20      0  100.00%
```

- **Statement coverage:** 36 dari 36 statement, atau 100%.
- **Branch coverage:** 20 dari 20 keluaran cabang, atau 100%.
- **Statement terlewat:** 0. **Cabang terlewat:** 0. **Cabang parsial:** 0.

Bukti yang disertakan:

- [Output lengkap 36 kasus](hasil-pytest.txt)
- [Data JSON coverage](coverage.json), termasuk `missing_lines` dan `missing_branches`
- [Laporan HTML](html/index.html), dibuka secara lokal setelah clone/download

[PDF final](latex/main.pdf) dan [sumber LaTeX](latex/main.tex) memuat sebelas
screenshot hasil eksekusi manual dari pengguna. Seluruh PNG asli dalam
`latex/images/` disertakan utuh tanpa crop. Paket pengumpulan pada
`output/pengumpulan-sesi9.zip` menyertakan PDF, LaTeX, dan folder gambar yang
diperlukan untuk kompilasi ulang.

Angka di atas berasal dari eksekusi lokal. Template `contoh/workflow-pytest.yml`
disediakan untuk pengujian pada Python 3.10 dan 3.12, dan belum diaktifkan sebagai
workflow repo.

## 4. Analisis cabang

| Fungsi | Keputusan yang diuji | Jumlah keluaran cabang |
| --- | --- | ---: |
| `hitung_denda` | Hari negatif atau tidak; hari maksimal 7 atau di atas 7 | 4 |
| `batas_peminjaman` | Cocok atau tidak untuk mahasiswa, dosen, dan umum | 6 |
| `pinjam_buku` | Jumlah negatif; mencapai batas; email kosong; stok tersedia; email berhasil | 10 |
| **Total** | Kedua hasil setiap keputusan telah dieksekusi | **20** |

**Tidak ada cabang Python yang belum tercakup** dalam paket `perpustakaan` pada
eksekusi ini. Daftar `missing_branches` dan `missing_lines` untuk `layanan.py`
di JSON kosong. Test stok habis dan buku tidak dikenal membuktikan dua keadaan
yang menghasilkan penolakan, sedangkan test kegagalan email dan timeout
memeriksa pemulihan state melalui rollback.

Coverage 100% ini terbatas pada kode Python milik paket yang diuji. Angka tersebut
tidak mencakup implementasi SQLite atau layanan email eksternal, dan tidak
membuktikan seluruh input mungkin telah diuji. Kontrak parameter mengasumsikan
hari dan jumlah pinjaman berupa bilangan bulat; pemeriksaan tipe dari input
antarmuka, validitas format email lengkap, gangguan koneksi database, dan
peminjaman serentak berada di luar ruang lingkup modul tugas ini. Jumlah
pinjaman aktif juga belum dilacak per anggota dalam database.

Untuk aplikasi nyata, adapter email memerlukan integration test dan kontrak
penyedia layanan. Suite ini memeriksa asumsi adapter melalui mock. Keberhasilan
email yang didefinisikan di sini adalah nilai balik pengirim; rollback database
tidak dapat menarik kembali email yang sudah dikirim oleh layanan eksternal.

## 5. Menjalankan ulang

Dari root repo pada Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe scripts/buat_laporan.py
```

Script membuat ulang output teks, JSON, dan HTML dari satu eksekusi suite dan
mengembalikan exit code PyTest. Konfigurasi `.coveragerc` mengaktifkan branch
coverage dan ambang coverage gabungan 100%.

## Referensi

1. Materi kuliah *Sesi 9 - Unit Testing (PyTest)*, bagian **Tugas Sesi 9**, halaman 10.
2. [Dokumentasi PyTest: yield fixture dan teardown](https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended).
3. [Dokumentasi PyTest: parametrization](https://docs.pytest.org/en/stable/how-to/parametrize.html).
4. [Dokumentasi pytest-cov: reporting](https://pytest-cov.readthedocs.io/en/latest/reporting.html).
5. [Dokumentasi Python: unittest.mock](https://docs.python.org/3/library/unittest.mock.html).
