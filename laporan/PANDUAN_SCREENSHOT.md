# Panduan 11 Screenshot Manual - Tugas Sesi 9

Ambil **11 gambar PNG** yang berfokus pada bukti pengujian: **8 gambar fungsi
unit test, 1 gambar fixture, 1 gambar mock, dan 1 gambar hasil eksekusi beserta
coverage**.

Ketentuan tugas saling mencakup: minimal 8 test sudah mencakup test BVA dengan
`parametrize` dan sedikitnya 2 test negatif menggunakan `pytest.raises`.
Jadi, 8 test dan 2 test negatif tidak harus dijumlahkan sebagai 10 test terpisah.
Pada urutan ini, gambar 01 menunjukkan BVA, sedangkan gambar 04 dan 05 memenuhi
minimal dua test negatif. Proyek tetap mempunyai 14 fungsi test dan 36 kasus;
delapan fungsi pada gambar 01-08 dipilih sebagai bukti minimum.

Simpan semua gambar asli di:

```text
C:\asemester5\asoftest\sesi9\laporan\latex\images
```

Nama file harus sama persis dengan tabel agar sumber LaTeX memasukkannya sesuai
urutan. PDF dan sumber LaTeX adalah dua format dari satu laporan yang sama.

## Persiapan screenshot

1. Buka VS Code melalui **File > Open Folder**, lalu pilih
   `C:\asemester5\asoftest\sesi9`.
2. Maksimalkan jendela. Untuk screenshot kode, tutup panel terminal dan atur zoom
   agar seluruh fungsi, decorator, dan assertion yang diminta tetap terbaca.
3. Gunakan **Ctrl+G**, masukkan nomor baris, lalu Enter. Rentang baris pada tabel
   sudah diverifikasi terhadap kode saat panduan ini disusun.
4. Tekan **Win+Shift+S**, seleksi area editor yang diperlukan. Klik notifikasi
   tangkapan layar untuk membuka Snipping Tool, kemudian **Ctrl+S** dan simpan
   sebagai PNG dengan nama yang sesuai.
5. Sertakan tab nama file dan nomor baris. Screenshot harus memperlihatkan kode
   aktual atau hasil eksekusi aktual, dengan teks yang tidak terpotong.

## Tepat 11 gambar

Gambar 01-08 dan 10 diambil dari
`C:\asemester5\asoftest\sesi9\tests\test_layanan.py`.

| No. | Nama file PNG | Bagian yang ditampilkan dan tujuan |
| --- | --- | --- |
| 01 | `01-test-bva-denda.png` | **Baris 20-34**, fungsi `test_hitung_denda_bva`. Tampilkan `@pytest.mark.parametrize`, nilai 0, 1, 6, 7, 8, 9 hari, dan assertion expected value. Ini bukti test pertama sekaligus BVA. |
| 02 | `02-test-batas-anggota.png` | **Baris 43-47**, fungsi `test_batas_peminjaman_per_jenis`. Tampilkan parameter mahasiswa, dosen, umum, serta assertion batas masing-masing. |
| 03 | `03-test-pinjam-sukses.png` | **Baris 56-81**, fungsi `test_pinjam_sukses_di_bawah_batas`. Tampilkan data parameter, pemanggilan fungsi, assertion hasil dan stok, serta `assert_called_once_with`. |
| 04 | `04-test-negatif-hari.png` | **Baris 37-40**, fungsi `test_hari_terlambat_negatif_ditolak`. Terlihat `pytest.raises(ValueError, ...)` untuk hari negatif. Ini test negatif pertama. |
| 05 | `05-test-negatif-anggota.png` | **Baris 50-53**, fungsi `test_jenis_anggota_tidak_dikenal_ditolak`. Terlihat `pytest.raises(ValueError, ...)` untuk jenis anggota salah. Ini test negatif kedua. |
| 06 | `06-test-negatif-jumlah.png` | **Baris 112-125**, fungsi `test_jumlah_pinjaman_negatif_ditolak`. Tampilkan exception yang diharapkan, stok tetap, dan mock email tidak dipanggil. |
| 07 | `07-test-batas-pinjaman.png` | **Baris 84-109**, fungsi `test_pinjam_pada_dan_di_atas_batas_ditolak`. Tampilkan data tepat pada batas dan satu di atas batas, `pytest.raises`, serta assertion tidak ada efek samping. |
| 08 | `08-test-buku-tidak-tersedia.png` | **Baris 159-175**, fungsi `test_buku_tidak_tersedia_ditolak`. Terlihat kasus stok habis dan kode tidak ada, exception, stok tetap, serta `assert_not_called()`. Ini fungsi test kedelapan. |
| 09 | `09-fixture-yield-cleanup.png` | Buka `C:\asemester5\asoftest\sesi9\tests\conftest.py`, tampilkan **baris 10-23**. Pastikan `@pytest.fixture`, data awal, `commit()`, `yield`, `finally`, dan `koneksi.close()` terlihat. |
| 10 | `10-mock-gagal-timeout.png` | Kembali ke `test_layanan.py`, tampilkan **baris 178-213**. Terlihat `return_value=False`, `side_effect=TimeoutError`, assertion stok kembali, dan verifikasi panggilan. Tutup terminal agar kedua fungsi muat. Mock dibuat pada `conftest.py` baris 26-29; kode ini juga dapat ditampilkan dengan split editor bila tetap terbaca. |
| 11 | `11-hasil-test-coverage.png` | Terminal hasil perintah di bawah. Tampilkan perintah dengan `--cov-branch`, ringkasan **36 passed**, serta tabel **36 statement**, **20 branch**, dan **100.00%**. Ini bukti eksekusi dan coverage. |

