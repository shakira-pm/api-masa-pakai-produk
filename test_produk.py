import pytest
from fastapi.testclient import TestClient
from main import app
from routers import produk as produk_module

client = TestClient(app)
ADMIN = {"X-API-Key": "admin-demo-123"}
STUDENT = {"X-API-Key": "student-demo-123"}
BAD_KEY = {"X-API-Key": "salah"}
VALID = {
    "nama_produk": "Moisturizer",
    "kategori": "skincare",
    "tanggal_dibuka": "2026-10-01",
    "masa_pakai_bulan": 6,
    "catatan": "Contoh catatan",
}

@pytest.fixture(autouse=True)
def reset_data():
    produk_module.db.clear()
    produk_module.next_id = 1

def create_product(headers=ADMIN, payload=None):
    return client.post("/api/v1/produk", headers=headers, json=payload or VALID)

def test_01_daftar_produk_kosong():
    assert client.get("/api/v1/produk", headers=ADMIN).status_code == 200

def test_02_tambah_produk_valid():
    assert create_product().status_code == 201

def test_03_detail_produk_ada():
    create_product()
    assert client.get("/api/v1/produk/1", headers=ADMIN).status_code == 200

def test_04_ubah_produk_valid():
    create_product()
    r = client.patch("/api/v1/produk/1", headers=ADMIN, json={"nama_produk": "Serum"})
    assert r.status_code == 200
    assert r.json()["nama_produk"] == "Serum"

def test_05_hapus_produk_admin():
    create_product()
    assert client.delete("/api/v1/produk/1", headers=ADMIN).status_code == 204

def test_06_detail_produk_tidak_ada():
    assert client.get("/api/v1/produk/99", headers=ADMIN).status_code == 404

def test_07_ubah_produk_tidak_ada():
    assert client.patch("/api/v1/produk/99", headers=ADMIN, json={"nama_produk": "Serum"}).status_code == 404

def test_08_hapus_produk_tidak_ada():
    assert client.delete("/api/v1/produk/99", headers=ADMIN).status_code == 404

def test_09_nama_produk_kosong():
    payload = {**VALID, "nama_produk": "   "}
    assert create_product(payload=payload).status_code == 422

def test_10_kategori_tidak_valid():
    payload = {**VALID, "kategori": "makanan"}
    assert create_product(payload=payload).status_code == 422

def test_11_masa_pakai_nol():
    payload = {**VALID, "masa_pakai_bulan": 0}
    assert create_product(payload=payload).status_code == 422

def test_12_format_tanggal_salah():
    payload = {**VALID, "tanggal_dibuka": "tanggal-salah"}
    assert create_product(payload=payload).status_code == 422

def test_13_tanpa_api_key():
    assert client.get("/api/v1/produk").status_code == 401

def test_14_api_key_salah():
    assert client.get("/api/v1/produk", headers=BAD_KEY).status_code == 401

def test_15_student_tidak_boleh_menghapus():
    create_product()
    assert client.delete("/api/v1/produk/1", headers=STUDENT).status_code == 403

def test_16_student_boleh_melihat_daftar():
    assert client.get("/api/v1/produk", headers=STUDENT).status_code == 200

def test_17_student_boleh_menambah():
    assert create_product(headers=STUDENT).status_code == 201

def test_18_student_tidak_boleh_mengubah():
    create_product()
    assert client.patch("/api/v1/produk/1", headers=STUDENT, json={"nama_produk": "Serum"}).status_code == 403

def test_19_update_kosong_ditolak():
    create_product()
    assert client.patch("/api/v1/produk/1", headers=ADMIN, json={}).status_code == 422


def test_20_swagger_docs_tersedia():
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
