from os import getenv

from cachetools.func import ttl_cache
from flask import Blueprint, request

from src.database.models import Block, ExportableModel, Item, Mob
from src.utils import response

TTL = int(getenv("CACHE_TTL", 60 * 60 * 24))

block_view = Blueprint("block", __name__, url_prefix="/block")
item_view = Blueprint("item", __name__, url_prefix="/item")
mob_view = Blueprint("mob", __name__, url_prefix="/mob")


@ttl_cache(maxsize=1000, ttl=TTL)
def get_object(model: ExportableModel, identifier: str):
    return model.query.filter_by(identifier=identifier).first()


# -------------------------------------------------------------------


def get_all(model: ExportableModel):
    data = [obj.identifier for obj in model.query.all()]
    return response(data=data)


@block_view.route("/")
def all_blocks():
    return get_all(Block)


@item_view.route("/")
def all_items():
    return get_all(Item)


@mob_view.route("/")
def all_mobs():
    return get_all(Mob)


# -------------------------------------------------------------------


def get_by_identifier(model: ExportableModel, identifier: str):
    obj = get_object(model, identifier)
    if obj:
        return response(data=obj.as_dict())
    return response(success=False, message=f"{model.__name__} not found", code=404)


@block_view.route("/<block_identifier>")
def get_block_by_identifier(block_identifier):
    return get_by_identifier(Block, block_identifier)


@item_view.route("/<item_identifier>")
def get_item_by_identifier(item_identifier):
    return get_by_identifier(Item, item_identifier)


@mob_view.route("/<mob_identifier>")
def get_mob_by_identifier(mob_identifier):
    return get_by_identifier(Mob, mob_identifier)


# -------------------------------------------------------------------


def search(model: ExportableModel):
    request_args = request.args
    if any(arg not in model.__table__.columns for arg in request_args):
        return response(success=False, message="Invalid search parameters", code=400)
    objs = model.query.filter_by(**request_args).all()
    data = {obj.identifier: obj.as_dict() for obj in objs}
    return response(data=data)


@block_view.route("/search")
def search_blocks():
    return search(Block)


@item_view.route("/search")
def search_items():
    return search(Item)


@mob_view.route("/search")
def search_mobs():
    return search(Mob)