Tidak perlu menambahkan gambar struktur folder, kode aplikasi, atau halaman HTML
ke dalam urutan 11 gambar ini. Kode aplikasi tetap tersedia di repo, dan
pembahasannya tetap ada di laporan.

## Perintah untuk gambar 11

Buka **Terminal > New Terminal** di VS Code, pilih PowerShell, lalu jalankan:

```powershell
Set-Location -LiteralPath 'C:\asemester5\asoftest\sesi9'
Clear-Host
.\.venv\Scripts\python.exe -m pytest -q --cov=perpustakaan --cov-branch --cov-report=term-missing --cov-report=html
```

Opsi `-q` membuat output ringkas agar perintah, tabel coverage, dan ringkasan test
muat dalam satu screenshot. Lebarkan terminal bila ada kolom yang terpotong.
Tunggu proses selesai, lalu simpan tangkapan layar sebagai
`11-hasil-test-coverage.png`.

Hasil yang sudah diverifikasi pada proyek ini adalah **36 passed** dengan
statement dan branch coverage **100%**. Test negatif juga seharusnya **PASSED**:
`pytest.raises` menyatakan test lulus jika exception yang diharapkan benar terjadi.
Ambil output eksekusi aktual; jangan mengetik ulang tabel sebagai penggantinya.

## Setelah 11 gambar tersimpan

Periksa ada tepat 11 file PNG dengan nama sesuai tabel di
`C:\asemester5\asoftest\sesi9\laporan\latex\images`. Buka setiap gambar dan
pastikan isinya terbaca. **PDF yang tersedia sekarang masih draf sampai seluruh
screenshot manual asli dimasukkan dan laporan dikompilasi ulang.**

Dari root proyek, jalankan:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\kompilasi_laporan.ps1
```

Hasil kompilasi adalah `laporan\latex\main.pdf`; sumbernya
`laporan\latex\main.tex`. Script menyebutkan gambar yang belum ada dan menolak
kompilasi final jika belum lengkap. Opsi `-Draf` hanya untuk pratinjau dengan
penanda gambar kosong.

Kumpulkan **11 gambar asli** dan **satu laporan dalam format PDF serta LaTeX**.
Sertakan folder `images` bersama sumber LaTeX agar laporan dapat dikompilasi
kembali. Compiler portabel sudah tersedia di komputer ini; jika memindahkan
proyek, folder `laporan\latex` juga dapat diunggah ke Overleaf.
