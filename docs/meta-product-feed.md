# Meta Product Catalog Feed — Field Reference

> **Scope:** dokumentasi untuk seluruh 33 kolom yang saat ini ada di `meta-product-feed.csv`.
>
> **Status:** panduan implementasi feed CSV katalog Meta, bukan jaminan bahwa setiap field berlaku untuk semua tipe katalog, negara, checkout, atau channel. Persyaratan akhir harus divalidasi di Commerce Manager untuk katalog yang digunakan.
>
> **Last reviewed:** 19 November 2026.

## 1. Current feed schema

CSV repository saat ini memiliki 33 kolom:

```csv
id,title,description,rich_text_description,availability,condition,price,link,image_link,additional_image_link,brand,gtin,mpn,google_product_category,fb_product_category,product_type,sale_price,sale_price_effective_date,item_group_id,color,size,material,pattern,gender,age_group,inventory,quantity_to_sell_on_facebook,status,custom_label_0,custom_label_1,custom_label_2,custom_label_3,custom_label_4
```

Kolom `inventory` masih tercantum karena ada pada file CSV saat ini. Untuk feed baru, gunakan `quantity_to_sell_on_facebook` sebagai field kuantitas yang direkomendasikan Meta. Jangan mengirim dua sumber kuantitas yang saling bertentangan.

## 2. Requirement levels

| Level | Meaning |
|---|---|
| Required | Termasuk dalam daftar required Meta Catalog Fields untuk produk standar. |
| Conditional | Wajib hanya untuk kategori, checkout, negara, atau channel tertentu. |
| Optional | Didokumentasikan Meta, tetapi tidak wajib secara universal. |
| Legacy | Field lama yang sedang digantikan; hindari untuk implementasi feed baru. |
| Verify | Perlu dikonfirmasi pada metode ingest atau konfigurasi katalog tertentu sebelum digunakan. |

### Required fields

Dokumentasi Meta Catalog Fields saat ini mencantumkan field berikut sebagai required untuk produk standar: `id`, `title`, `description`, `availability`, `condition`, `price`, `link`, `image_link`, dan `brand`.

Ada panduan Meta Data Feed Help Center yang lebih lama yang menyebut brand, MPN, atau GTIN sebagai alternatif identifikasi. Karena sumber dan alur feed dapat berbeda, dokumen ini mengikuti daftar required pada Meta Catalog Fields yang lebih baru: isi `brand`, dan sertakan GTIN/MPN bila tersedia serta valid. Jangan menganggap GTIN atau MPN menggantikan `brand` tanpa konfirmasi pada persyaratan katalog target.

## 3. Field-by-field reference

### 3.1 Product identity and content

| Field | Level | Purpose and guidance | Limit / format |
|---|---|---|---|
| `id` | Required | ID item unik dan stabil; idealnya SKU. Setiap varian memiliki ID sendiri. Samakan dengan content ID Pixel/Conversions API bila dipakai untuk pencocokan katalog. | Maks. 100 karakter |
| `title` | Required | Nama produk yang spesifik dan mudah dibaca. | Maks. 200 karakter; disarankan ≤65 karakter agar tidak terpotong |
| `description` | Required | Deskripsi plain text, unik, informatif, dan bukan sekadar pengulangan judul. Jangan masukkan HTML. Tetap isi sebagai fallback walaupun rich text tersedia. | Maks. 9.999 karakter |
| `rich_text_description` | Optional | Deskripsi HTML/rich text. Saat tersedia, dapat dipakai untuk tampilan deskripsi kaya di Shop; plain-text `description` tetap harus ada sebagai fallback. Tidak didukung untuk catalog ads. | Maks. 9.999 karakter |

### 3.2 Availability, price, and destination

