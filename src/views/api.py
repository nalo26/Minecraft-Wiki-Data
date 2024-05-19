from hashlib import md5

from flask import Blueprint

from src import cache
from src.database.models import Block, ExportableModel, Item, Mob
from src.utils import get_all_from, get_by_identifier_from, get_request_ip, response, search_from

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


def user_cache_key(*args, **kwargs):
    hashed_ip = md5(get_request_ip().encode()).hexdigest()
    return f"user_{hashed_ip}"


@view.route("/<string:model_name>")
@cache.cached(make_cache_key=user_cache_key, query_string=True)
@get_model
def get_all(model: ExportableModel):
    return get_all_from(model)


@view.route("/<string:model_name>/<string:identifier>")
@cache.cached(make_cache_key=user_cache_key, query_string=True)
@get_model
def get_identifier(model: ExportableModel, identifier: str):
    return get_by_identifier_from(model, identifier)


@view.route("/<string:model_name>/search")
@cache.cached(make_cache_key=user_cache_key, query_string=True)
@get_model
def search_blocks(model: ExportableModel):
    return search_from(model)
