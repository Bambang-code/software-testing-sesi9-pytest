"""Fixture terisolasi: katalog baru dan pengganti layanan email tiap test."""

from unittest.mock import Mock

import pytest

from perpustakaan.layanan import buat_katalog


@pytest.fixture
def katalog():
    """Sediakan database sementara dan tutup koneksinya setelah test."""
    koneksi = buat_katalog()
    try:
        koneksi.executemany(
            "INSERT INTO buku (kode, stok) VALUES (?, ?)",
            [("B001", 2), ("B002", 0)],
        )
        # Data awal harus selesai disimpan sebelum transaksi peminjaman diuji.
        koneksi.commit()
        yield koneksi
    finally:
        koneksi.close()


@pytest.fixture
def pengirim_email():
    """Tidak ada email sungguhan yang dikirim selama pengujian."""
    return Mock(name="kirim_email", return_value=True)