| Field | Level | Purpose and guidance | Limit / format |
|---|---|---|---|
| `availability` | Required | Status ketersediaan stok. Untuk feed CSV, gunakan nilai `in stock` atau `out of stock` sesuai spesifikasi Catalog Fields. Jangan menyalin seluruh enum dari Product Item API ke CSV. | Enum feed: `in stock`, `out of stock` |
| `condition` | Required | Kondisi produk. | Feed values: `new`, `refurbished`, `used` |
| `price` | Required | Harga reguler. Format feed: angka, spasi, kode mata uang ISO 4217, misalnya `24999000 IDR`. Gunakan titik untuk desimal; tanpa simbol mata uang atau pemisah ribuan lokal. | `amount ISO_CURRENCY` |
| `link` | Required | URL langsung ke halaman produk pada situs merchant. Halaman harus merepresentasikan produk/varian pada baris tersebut. | URL HTTP(S) yang valid |
| `image_link` | Required | URL gambar utama produk yang dapat diakses publik. | JPEG/PNG; minimum 500 × 500 px; maksimum 8 MB |
| `additional_image_link` | Optional | URL gambar tambahan produk. Maksimum 20 gambar dan total panjang field 2.000 karakter. | Pisahkan URL dengan koma, titik koma, spasi, atau pipe (`|`); bungkus seluruh daftar dalam satu quoted CSV cell |
| `sale_price` | Optional | Harga promosi, memakai format yang sama dengan `price`; harus lebih rendah dari harga reguler. | `amount ISO_CURRENCY` |
| `sale_price_effective_date` | Optional | Rentang waktu promosi dengan timestamp mulai dan selesai dipisahkan `/`. Sertakan timezone, misalnya `2026-11-27T00:00+07:00/2026-11-30T23:59+07:00`. | `start/end` |
| `status` | Optional | Status item katalog pada feed: `active` atau `archived`. Jangan menyamakan field ini dengan `visibility` pada Product Item API. | Feed values: `active`, `archived` |

Jika URL gambar diganti setelah feed diproses, gunakan URL gambar baru atau pastikan mekanisme refresh katalog mengenali perubahan gambar. Jangan mengandalkan perubahan file pada URL yang sama akan langsung memicu pemrosesan ulang gambar.

### 3.3 Brand and product identifiers

| Field | Level | Purpose and guidance | Limit / format |
|---|---|---|---|
| `brand` | Required | Nama brand/manufacturer. Diisi sesuai daftar required pada Meta Catalog Fields. | Teks |
| `gtin` | Optional / recommended when available | Global Trade Item Number seperti UPC, EAN, JAN, atau ISBN yang benar-benar ditetapkan untuk produk. Jangan membuat atau memakai ulang GTIN. | Identifier valid |
| `mpn` | Optional / recommended when available | Manufacturer Part Number yang ditetapkan produsen. Jangan menggantinya dengan SKU internal kecuali SKU tersebut memang MPN produsen. | Identifier valid |

**Catatan perbedaan sumber:** sejumlah panduan feed lama menyebut `brand`, `mpn`, atau `gtin` sebagai alternatif. Meta Catalog Fields yang menjadi acuan field pada dokumen ini mencantumkan `brand` sebagai required dan GTIN/MPN sebagai identifier tambahan. Ikuti validasi Commerce Manager bila instruksi katalog tertentu berbeda.

### 3.4 Categorization and variants

| Field | Level | Purpose and guidance | Limit / format |
|---|---|---|---|
| `google_product_category` | Optional / conditional | Kategori dari Google Product Taxonomy. Meta Catalog Fields mencantumkannya sebagai optional; kebutuhan tambahan dapat bergantung pada checkout/channel atau instruksi katalog tertentu. | Maks. 750 karakter |
| `fb_product_category` | Optional | Kategori dari taksonomi Meta/Facebook. Gunakan kategori paling spesifik yang sesuai; feed dapat menggunakan nilai kategori yang dikenali, seperti nama atau ID sesuai spesifikasi. | Meta taxonomy |
| `product_type` | Optional | Jalur kategori buatan merchant, misalnya `Electronics > Phones > Smartphones`. Bukan pengganti taxonomy platform jika taxonomy diwajibkan. | Maks. 750 karakter |
| `item_group_id` | Optional | ID bersama untuk mengelompokkan varian satu produk induk. Semua varian memakai nilai yang sama, sedangkan `id` tiap varian tetap unik. | Maks. 100 karakter |
| `color` | Optional / category-dependent | Warna varian; gunakan nilai konsisten dan akurat. | Maks. 200 karakter |
| `size` | Conditional | Ukuran produk. Dapat diwajibkan untuk kategori tertentu di Shops, khususnya pakaian dan sepatu; bukan persyaratan umum untuk varian kapasitas penyimpanan ponsel. | Maks. 200 karakter |
| `material` | Optional / category-dependent | Material atau komposisi produk bila relevan. | Maks. 200 karakter |
| `pattern` | Optional / category-dependent | Motif/pola produk bila relevan. | Maks. 100 karakter |
| `gender` | Optional / category-dependent | Target gender bila relevan dengan kategori produk. Gunakan nilai taxonomy yang sesuai. | Nilai taxonomy |
| `age_group` | Optional / category-dependent | Kelompok usia bila relevan. Gunakan nilai taxonomy yang sesuai, misalnya `adult`, `kids`, atau `infant`. | Nilai taxonomy |

### 3.5 Inventory and checkout

