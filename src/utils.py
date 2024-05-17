from datetime import datetime
from os import getenv

from cachetools.func import ttl_cache
from flask import request

from src import db
from src.database.models import ExportableModel, Statistic

TTL = int(getenv("SERVER_CACHE_TTL", 60 * 60 * 24))


def response(success: bool = True, message: str = "", code: int = 200, **kwargs):
    data = {"success": success}
    if message:
        data["message"] = message
    data.update(kwargs)
    return data, code


@ttl_cache(maxsize=1000, ttl=TTL)
def get_object(model: ExportableModel, identifier: str):
    return model.query.filter_by(identifier=identifier).first()


def save_statistic(model: ExportableModel):
    stat = Statistic(date=datetime.now(), ip=request.access_route[-1], path=request.path, model=model.__name__)
    db.session.add(stat)
    db.session.commit()


def get_all_from(model: ExportableModel):
    save_statistic(model)
    data = [obj.identifier for obj in model.query.all()]
    return response(data=data)


def get_by_identifier_from(model: ExportableModel, identifier: str):
    save_statistic(model)
    obj = get_object(model, identifier)
    if obj:
        return response(data=obj.as_dict())
    return response(success=False, message=f"{model.__name__} not found", code=404)


def search_from(model: ExportableModel):
    save_statistic(model)
    request_args = request.args
    if any(arg not in model.__table__.columns for arg in request_args):
        return response(success=False, message="Invalid search parameters", code=400)
    objs = model.query.filter_by(**request_args).all()
    data = {obj.identifier: obj.as_dict() for obj in objs}
    return response(data=data)
