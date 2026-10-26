# Panduan 11 Screenshot Manual - Tugas Sesi 9

Ambil **11 gambar PNG** dari kode dan hasil eksekusi di komputer sendiri. Simpan
semuanya di:

```text
C:\asemester5\asoftest\sesi9\laporan\latex\images
```

Nama file di tabel harus sama persis agar gambar dapat dimasukkan ke laporan
LaTeX sesuai urutannya. PDF dan sumber LaTeX merupakan dua format dari laporan
yang sama.

## Persiapan tampilan

1. Buka VS Code, pilih **File > Open Folder**, lalu buka
   `C:\asemester5\asoftest\sesi9`.
2. Maksimalkan jendela. Untuk screenshot kode, tutup panel terminal agar area kode
   lebih luas. Atur zoom sehingga teks terbaca dan bagian yang diminta muat.
3. Gunakan **Ctrl+G**, ketik nomor baris, lalu Enter untuk menuju bagian kode.
   Nomor baris di bawah sudah diperiksa berdasarkan file tugas saat ini.
4. Tekan **Win+Shift+S**, pilih area yang ingin diambil. Klik notifikasi hasil
   tangkapan untuk membuka Snipping Tool, lalu **Ctrl+S** dan simpan dengan nama
   yang ditentukan di folder `images` di atas.
5. Sertakan tab nama file dan nomor baris pada screenshot kode. Pastikan teks
   penting tidak terpotong, terutama assertion, `yield`, dan cleanup.

## Urutan gambar

| No. | Nama file | Tampilan yang diambil |
| --- | --- | --- |
| 01 | `01-struktur.png` | Explorer VS Code: tampilkan folder `perpustakaan`, `tests`, `laporan`, serta file `pytest.ini`, `.coveragerc`, dan `requirements-dev.txt`. Buka folder `perpustakaan` dan `tests` agar file Python terlihat. Folder `.venv` cukup dilipat. |
| 02 | `02-fungsi-denda-batas.png` | Buka `C:\asemester5\asoftest\sesi9\perpustakaan\layanan.py`, tampilkan **baris 12-33**. Terlihat fungsi `hitung_denda` dan `batas_peminjaman` beserta percabangannya. |
| 03 | `03-fungsi-pinjam.png` | Masih di `layanan.py`, tampilkan **baris 50-86**: parameter `pinjam_buku`, validasi, pengurangan stok, pemanggilan email, dan hasil. Bila perlu lipat docstring baris 59-65 agar kode logika tetap terbaca. |
| 04 | `04-fixture-cleanup.png` | Buka `C:\asemester5\asoftest\sesi9\tests\conftest.py`, tampilkan **baris 1-29**. Pastikan `@pytest.fixture`, penyemaian data, `commit()`, `yield`, `finally`, `close()`, serta `Mock(..., return_value=True)` terlihat. |
| 05 | `05-parametrize-bva.png` | Buka `C:\asemester5\asoftest\sesi9\tests\test_layanan.py`, tampilkan **baris 20-34**. Terlihat `@pytest.mark.parametrize`, data 0, 1, 6, 7, 8, 9 hari, dan assertion hasil denda. |
| 06 | `06-test-negatif.png` | Di `test_layanan.py`, tampilkan **baris 37-53**. Terlihat dua fungsi test negatif dengan `pytest.raises`: hari terlambat negatif dan jenis anggota tidak dikenal. |
| 07 | `07-mock-email.png` | Di `test_layanan.py`, tampilkan **baris 56-81**. Terlihat test peminjaman sukses, injeksi `pengirim_email`, assertion stok, dan `assert_called_once_with`. |
| 08 | `08-mock-gagal-timeout.png` | Di `test_layanan.py`, tampilkan **baris 178-213**. Terlihat pengaturan `return_value=False` dan `side_effect=TimeoutError`, `pytest.raises`, serta assertion stok kembali. Tutup panel terminal agar kedua fungsi muat. |
| 09 | `09-hasil-pytest.png` | Terminal setelah menjalankan perintah test pada bagian berikut. Tampilkan deretan hasil `PASSED` dan ringkasan **36 passed**. Gulir sampai ringkasan terlihat; tidak perlu memaksa seluruh 36 baris muat dalam satu gambar. |
| 10 | `10-coverage-terminal.png` | Terminal setelah menjalankan perintah coverage di bawah. Sertakan perintah `--cov-branch`, tabel coverage dengan **36 statement**, **20 branch**, **100.00%**, dan ringkasan **36 passed**. |
| 11 | `11-coverage-html.png` | Browser yang membuka `htmlcov/index.html`. Tampilkan judul laporan, baris `perpustakaan/layanan.py`, dan total **100%**. Pastikan tabel coverage terbaca. |

## Perintah untuk gambar 09

Buka terminal PowerShell di VS Code (**Terminal > New Terminal**), lalu jalankan:

```powershell
Set-Location -LiteralPath 'C:\asemester5\asoftest\sesi9'
.\.venv\Scripts\python.exe -m pytest -v
```

Tunggu sampai selesai, lalu ambil `09-hasil-pytest.png`. Hasil yang sudah
diverifikasi pada proyek ini adalah **36 passed**. Test negatif juga seharusnya
**PASSED**: `pytest.raises` membuktikan exception yang diharapkan benar terjadi.

## Perintah untuk gambar 10

Gunakan `-q` agar hasil ringkas dan tabel coverage muat dalam satu gambar:

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -q --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html
```

Tunggu sampai selesai. Hasil yang sudah diverifikasi:

```text
Name                       Stmts   Miss Branch BrPart    Cover
perpustakaan\__init__.py       0      0      0      0  100.00%
perpustakaan\layanan.py       36      0     20      0  100.00%
TOTAL                         36      0     20      0  100.00%
```

Ambil `10-coverage-terminal.png` dari hasil terminal aktual. Lebarkan terminal
bila kolom tabel terpotong. Jangan mengetik ulang tabel sebagai pengganti hasil
eksekusi.

## Membuka laporan untuk gambar 11

Setelah perintah coverage selesai, jalankan:

```powershell
Start-Process .\htmlcov\index.html
```

Browser akan membuka laporan HTML lokal. Maksimalkan jendela dan ambil
`11-coverage-html.png` pada halaman ringkasan. Tampilan browser dapat menggunakan
garis miring `/` atau `\` untuk nama file; keduanya menunjuk modul yang sama.

## Setelah semua screenshot disimpan

Periksa folder `C:\asemester5\asoftest\sesi9\laporan\latex\images`: harus ada
tepat 11 file PNG sesuai tabel. Buka setiap gambar untuk memastikan isinya
terbaca. Setelah gambar tersedia, kompilasi ulang laporan LaTeX agar PDF memuat
seluruh bukti asli. Kumpulkan 11 gambar dan satu laporan dalam dua format:
`.pdf` serta `.tex` beserta folder gambar yang dirujuknya.

Jalankan dari root proyek:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\kompilasi_laporan.ps1
```

Hasilnya `laporan\latex\main.pdf`, dengan sumber `laporan\latex\main.tex`.
Script akan menyebutkan gambar yang belum ada dan menghentikan kompilasi final.
Untuk melihat draf dengan penanda gambar kosong, tambahkan `-Draf` pada perintah.
Compiler portabel sudah tersedia di komputer ini; bila memindahkan proyek,
folder `laporan\latex` juga bisa diunggah ke Overleaf untuk dikompilasi.
