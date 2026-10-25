# API Pendataan Masa Pakai Produk Perawatan Pribadi

REST API latihan menggunakan FastAPI, Pydantic v2, autentikasi header, role-based access control, dan pytest TestClient.

## Menjalankan di Google Colab
1. Pasang dependensi: `pip install -r requirements.txt`
2. Jalankan tes dari folder proyek: `pytest -v`
3. Jalankan server: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Buka `/docs` pada alamat server yang tersedia.

## Endpoint
- GET `/api/v1/produk`
- POST `/api/v1/produk`
- GET `/api/v1/produk/{produk_id}`
- PATCH `/api/v1/produk/{produk_id}`
- DELETE `/api/v1/produk/{produk_id}`

Semua endpoint memerlukan header `X-API-Key`.
Kunci demo: `admin-demo-123` (Admin) dan `student-demo-123` (Student).
Kunci ini hanya untuk demonstrasi praktikum.

## Catatan
Data disimpan di memori dan hilang ketika aplikasi dimulai ulang. Informasi masa pakai harus mengikuti label produk; API ini hanya mencatat data dan tidak menentukan keamanan produk.
