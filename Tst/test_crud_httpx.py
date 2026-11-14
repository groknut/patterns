import httpx
import pytest

from main import app

BASE_URL = "http://localhost:8000"

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as c:
        yield c


async def test_formats_returns_all(client):
    """GET /api/report/formats → 5 форматов"""
    r = await client.get("/api/report/formats")
    assert r.status_code == 200
    assert r.json() == ["TXT", "CSV", "Markdown", "XML", "HTML"]


async def test_crud_create_read_delete(client):
    """POST → GET → DELETE для range"""
    payload = {"__class__": "range_model", "name": "тест_httpx", "coef": 1.0}

    created = await client.post("/api/entities/range", json=payload)
    assert created.status_code == 201
    code = created.json()["id"]

    read = await client.get(f"/api/entities/range/{code}")
    assert read.status_code == 200
    assert read.json()["name"] == "тест_httpx"

    deleted = await client.delete(f"/api/entities/range/{code}")
    assert deleted.status_code == 204


async def test_delete_linked_returns_409(client):
    """DELETE связанной range → 409 с references"""
    from Src.Logics.storage_manager import storage_manager

    kg = next(r for r in storage_manager().ranges.values() if r.name == "килограмм")
    r = await client.delete(f"/api/entities/range/{kg.id}")

    assert r.status_code == 409
    assert "references" in r.json()["detail"]
    assert len(r.json()["detail"]["references"]) > 0
