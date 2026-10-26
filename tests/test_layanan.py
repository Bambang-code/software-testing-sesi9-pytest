"""Uji batas, skenario negatif, transaksi katalog, dan isolasi email."""

from unittest.mock import call

import pytest

from perpustakaan.layanan import (
    batas_peminjaman,
    hitung_denda,
    pinjam_buku,
)


def _stok(katalog, kode_buku="B001"):
    return katalog.execute(
        "SELECT stok FROM buku WHERE kode = ?", (kode_buku,)
    ).fetchone()[0]


@pytest.mark.parametrize(
    "hari, diharapkan",
    [(0, 0), (1, 2_000), (6, 12_000), (7, 14_000), (8, 19_000), (9, 24_000)],
    ids=[
        "tanpa-terlambat",
        "satu-hari",
        "batas-minus-1",
        "batas-7",
        "batas-plus-1",
        "sembilan-hari",
    ],
)
def test_hitung_denda_bva(hari, diharapkan):
    """BVA pada batas 0 hari dan perubahan tarif setelah hari ketujuh."""
    assert hitung_denda(hari) == diharapkan


@pytest.mark.parametrize("hari", [-1, -7])
def test_hari_terlambat_negatif_ditolak(hari):
    with pytest.raises(ValueError, match="^Hari terlambat tidak boleh negatif$"):
        hitung_denda(hari)


@pytest.mark.parametrize(
    "jenis, diharapkan", [("mahasiswa", 3), ("dosen", 5), ("umum", 2)]
)
def test_batas_peminjaman_per_jenis(jenis, diharapkan):
    assert batas_peminjaman(jenis) == diharapkan


@pytest.mark.parametrize("jenis", ["alumni", ""])
def test_jenis_anggota_tidak_dikenal_ditolak(jenis):
    with pytest.raises(ValueError, match="^Jenis anggota tidak dikenal$"):
        batas_peminjaman(jenis)


@pytest.mark.parametrize(
    "jenis, jumlah",
    [
        ("mahasiswa", 0),
        ("mahasiswa", 2),
        ("dosen", 0),
        ("dosen", 4),
        ("umum", 0),
        ("umum", 1),
    ],
)
def test_pinjam_sukses_di_bawah_batas(katalog, pengirim_email, jenis, jumlah):
    hasil = pinjam_buku(
        katalog,
        kode_buku="B001",
        jenis_anggota=jenis,
        jumlah_dipinjam=jumlah,
        email="anggota@example.com",
        kirim_email=pengirim_email,
    )

    assert hasil == "Buku B001 berhasil dipinjam"
    assert _stok(katalog) == 1
    pengirim_email.assert_called_once_with(
        "anggota@example.com", "Peminjaman buku B001 berhasil"
    )


@pytest.mark.parametrize(
    "jenis, jumlah",
    [
        ("mahasiswa", 3),
        ("mahasiswa", 4),
        ("dosen", 5),
        ("dosen", 6),
        ("umum", 2),
        ("umum", 3),
    ],
)
def test_pinjam_pada_dan_di_atas_batas_ditolak(
    katalog, pengirim_email, jenis, jumlah
):
    with pytest.raises(ValueError, match="^Batas peminjaman tercapai$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota=jenis,
            jumlah_dipinjam=jumlah,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_not_called()


@pytest.mark.parametrize("jumlah", [-1, -2])
def test_jumlah_pinjaman_negatif_ditolak(katalog, pengirim_email, jumlah):
    with pytest.raises(ValueError, match="^Jumlah pinjaman tidak boleh negatif$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota="mahasiswa",
            jumlah_dipinjam=jumlah,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_not_called()


def test_pinjam_dengan_jenis_anggota_tidak_dikenal(katalog, pengirim_email):
    with pytest.raises(ValueError, match="^Jenis anggota tidak dikenal$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota="alumni",
            jumlah_dipinjam=0,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_not_called()


@pytest.mark.parametrize("email", ["", "   "])
def test_email_kosong_ditolak(katalog, pengirim_email, email):
    with pytest.raises(ValueError, match="^Email wajib diisi$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota="mahasiswa",
            jumlah_dipinjam=0,
            email=email,
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_not_called()


@pytest.mark.parametrize(
    "kode", ["B002", "B999"], ids=["stok-habis", "kode-tidak-ada"]
)
def test_buku_tidak_tersedia_ditolak(katalog, pengirim_email, kode):
    with pytest.raises(ValueError, match="^Buku tidak tersedia$"):
        pinjam_buku(
            katalog,
            kode_buku=kode,
            jenis_anggota="mahasiswa",
            jumlah_dipinjam=0,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog, "B001") == 2
    assert _stok(katalog, "B002") == 0
    pengirim_email.assert_not_called()


def test_email_gagal_mengembalikan_stok(katalog, pengirim_email):
    pengirim_email.return_value = False

    with pytest.raises(RuntimeError, match="^Pengiriman email gagal$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota="mahasiswa",
            jumlah_dipinjam=0,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_called_once_with(
        "anggota@example.com", "Peminjaman buku B001 berhasil"
    )


def test_email_timeout_mengembalikan_stok(katalog, pengirim_email):
    pengirim_email.side_effect = TimeoutError("Layanan email timeout")

    with pytest.raises(TimeoutError, match="^Layanan email timeout$"):
        pinjam_buku(
            katalog,
            kode_buku="B001",
            jenis_anggota="mahasiswa",
            jumlah_dipinjam=0,
            email="anggota@example.com",
            kirim_email=pengirim_email,
        )

    assert _stok(katalog) == 2
    pengirim_email.assert_called_once_with(
        "anggota@example.com", "Peminjaman buku B001 berhasil"
    )


def test_stok_terakhir_habis_setelah_dipinjam(katalog, pengirim_email):
    katalog.execute("UPDATE buku SET stok = 1 WHERE kode = 'B001'")
    katalog.commit()
    argumen = {
        "kode_buku": "B001",
        "jenis_anggota": "mahasiswa",
        "jumlah_dipinjam": 0,
        "email": "anggota@example.com",
        "kirim_email": pengirim_email,
    }

    assert pinjam_buku(katalog, **argumen) == "Buku B001 berhasil dipinjam"
    assert _stok(katalog) == 0

    with pytest.raises(ValueError, match="^Buku tidak tersedia$"):
        pinjam_buku(katalog, **argumen)

    assert _stok(katalog) == 0
    pengirim_email.assert_called_once_with(
        "anggota@example.com", "Peminjaman buku B001 berhasil"
    )


def test_rollback_tidak_membatalkan_peminjaman_sebelumnya(katalog, pengirim_email):
    pengirim_email.side_effect = [True, False]
    argumen = {
        "kode_buku": "B001",
        "jenis_anggota": "mahasiswa",
        "jumlah_dipinjam": 0,
        "email": "anggota@example.com",
        "kirim_email": pengirim_email,
    }

    assert pinjam_buku(katalog, **argumen) == "Buku B001 berhasil dipinjam"
    with pytest.raises(RuntimeError, match="^Pengiriman email gagal$"):
        pinjam_buku(katalog, **argumen)

    # Peminjaman pertama telah commit, hanya peminjaman kedua yang dibatalkan.
    assert _stok(katalog) == 1
    assert pengirim_email.call_count == 2
    assert pengirim_email.call_args_list == [
        call("anggota@example.com", "Peminjaman buku B001 berhasil"),
        call("anggota@example.com", "Peminjaman buku B001 berhasil"),
    ]
