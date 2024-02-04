from flask_sqlalchemy import SQLAlchemy

from .models import Behavior, Classification, Rarity, Transparency


def create_database(db: SQLAlchemy):
    db.drop_all()
    db.create_all()

    db.session.add_all(
        [
            Transparency(name="Yes"),
            Transparency(name="No"),
            Transparency(name="Partial"),
        ]
    )

    db.session.add_all(
        [
            Rarity(name="Common"),
            Rarity(name="Uncommon"),
            Rarity(name="Rare"),
            Rarity(name="Epic"),
        ]
    )

    db.session.add_all(
        [
            Behavior(name="Passive"),
            Behavior(name="Hostile"),
            Behavior(name="Neutral"),
        ]
    )

    db.session.add_all(
        [
            Classification(name="Ambient"),
            Classification(name="Animal"),
            Classification(name="Aquatic"),
            Classification(name="Arthropod"),
            Classification(name="Golem"),
            Classification(name="Illager"),
            Classification(name="Monster"),
            Classification(name="Undead"),
        ]
    )

    db.session.commit()
