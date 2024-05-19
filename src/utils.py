import operator as op
from datetime import datetime
from os import getenv

from cachetools.func import ttl_cache
from flask import request

from src import db
from src.database.models import ExportableModel, Statistic

# from sqlalchemy import and_


TTL = int(getenv("SERVER_CACHE_TTL", 60 * 60 * 24))

OPERATORS = [
    "eq",
    "ne",
    "lt",
    "le",
    "gt",
    "ge",
]


def response(success: bool = True, message: str = "", code: int = 200, **kwargs):
    data = {"success": success}
    if message:
        data["message"] = message
    data.update(kwargs)
    return data, code


@ttl_cache(maxsize=1000, ttl=TTL)
def get_object(model: ExportableModel, identifier: str):
    return model.query.filter_by(identifier=identifier).first()


def get_request_ip():
    return request.headers.get("Cf-Connecting-Ip", request.headers.get("X-Forwarded-For", request.access_route[-1]))


def save_statistic(model: ExportableModel):
    stat = Statistic(date=datetime.now(), ip=get_request_ip(), path=request.path, model=model.__name__)
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

    filtered_args = []
    for arg, value in request_args.items():
        if "__" not in arg:
            field = arg
            operator = "eq"
        else:
            field, operator = arg.split("__")

        if operator not in OPERATORS:
            return response(success=False, message=f"Invalid operator filter '{operator}'", code=400)
        operator = getattr(op, operator)
        if field not in model.__table__.columns.keys():
            return response(success=False, message=f"Invalid search parameter '{field}'", code=400)
        field = getattr(model, field)
        filtered_args.append(operator(field, value))

    print(*filtered_args)

    objs = model.query.filter(*filtered_args).all()
    data = {obj.identifier: obj.as_dict() for obj in objs}
    return response(data=data)
