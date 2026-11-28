from fastapi.testclient import TestClient

from main import app
from Src.Services.logger_service import logger_service
from Src.Logics.observer import observer


def test_crud_operation_logged_to_file(tmp_path):
    """POST /api/entities/range → observer → logger_service пишет в файл"""
    # Подготовка: чистый observer, лог во временном файле
    observer.clear()
    log_file = tmp_path / "test.log"
    logger_service(log_file=str(log_file))

    # Действие: создаём range через API
    client = TestClient(app)
    payload = {"__class__": "range_model", "name": "лог_тест", "coef": 1.0}
    response = client.post("/api/entities/range", json=payload)

    # Проверки
    assert response.status_code == 201
    assert log_file.exists(), "Лог-файл не создан"

    content = log_file.read_text(encoding="utf-8")
    assert "web_call" in content, "web_call не залогирован"
    assert "crud_operation" in content, "crud_operation не залогирован"
    assert "create" in content, "действие create не залогировано"
    assert "лог_тест" in content, "имя объекта не попало в лог"

    # cleanup
    client.delete(f"/api/entities/range/{response.json()['id']}")
    observer.clear()
