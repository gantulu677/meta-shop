# Meta Shop — Meta Product Catalog Feed

> **DEMO / NON-PRODUCTION.** CSV berisi enam varian contoh, URL `example.com`, serta harga, stok, dan spesifikasi dummy. Jangan unggah sebagai feed toko produksi.

Repository ini menyediakan contoh feed CSV Meta, dokumentasi field, dan validator.

## Struktur

```text
meta-shop/
├── README.md
├── meta-product-feed.csv
├── docs/meta-product-feed.md
├── scripts/validate-feed.py
└── .github/workflows/validate-feed.yml
```

## Validasi lokal

Memerlukan Python 3.10+; tidak membutuhkan dependency pihak ketiga.

```bash
python scripts/validate-feed.py
python scripts/validate-feed.py --production
```

Mode default mengizinkan placeholder demo dan menampilkannya sebagai warning. Mode `--production` menolak URL `example.com` serta penanda sample. Lulus validator bukan pengganti pengujian feed melalui Commerce Manager.

## Kebijakan schema dan inventory

- Header CSV 33 kolom; nama dan urutannya adalah kontrak schema repository.
- Setiap varian harus memiliki `id` unik; varian satu produk berbagi `item_group_id`.
- `inventory` dipertahankan sebagai kolom legacy demi kompatibilitas, tetapi wajib kosong. Validator menolak nilai yang diisi.
- `quantity_to_sell_on_facebook` adalah satu-satunya field kuantitas aktif; bila diisi harus bilangan bulat non-negatif.
- Jangan hapus kolom `inventory` sebelum konsumen lama dimigrasikan dan perubahan schema disetujui.

## Checklist sebelum produksi

1. Ganti semua URL placeholder dengan URL produk dan gambar yang dapat diakses publik.
2. Ganti seluruh data contoh dengan detail produk, harga, stok, dan promosi yang benar.
3. Verifikasi identifier produk dan taxonomy.
4. Jalankan validator dengan `--production`.
5. Uji feed dan selesaikan item diagnostics di Commerce Manager.

## Dokumentasi

Lihat [Meta Product Catalog Feed Field Reference](docs/meta-product-feed.md). Persyaratan dapat berbeda menurut katalog, negara, checkout, dan channel; dokumentasi Meta dan Commerce Manager tetap menjadi acuan akhir.