| Field | Level | Purpose and guidance |
|---|---|---|
| `quantity_to_sell_on_facebook` | Optional / checkout-dependent | Field kuantitas yang direkomendasikan Meta untuk jumlah yang tersedia dijual di Facebook. Gunakan untuk integrasi feed baru bila sesuai dengan channel/checkout katalog. Pastikan nilainya sinkron dengan stok aktual. |
| `inventory` | Legacy | Meta menyatakan `inventory` digantikan oleh `quantity_to_sell_on_facebook`. Nama lama masih dapat didukung selama masa transisi, tetapi jangan gunakan untuk implementasi baru. Hapus dari skema feed baru setelah kompatibilitas dan migrasi katalog dipastikan. |

**Kebijakan schema repository:** kolom `inventory` dipertahankan pada header 33 kolom untuk kompatibilitas, tetapi wajib kosong di semua baris; validator menolak nilai non-empty. Kolom ini tidak boleh menjadi sumber stok baru. `quantity_to_sell_on_facebook` adalah satu-satunya kolom kuantitas yang digunakan; jika diisi, nilainya bilangan bulat non-negatif. Jangan hapus kolom legacy sebelum konsumen feed lama dimigrasikan dan perubahan schema disetujui.

Jangan mengirim nilai stok berbeda pada `inventory` dan `quantity_to_sell_on_facebook`. Untuk katalog lama, periksa aturan migrasi dan hasil diagnostik sebelum menghapus field legacy.

### 3.6 Custom labels

| Field | Level | Purpose and guidance | Limit |
|---|---|---|---|
| `custom_label_0` | Optional | Label teks merchant untuk segmentasi/organisasi item. | Maks. 100 karakter |
| `custom_label_1` | Optional | Label teks merchant kedua. | Maks. 100 karakter |
| `custom_label_2` | Optional | Label teks merchant ketiga. | Maks. 100 karakter |
| `custom_label_3` | Optional | Label teks merchant keempat. | Maks. 100 karakter |
| `custom_label_4` | Optional | Label teks merchant kelima. | Maks. 100 karakter |

Custom labels adalah lima field scalar terpisah, bukan daftar yang dipisahkan titik koma atau pipe. Contoh `flash_sale`, `discount`, dan `black_friday` hanyalah klasifikasi internal merchant; label tidak membuat atau mengaktifkan promosi Meta. Meta juga mendokumentasikan `internal_label` untuk pengelompokan/filter product set; pertimbangkan field tersebut jika workflow mendukungnya.

## 4. `rich_text_description` HTML guidance

Meta Catalog Fields mencantumkan tag HTML berikut sebagai tag yang didukung untuk rich text:

- Structure/content: `<form>`, `<fieldset>`, `<div>`, `<span>`, `<section>`, `<header>`
- Headings: `<h1>` sampai `<h6>`
- Tables: `<table>`, `<tbody>`, `<tfoot>`, `<thead>`, `<td>`, `<th>`, `<tr>`
- Lists: `<ul>`, `<li>`, `<ol>`, `<dl>`, `<dd>`, `<dt>`
- Formatting: `<b>`, `<u>`, `<i>`, `<em>`, `<strong>`, `<title>`, `<small>`, `<br>`, `<p>`, `<sub>`, `<sup>`, `<pre>`, `<q>`, `<s>`

Daftar ini adalah allow-list rujukan Meta, bukan jaminan bahwa setiap kombinasi tag tampil identik di semua placement. Meta dapat menghapus atribut HTML seperti styling. Jangan mengandalkan CSS, JavaScript, embed, event handler, atau elemen interaktif. Tag `<html>` yang tampak pada contoh wrapper dokumentasi bukan bagian dari allow-list eksplisit; `<body>` juga tidak tercantum. Karena itu, hindari wrapper tersebut dan kirim fragmen HTML sederhana.

Contoh fragmen yang disarankan:

```html
<h2>Product Name</h2>
<p>Short product description.</p>

<h3>Product Details</h3>
<ul>
  <li><strong>Brand:</strong> Example Brand</li>
  <li><strong>Model:</strong> Example Model</li>
  <li><strong>Color:</strong> Black</li>
</ul>

<h3>Features</h3>
<ul>
  <li>Feature one</li>
  <li>Feature two</li>
</ul>

<h3>Specifications</h3>
<table>
  <tbody>
    <tr><th>Storage</th><td>256GB</td></tr>
    <tr><th>Condition</th><td>New</td></tr>
  </tbody>
</table>
```

Rich text tidak didukung untuk catalog ads. Selalu isi `description` plain text sebagai fallback.

## 5. CSV formatting rules

