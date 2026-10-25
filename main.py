from fastapi import FastAPI
from routers.produk import router as produk_router

app = FastAPI(
    title="API Pendataan Masa Pakai Produk Perawatan Pribadi",
    description="REST API untuk mencatat masa pakai produk setelah kemasan dibuka.",
    version="1.0.0",
)

app.include_router(produk_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"pesan": "API Masa Pakai Produk berjalan"}
