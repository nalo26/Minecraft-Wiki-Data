from sqlalchemy import Boolean, Date, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from .. import db


class Block(db.Model):
    __tablename__ = "block"

    identifier = db.Column(String(100), primary_key=True)
    name = db.Column(String(100), nullable=False, unique=True)
    render_image = db.Column(String(200))
    inventory_image = db.Column(String(200))
    version_id = db.Column(String(100), db.ForeignKey("version.version"))
    version = db.relationship("Version", back_populates="blocks")
    stack_size = db.Column(Integer, nullable=False)
    tools = db.relationship("Tool", secondary="block_tool", back_populates="blocks")
    blast_resistance = db.Column(Float, nullable=False)
    hardness = db.Column(Float, nullable=False)
    luminous = db.Column(Integer, nullable=False)
    transparency_id = db.Column(String(100), db.ForeignKey("transparency.name"))
    transparency = db.relationship("Transparency", back_populates="blocks")
    flammable = db.Column(Boolean, nullable=False)
    waterloggable = db.Column(Boolean, nullable=True)  # None for full block


class Item(db.Model):
    __tablename__ = "item"

    identifier = db.Column(String(100), primary_key=True)
    name = db.Column(String(100), nullable=False, unique=True)
    inventory_image = db.Column(String(200))
    version_id = db.Column(String(100), db.ForeignKey("version.version"))
    version = db.relationship("Version", back_populates="items")
    rarity_id = db.Column(String(100), db.ForeignKey("rarity.name"))
    rarity = db.relationship("Rarity", back_populates="items")
    renewable = db.Column(Boolean, nullable=False)
    stack_size = db.Column(Integer, nullable=False)
    dropped_by = db.relationship("Mob", secondary="drop", back_populates="drops")


class Mob(db.Model):
    __tablename__ = "mob"

    identifier = db.Column(String(100), primary_key=True)
    name = db.Column(String(100), nullable=False, unique=True)
    head_image = db.Column(String(200))
    render_image = db.Column(String(200))
    version_id = db.Column(String(100), db.ForeignKey("version.version"))
    version = db.relationship("Version", back_populates="mobs")
    behaviors = db.relationship("Behavior", secondary="mob_behavior", back_populates="mobs")
    classifications = db.relationship("Classification", secondary="mob_classification", back_populates="mobs")
    width = db.Column(Float, nullable=False)
    height = db.Column(Float, nullable=False)
    health = db.Column(Float, nullable=False)
    attacks = db.relationship("Attack", back_populates="mob")
    drops = db.relationship("Item", secondary="drop", back_populates="dropped_by")


class Version(db.Model):
    __tablename__ = "version"

    update = db.Column(String(100))
    version = db.Column(String(50), primary_key=True)
    release_date = db.Column(Date)
    blocks = db.relationship("Block", back_populates="version")
    items = db.relationship("Item", back_populates="version")
    mobs = db.relationship("Mob", back_populates="version")


class Tool(db.Model):
    __tablename__ = "tool"
    name = db.Column(String(30), primary_key=True)
    blocks = db.relationship("Block", secondary="block_tool", back_populates="tools")


class Transparency(db.Model):
    __tablename__ = "transparency"
    name = db.Column(String(20), primary_key=True)
    blocks = relationship("Block", back_populates="transparency")


class Rarity(db.Model):
    __tablename__ = "rarity"
    name = db.Column(String(20), primary_key=True)
    items = db.relationship("Item", back_populates="rarity")


class Behavior(db.Model):
    __tablename__ = "behavior"
    name = db.Column(String(20), primary_key=True)
    mobs = db.relationship("Mob", secondary="mob_behavior", back_populates="behaviors")


class Classification(db.Model):
    __tablename__ = "classification"
    name = db.Column(String(20), primary_key=True)
    mobs = db.relationship("Mob", secondary="mob_classification", back_populates="classifications")


class Difficulty(db.Model):
    __tablename__ = "difficulty"
    name = db.Column(String(20), primary_key=True)


class Attack(db.Model):
    __tablename__ = "attack"
    mob_id = db.Column(String(100), db.ForeignKey("mob.identifier"), primary_key=True)
    mob = db.relationship("Mob", back_populates="attacks")
    difficulty_name = db.Column(String(20), db.ForeignKey("difficulty.name"), primary_key=True)
    difficulty = db.relationship("Difficulty")
    damage = db.Column(Float, nullable=False)


block_tool = db.Table(
    "block_tool",
    db.Column("block_id", String(100), db.ForeignKey("block.identifier"), primary_key=True),
    db.Column("tool_id", String(100), db.ForeignKey("tool.name"), primary_key=True),
)

mob_behavior = db.Table(
    "mob_behavior",
    db.Column("mob_id", String(100), db.ForeignKey("mob.identifier"), primary_key=True),
    db.Column("behavior_name", String(20), db.ForeignKey("behavior.name"), primary_key=True),
)

mob_classification = db.Table(
    "mob_classification",
    db.Column("mob_id", String(100), db.ForeignKey("mob.identifier"), primary_key=True),
    db.Column("classification_name", String(20), db.ForeignKey("classification.name"), primary_key=True),
)

drop = db.Table(
    "drop",
    db.Column("mob_id", String(100), db.ForeignKey("mob.identifier"), primary_key=True),
    db.Column("item_id", String(100), db.ForeignKey("item.identifier"), primary_key=True),
    db.Column("chance", Float, nullable=False),
    db.Column("Quantity", Integer, nullable=False),
)


class Statistic(db.Model):
    __tablename__ = "statistic"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    date = db.Column(DateTime, nullable=False)
    ip = db.Column(String(100), nullable=False)
    path = db.Column(String(100), nullable=False)
    model = db.Column(String(100), nullable=False)
