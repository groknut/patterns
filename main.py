import uvicorn
from fastapi import FastAPI, status

from Src.Logics.report_factory import report_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Logics.text_report import text_report

app = FastAPI()


setting_manager = settings_manager()
setting_manager.load()
storage = storage_manager()
storage.convert(setting_manager.settings.is_first)


@app.post("/")
async def main():
    return "Hello, world"


@app.get(
    "/api/get_report",
    summary="Получить отчет",
    description="Эндпоинт возвращает статус формирования отчета",
    status_code=status.HTTP_200_OK,
)
def get_report():
    recipe = next(iter(storage.recipes.values()))
    report = text_report()
    rep = report.build(recipe)

    assert rep.binary == []
    assert rep.text != ""
    return rep.text


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
