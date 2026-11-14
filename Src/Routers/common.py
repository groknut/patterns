from Src.Dtos.report_type_dto import entity_type_enum
from Src.Logics.convert_factory import convert_factory
from Src.Logics.report_sources import report_source_factory
from Src.Logics.settings_manager import settings_manager
from Src.Logics.storage_manager import storage_manager
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.recipe_model import recipe_model


def get_storage() -> storage_manager:
    sm = settings_manager()
    if sm.settings is None:
        sm.load()
    st = storage_manager()
    if not st.is_initialized:
        st.convert(sm.settings.is_first)
    return st


def get_convert_factory() -> convert_factory:
    return convert_factory()


def get_source_factory() -> report_source_factory:
    return report_source_factory()


def get_collection_and_model(etype: entity_type_enum):
    """Возвращает (коллекция из storage, класс модели)."""
    st = get_storage()
    mapping = {
        entity_type_enum.NOMENCLATURE: (st.nomenclatures, nomenclature_model),
        entity_type_enum.RANGE: (st.ranges, range_model),
        entity_type_enum.RECIPE: (st.recipes, recipe_model),
    }
    return mapping[etype]
