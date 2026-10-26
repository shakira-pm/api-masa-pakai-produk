from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

Kategori = Literal["skincare", "parfum", "kosmetik", "perawatan_tubuh"]

class ProdukCreate(BaseModel):
    nama_produk: str = Field(min_length=1, max_length=100)
    kategori: Kategori
    tanggal_dibuka: date
    masa_pakai_bulan: int = Field(gt=0, le=120)
    catatan: Optional[str] = Field(default=None, max_length=300)

    @field_validator("nama_produk")
    @classmethod
    def nama_tidak_boleh_kosong(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Nama produk tidak boleh kosong.")
        return value

class ProdukUpdate(BaseModel):
    nama_produk: Optional[str] = Field(default=None, min_length=1, max_length=100)
    kategori: Optional[Kategori] = None
    tanggal_dibuka: Optional[date] = None
    masa_pakai_bulan: Optional[int] = Field(default=None, gt=0, le=120)
    catatan: Optional[str] = Field(default=None, max_length=300)

    @field_validator("nama_produk")
    @classmethod
    def nama_tidak_boleh_kosong(cls, value):
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Nama produk tidak boleh kosong.")
        return value

    @model_validator(mode="after")
    def minimal_satu_field(self):
        if not self.model_fields_set:
            raise ValueError("Minimal satu field harus diisi untuk pembaruan.")
        return self

class ProdukResponse(BaseModel):
    id: int
    nama_produk: str
    kategori: Kategori
    tanggal_dibuka: date
    masa_pakai_bulan: int
    catatan: Optional[str] = None
