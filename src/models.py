from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSON

from . import db


class Block(db.Model):
    __tablename__ = "block"


class Item(db.Model):
    __tablename__ = "item"


class Mob(db.Model):
    __tablename__ = "mob"