1. Baris pertama harus berisi nama field persis seperti header schema; gunakan nama field bahasa Inggris.
2. Setiap baris berikutnya merepresentasikan satu item/varian katalog.
3. Gunakan koma sebagai delimiter kolom CSV.
4. Bungkus field dengan tanda kutip ganda jika berisi koma, line break, atau karakter kutip.
5. Escape tanda kutip di dalam quoted value dengan menggandakannya: `""`.
6. Untuk `additional_image_link`, separator daftar URL yang didokumentasikan adalah koma, titik koma, spasi, atau pipe (`|`). Bungkus seluruh daftar sebagai satu quoted CSV cell agar delimiter tidak memecah kolom.
7. Untuk `sale_price_effective_date`, pisahkan timestamp awal dan akhir dengan `/`; ini bukan separator daftar URL.
8. Format harga adalah `amount ISO_CURRENCY`, misalnya `24999000 IDR`; gunakan titik sebagai pemisah desimal.
9. ID tiap varian harus unik dan stabil. Varian satu produk berbagi `item_group_id`.
10. Jangan memasukkan HTML ke `description`; gunakan `rich_text_description` untuk markup yang didukung.
11. Jangan mengirim `inventory` dan `quantity_to_sell_on_facebook` dengan nilai stok yang bertentangan.

Contoh satu cell untuk beberapa gambar:

```csv
" https://example.com/black-front.jpg|https://example.com/black-back.jpg|https://example.com/black-side.jpg "
```

Hapus spasi awal/akhir pada nilai sebenarnya; contoh di atas hanya menonjolkan bahwa keseluruhan daftar berada dalam satu quoted cell.

## 6. CSV feed vs Product Item API

Nama field dan format pada CSV feed tidak selalu sama dengan parameter Product Item API. Tabel ini adalah peta nama/konsep, bukan instruksi untuk mengirim nama API ke CSV.

| CSV feed field | Product Item API field / concept | Important difference |
|---|---|---|
| `id` | `retailer_id` | API memakai nama parameter berbeda untuk retailer item ID. |
| `title` | `name` | Nama produk pada API. |
| `link` | `url` | URL produk pada API. |
| `image_link` | `image_url` | URL gambar utama pada API. |
| `additional_image_link` | `additional_image_urls` | API merepresentasikan gambar tambahan sebagai field berbeda; jangan salin serialisasi CSV secara otomatis. |
| `google_product_category` | `category` | API category field tidak berarti format taksonomi CSV identik untuk semua alur. |
| `item_group_id` | `retailer_product_group_id` | Konsep grouping varian; nama API berbeda. |
| `sale_price_effective_date` | `sale_price_start_date` + `sale_price_end_date` | CSV memakai satu rentang start/end; API memisahkan dua field. |
| `status` | `visibility` | Tidak setara langsung: feed `active/archived`, API visibility menggunakan konsep seperti `staging/published`. |
| `availability` | API `availability` | API memiliki enum lebih luas; jangan menganggap semua enum API diterima pada CSV. |
| `price` | API `price` | CSV memakai string `amount ISO_CURRENCY`; parameter API dapat memakai integer dalam unit minor (misalnya cents) sesuai kontrak API. |

**Aturan:** implementasi CSV harus mengikuti spesifikasi feed CSV. Implementasi API harus mengikuti versi Product Item API yang benar-benar digunakan, termasuk tipe data, enum, dan unit harga. Jangan mencampur field names atau format dari kedua interface.

## 7. Optional Meta catalog attributes not in this CSV

Meta mendokumentasikan atribut katalog tambahan yang belum termasuk dalam 33 kolom repository ini. Daftar berikut bukan rekomendasi untuk menambahkan semuanya; pilih hanya bila ada kebutuhan dan ingestion path mendukungnya.

| Attribute | Typical purpose | Notes |
|---|---|---|
| `shipping` | Informasi ongkos/layanan pengiriman | Struktur dan format bergantung pada spesifikasi feed/channel. |
| `shipping_weight` | Berat pengiriman | Isi dengan unit dan format yang diterima feed. |
| `internal_label` | Label internal untuk product set/filtering | Meta menyarankan mempertimbangkannya untuk pengelompokan produk. |
| `custom_number_0`–`custom_number_4` | Nilai numerik custom | Field tambahan; verifikasi dukungan feed. |
| `expiration_date` | Tanggal kedaluwarsa | Relevan untuk produk yang memiliki tanggal kedaluwarsa. |
| `mobile_link` | URL landing page mobile | Opsional jika URL mobile terpisah. |
| `video[0].url`–`video[19].url` | Video produk | Gunakan struktur yang diterima feed, bukan format API yang diasumsikan. |
| `additional_variant_attribute` | Atribut varian tambahan | Gunakan hanya jika struktur varian katalog membutuhkannya. |

