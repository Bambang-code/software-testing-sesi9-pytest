# Panduan 11 Screenshot Hasil Test - Tugas Sesi 9

Kesebelas screenshot manual dari pengguna sudah disertakan secara utuh tanpa
crop pada laporan PDF final. PNG asli berada di `laporan/latex/images/`, bersama
sumber LaTeX yang merujuk gambar tersebut. Panduan ini menyediakan perintah untuk
mengulangi **11 hasil eksekusi di terminal**: delapan hasil fungsi test, satu hasil
setup/teardown fixture, satu hasil test mock, dan satu hasil suite beserta coverage.

Minimal delapan test sudah dapat mencakup test BVA dengan `parametrize` serta
minimal dua test negatif menggunakan `pytest.raises`. Pada urutan ini, gambar 01
memenuhi BVA, sedangkan gambar 04 dan 05 menunjukkan dua test negatif.
Proyek mempunyai 14 fungsi test dan 36 kasus setelah parametrization; delapan
fungsi pada gambar 01-08 dipilih sebagai bukti minimum.

## Persiapan dan cara menyimpan

1. Buka folder `C:\asemester5\asoftest\sesi9` di VS Code.
2. Pilih **Terminal > New Terminal**, gunakan PowerShell, lalu jalankan:

   ```powershell
   Set-Location -LiteralPath 'C:\asemester5\asoftest\sesi9'
   ```

3. Lebarkan dan tinggikan panel terminal agar perintah, nama test, status
   `PASSED`, dan ringkasan hasil terbaca. Jalankan satu blok perintah di bawah
   untuk setiap gambar; `Clear-Host` membersihkan hasil sebelumnya.
4. Tunggu perintah selesai, tekan **Win+Shift+S**, lalu seleksi area terminal.
   Klik notifikasi tangkapan, tekan **Ctrl+S**, dan simpan sebagai PNG dengan nama
   yang ditentukan. Simpan semua gambar di:

   ```text
   C:\asemester5\asoftest\sesi9\laporan\latex\images
   ```

5. Gunakan output aktual. Jangan mengetik ulang hasil sebagai pengganti eksekusi.
   Durasi test boleh berbeda dari eksekusi sebelumnya.

## Gambar 01 - Hasil test BVA denda

Nama file: `01-test-bva-denda.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_hitung_denda_bva
```

Tampilkan enam kasus BVA berstatus `PASSED` dan ringkasan **6 passed**. Kasus
mencakup 0, 1, 6, 7, 8, dan 9 hari, termasuk batas perubahan tarif.

## Gambar 02 - Hasil test batas anggota

Nama file: `02-test-batas-anggota.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_batas_peminjaman_per_jenis
```

Tampilkan hasil mahasiswa, dosen, dan umum beserta ringkasan **3 passed**.

## Gambar 03 - Hasil test peminjaman sukses

Nama file: `03-test-pinjam-sukses.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_pinjam_sukses_di_bawah_batas
```

Tampilkan hasil peminjaman di bawah batas masing-masing jenis anggota dan
ringkasan **6 passed**. Test memeriksa hasil, pengurangan stok, serta interaksi
pengirim email.

## Gambar 04 - Hasil test negatif hari

Nama file: `04-test-negatif-hari.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_hari_terlambat_negatif_ditolak
```

Tampilkan kedua kasus hari negatif berstatus `PASSED` dan **2 passed**. Test
negatif tetap lulus karena `pytest.raises` menerima exception yang diharapkan.

## Gambar 05 - Hasil test negatif anggota

Nama file: `05-test-negatif-anggota.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_jenis_anggota_tidak_dikenal_ditolak
```

Tampilkan kedua kasus jenis anggota yang ditolak dan ringkasan **2 passed**.
Ini bukti hasil test negatif kedua dengan `pytest.raises`.

## Gambar 06 - Hasil test jumlah pinjaman negatif

Nama file: `06-test-negatif-jumlah.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_jumlah_pinjaman_negatif_ditolak
```

Tampilkan hasil kedua jumlah negatif dan **2 passed**. Assertion juga memastikan
stok tetap serta pengirim email tidak dipanggil.

## Gambar 07 - Hasil test batas peminjaman

