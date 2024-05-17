from flask import Blueprint

from src.database.models import Block, ExportableModel, Item, Mob
from src.utils import get_all_from, get_by_identifier_from, response, search_from

ROUTES_DICT = {"block": Block, "item": Item, "mob": Mob}

view = Blueprint("api", __name__)


def get_model(func):
    def wrapper(model_name, *args, **kwargs):
        model = ROUTES_DICT.get(model_name)
        if not model:
            return response(success=False, message="Invalid model", code=400)
        return func(model, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


@view.route("/<string:model_name>")
@get_model
def get_all(model: ExportableModel):
    return get_all_from(model)


@view.route("/<string:model_name>/<string:identifier>")
@get_model
def get_identifier(model: ExportableModel, identifier: str):
    return get_by_identifier_from(model, identifier)


@view.route("/<string:model_name>/search")
@get_model
def search_blocks(model: ExportableModel):
    return search_from(model)