Sebelum memperluas schema CSV, cek apakah atribut tersedia pada metode feed yang dipakai dan apakah katalog target menerima formatnya. Field yang ada pada dokumentasi API tidak otomatis dapat dipakai dengan nama/format identik pada CSV.

## 8. Validation checklist

- [ ] Semua required fields Meta Catalog Fields terisi.
- [ ] `brand` tersedia; GTIN/MPN ditambahkan bila tersedia dan valid.
- [ ] Setiap `id` unik, stabil, dan maksimum 100 karakter.
- [ ] Panjang `title`, `description`, `item_group_id`, dan atribut lain sesuai batas pada tabel.
- [ ] `availability` menggunakan nilai feed `in stock` atau `out of stock`.
- [ ] `condition` menggunakan nilai feed yang diterima: `new`, `refurbished`, atau `used`.
- [ ] `price` dan `sale_price` menggunakan format mata uang yang benar.
- [ ] `sale_price` lebih rendah dari `price`; tanggal promosi dan timezone valid.
- [ ] URL produk dan gambar dapat diakses publik serta sesuai dengan varian.
- [ ] Gambar utama JPEG/PNG, minimal 500 × 500 px, dan maksimum 8 MB.
- [ ] Daftar gambar tambahan tidak lebih dari 20 URL/2.000 karakter dan berada dalam satu quoted CSV cell.
- [ ] Kuantitas Facebook sinkron dengan stok; field baru `quantity_to_sell_on_facebook` digunakan bila workflow mendukungnya.
- [ ] Field legacy `inventory` tidak menjadi sumber stok yang bertentangan.
- [ ] Taxonomy kategori sesuai produk dan ketentuan katalog/channel.
- [ ] `size` diisi untuk kategori yang mewajibkannya.
- [ ] Custom labels masing-masing berisi satu nilai dan tidak dianggap sebagai promosi.
- [ ] CSV dapat diparse dengan jumlah kolom yang konsisten pada setiap baris.
- [ ] Feed diuji melalui Commerce Manager dan seluruh item diagnostics ditinjau.

## 9. Sample data status

File `meta-product-feed.csv` di repository adalah file demonstrasi, bukan feed produksi. Validator default memeriksa schema dan konsistensi data demo; gunakan opsi `--production` untuk menolak URL placeholder dan penanda sample sebelum rilis produksi. File berisi URL placeholder `example.com`, harga/kuantitas contoh, dan contoh varian iPhone 18 Pro Max fiktif. Jangan gunakan sebagai feed produksi sebelum spesifikasi produk, brand, GTIN/MPN, URL produk, URL gambar, harga, stok, serta tanggal promosi nyata diberikan dan divalidasi.

## 10. Official references

1. Meta Developers — [Catalog Fields](https://developers.facebook.com/documentation/ads-commerce/commerce-platform/catalog/fields) — acuan utama required/optional fields, batas field, image requirements, rich text, dan atribut katalog.
2. Meta Developers — [Inventory](https://developers.facebook.com/documentation/ads-commerce/commerce-platform/catalog/inventory) — menyatakan `inventory` digantikan oleh `quantity_to_sell_on_facebook`; halaman ini mencatat pembaruan 3 Maret 2026.
3. Meta Developers — [Product Item API reference](https://developers.facebook.com/docs/marketing-api/reference/product-item/) — acuan khusus API; field names, enum, dan tipe data API tidak boleh diasumsikan identik dengan CSV.
4. Meta Business Help Center — [Data Feed Specifications for Catalogs](https://www.facebook.com/business/help/120325381656392) — panduan feed dan checkout; beberapa instruksi lama dapat berbeda dari Catalog Fields terbaru.
5. Meta Developers — [Marketplace Partner Item API](https://developers.facebook.com/docs/marketplace/partnerships/itemAPI/) — spesifikasi khusus partner Marketplace, bukan pengganti spesifikasi umum CSV katalog.
6. Meta Developers — [Feed API Reference](https://developers.facebook.com/documentation/ads-commerce/catalog/guides/feed-api) — dokumentasi Feed API; gunakan hanya untuk interface tersebut.

**Documentation note:** Meta dapat mengubah field, batas, dan persyaratan. Sebelum rilis produksi, periksa ulang dokumentasi resmi dan instruksi/diagnostik Commerce Manager untuk katalog, negara, checkout, dan channel yang digunakan.