Nama file: `07-test-batas-pinjaman.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_pinjam_pada_dan_di_atas_batas_ditolak
```

Tampilkan kasus tepat pada batas dan di atas batas untuk mahasiswa, dosen, dan
umum, dengan ringkasan **6 passed**.

## Gambar 08 - Hasil test buku tidak tersedia

Nama file: `08-test-buku-tidak-tersedia.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py::test_buku_tidak_tersedia_ditolak
```

Tampilkan kasus `stok-habis` dan `kode-tidak-ada`, keduanya `PASSED`, dengan
ringkasan **2 passed**. Ini hasil fungsi test kedelapan.

## Gambar 09 - Hasil setup dan teardown fixture

Nama file: `09-fixture-yield-cleanup.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v --setup-show tests/test_layanan.py::test_stok_terakhir_habis_setelah_dipinjam
```

Tampilkan **SETUP F katalog**, hasil test, **TEARDOWN F katalog**, dan ringkasan
**1 passed**. Opsi `--setup-show` memperlihatkan fixture dibuat dan teardown
dijalankan. Implementasi fixture memakai `yield` dan menutup koneksi pada
`finally`; nama `close()` tidak dicetak oleh trace bawaan PyTest.

## Gambar 10 - Hasil test mock email gagal dan timeout

Nama file: `10-mock-gagal-timeout.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -v tests/test_layanan.py -k "email_gagal or email_timeout"
```

Tampilkan `test_email_gagal_mengembalikan_stok` dan
`test_email_timeout_mengembalikan_stok` berstatus `PASSED`, dengan ringkasan
**2 passed**. Kasus lain ditandai `deselected` karena disaring oleh `-k`.
Hasil lulus berarti assertion rollback dan verifikasi mock berhasil; PyTest
tidak mencetak argumen panggilan mock secara otomatis ketika assertion lulus.

## Gambar 11 - Hasil seluruh test dan branch coverage

Nama file: `11-hasil-test-coverage.png`.

```powershell
Clear-Host
.\.venv\Scripts\python.exe -m pytest -q --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html
```

Tampilkan perintah yang memuat `--cov-branch`, tabel **36 statement**, **20
branch**, **100.00%**, serta ringkasan **36 passed**. Opsi `-q` meringkas hasil
agar tabel dan ringkasan muat dalam satu screenshot. Lebarkan terminal jika
kolom terpotong. Ini hasil suite lengkap, termasuk test yang tidak diambil
screenshotnya satu per satu.

## PDF final dan kompilasi ulang

PDF final sudah memuat tepat 11 screenshot hasil eksekusi asli dari folder
`C:\asemester5\asoftest\sesi9\laporan\latex\images`. Setiap gambar dipertahankan
utuh tanpa crop. Nama file sesuai urutan di atas agar sumber LaTeX dapat
dikompilasi ulang dengan semua bukti yang sama. Seluruh halaman menggunakan
A4 portrait (210 x 297 mm), dengan screenshot utuh yang diskalakan proporsional.

Dari root proyek, jalankan:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\kompilasi_laporan.ps1
```

Hasilnya `laporan\latex\main.pdf`, dengan sumber `laporan\latex\main.tex`.
Jika gambar pada revisi berikutnya belum lengkap, script menyebutkan gambar
yang belum ada dan menolak kompilasi final. Opsi `-Draf` bersifat opsional untuk
pratinjau revisi yang masih memiliki gambar kosong.

Kumpulkan **11 gambar hasil eksekusi asli** dan **satu laporan dalam format PDF
serta LaTeX**. Sertakan folder `images/` dan `assets/` bersama sumber LaTeX agar
laporan dan logo pada cover dapat dikompilasi kembali. Logo universitas berada
di `assets/logo-ukwms.png`, terpisah dari sebelas screenshot hasil test.
Compiler portabel sudah tersedia di komputer ini; jika
memindahkan proyek, folder `laporan\latex` juga dapat diunggah ke Overleaf.

Paket `output\pengumpulan-sesi9.zip` menggabungkan `main.pdf`, `main.tex`, folder
`images/` berisi 11 PNG asli, serta `assets/` berisi logo cover. Isi paket lengkap
berjumlah 14 file, sehingga sumber laporan tetap portabel.
