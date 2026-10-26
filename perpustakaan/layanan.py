"""Logika perpustakaan dengan katalog lokal dan dependensi email yang disuntikkan.

Parameter hari dan jumlah pinjaman menggunakan bilangan bulat. Jenis anggota
yang diterima adalah ``mahasiswa``, ``dosen``, dan ``umum`` (huruf kecil).
Tidak ada koneksi jaringan atau pengiriman email sungguhan di modul ini.
"""

import sqlite3
from typing import Callable


def hitung_denda(hari_terlambat: int) -> int:
    """Hitung rupiah: 7 hari pertama Rp2.000/hari, sisanya Rp5.000/hari.

    Nol hari berarti tidak ada denda. Hari negatif ditolak dengan ValueError.
    Tarif bertingkat: keterlambatan 8 hari = 7 * 2.000 + 1 * 5.000.
    """
    if hari_terlambat < 0:
        raise ValueError("Hari terlambat tidak boleh negatif")
    if hari_terlambat <= 7:
        return hari_terlambat * 2_000
    return 7 * 2_000 + (hari_terlambat - 7) * 5_000


def batas_peminjaman(jenis_anggota: str) -> int:
    """Kembalikan batas pinjaman aktif: mahasiswa 3, dosen 5, umum 2."""
    if jenis_anggota == "mahasiswa":
        return 3
    if jenis_anggota == "dosen":
        return 5
    if jenis_anggota == "umum":
        return 2
    raise ValueError("Jenis anggota tidak dikenal")


def buat_katalog() -> sqlite3.Connection:
    """Buat katalog SQLite dalam memori; pemanggil wajib menutup koneksinya."""
    katalog = sqlite3.connect(":memory:")
    katalog.execute(
        """
        CREATE TABLE buku (
            kode TEXT PRIMARY KEY,
            stok INTEGER NOT NULL CHECK (stok >= 0)
        )
        """
    )
    return katalog


def pinjam_buku(
    katalog: sqlite3.Connection,
    *,
    kode_buku: str,
    jenis_anggota: str,
    jumlah_dipinjam: int,
    email: str,
    kirim_email: Callable[[str, str], bool],
) -> str:
    """Pinjam satu buku dan kirim konfirmasi melalui dependensi email.

    Validasi dilakukan sebelum stok berubah. Stok hanya berkurang jika buku
    tersedia dan pengirim email mengembalikan True. Nilai False atau exception
    dari pengirim membatalkan transaksi SQLite dan mengembalikan stok.
    Jumlah pinjaman aktif disediakan pemanggil untuk anggota yang bersangkutan.
    """
    if jumlah_dipinjam < 0:
        raise ValueError("Jumlah pinjaman tidak boleh negatif")
    batas = batas_peminjaman(jenis_anggota)
    if jumlah_dipinjam >= batas:
        raise ValueError("Batas peminjaman tercapai")
    if not email.strip():
        raise ValueError("Email wajib diisi")

    with katalog:
        perubahan = katalog.execute(
            "UPDATE buku SET stok = stok - 1 WHERE kode = ? AND stok > 0",
            (kode_buku,),
        )
        if perubahan.rowcount != 1:
            raise ValueError("Buku tidak tersedia")

        pesan = f"Peminjaman buku {kode_buku} berhasil"
        if not kirim_email(email, pesan):
            raise RuntimeError("Pengiriman email gagal")

    return f"Buku {kode_buku} berhasil dipinjam"
