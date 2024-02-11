import requests as rq
from bs4 import BeautifulSoup, ResultSet, Tag
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from src.database.models import Item, Rarity

from .constants import EXTRACT_NUMBER_RE, IGNORES, REMOVE_PARENTHESES_RE
from .utils import get_identifier, get_info_table, get_inventory_image


def parse_item(BASE_URI: str, url: str, name: str) -> Item:
    response = rq.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    identifier = get_identifier(soup, name)
    # version = get_version(soup, name) # TODO: get version from history
    inventory_image = BASE_URI % get_inventory_image(soup, name)

    info_table, _ = get_info_table(soup)

    rarity_name = info_table.get("rarity color", "common")
    rarity = Rarity.query.filter(func.lower(Rarity.name) == rarity_name).first()
    renewable = info_table.get("renewable", "no") == "yes"
    stackable = info_table.get("stackable", "1").replace("no", "1")
    stack_size = int(EXTRACT_NUMBER_RE.findall(stackable)[0])

    item = Item(
        identifier=identifier,
        name=name,
        inventory_image=inventory_image,
        # version=version,
        rarity=rarity,
        renewable=renewable,
        stack_size=stack_size,
    )

    return item


def fetch_items(BASE_URI: str, db: SQLAlchemy):
    URL = BASE_URI % "w/Item"
    response = rq.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    item_tags: ResultSet[Tag] = soup.find("span", {"id": "List_of_items"}).parent.find_all_next("li")
    last_item = soup.find("span", {"id": "Education_Edition_exlusives"}).parent.find_previous("li")
    item_tags = item_tags[: item_tags.index(last_item) + 1]

    dones = set()

    for item_tag in item_tags:
        name_tag = item_tag.find("a")
        name = REMOVE_PARENTHESES_RE.sub("", name_tag["title"].strip())
        if name in IGNORES:
            continue
        if name in ("Music Disc", "Banner Pattern"):
            name = item_tag.text.strip()
        url = BASE_URI % name_tag["href"].lstrip("/")
        if name == "Tropical Fish":
            url = BASE_URI % "w/Tropical_Fish_(item)"
        item = parse_item(BASE_URI, url, name)
        if item.identifier in dones:
            continue
        dones.add(item.identifier)
        print(f"{item.name} / {item.identifier}")

        db.session.add(item)
    db.session.commit()
