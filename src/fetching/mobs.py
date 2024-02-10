import requests as rq
from bs4 import BeautifulSoup, ResultSet, Tag
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from src.database.models import Behavior, Classification, Mob

from .constants import (
    EXTRACT_NUMBER_RE,
    FILE_LINK_RE,
    HEIGHT_RE,
    REMOVE_NOTE_RE,
    REMOVE_PARENTHESES_RE,
    SPACE_SEPARATOR,
    WIDTH_RE,
)
from .utils import get_identifier, get_info_table


def parse_mob(BASE_URI: str, url: str, name: str, head_image: str) -> Mob:
    response = rq.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    identifier = get_identifier(soup, name)
    # version = get_version(soup, name) # TODO: get version from history
    image_tag = soup.find("div", {"class": "infobox-imagearea"}).find("a")
    render_image = BASE_URI % ("images/" + FILE_LINK_RE.sub(r"\1", image_tag["href"]))

    info_table, _ = get_info_table(soup)

    raw_behaviors = info_table.get("behavior", "")
    raw_classifications = info_table.get("classification", "")
    hitbox_info = info_table.get("hitbox size")
    if hitbox_info is not None:
        height = float((HEIGHT_RE.findall(hitbox_info) or [-1])[0])
        width = float((WIDTH_RE.findall(hitbox_info) or [-1])[0])
    else:
        height, width = -1, -1
    health = float(EXTRACT_NUMBER_RE.findall(info_table.get("health points", "0"))[0])

    if identifier == "rabbit":
        raw_behaviors = "passive"

    behaviors = []
    raw_behaviors = raw_behaviors.split("\n") if "\n" in raw_behaviors else raw_behaviors.replace("\n", ",").split(",")
    for behavior in raw_behaviors:
        behavior = REMOVE_PARENTHESES_RE.sub("", behavior.strip())
        if behavior == "":
            break
        if "be" in behavior and "only" in behavior:
            continue
        behavior = REMOVE_NOTE_RE.sub("", behavior)
        if SPACE_SEPARATOR in behavior:
            behavior = behavior.split(SPACE_SEPARATOR)[0]
        behaviors.append(Behavior.query.filter(func.lower(Behavior.name) == behavior).first())

    classifications = []
    raw_classifications = (
        raw_classifications.split("\n")
        if "\n" in raw_classifications
        else raw_classifications.replace("\n", ",").split(",")
    )
    for classification in raw_classifications:
        classification = REMOVE_PARENTHESES_RE.sub("", classification.strip())
        if classification == "":
            break
        if "be" in classification and "only" in classification:
            continue
        classification = REMOVE_NOTE_RE.sub("", classification)
        if SPACE_SEPARATOR in classification:
            classification = classification.split(SPACE_SEPARATOR)[0]
        classifications.append(Classification.query.filter(func.lower(Classification.name) == classification).first())

    # TODO: attacks & drops

    mob = Mob(
        identifier=identifier,
        name=name,
        head_image=head_image,
        render_image=render_image,
        # version_id=version_id,
        behaviors=behaviors,
        classifications=classifications,
        width=width,
        height=height,
        health=health,
    )
    return mob


def fetch_mobs(BASE_URI: str, db: SQLAlchemy):
    URL = BASE_URI % "w/Mob"
    response = rq.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    mob_tables: ResultSet[Tag] = soup.find("span", {"id": "List_of_mobs"}).parent.find_all_next("table")
    last_mob = soup.find("span", {"id": "Removed_mobs"}).parent.find_previous("td")
    image_cells: list[Tag] = []
    name_cells: list[Tag] = []

    for table in mob_tables:
        rows = table.find_all("tr")
        image_row, name_row = rows[0], rows[1]
        if last_mob in name_row:
            break
        image_cells.extend(image_row.find_all("td"))
        name_cells.extend(name_row.find_all("td"))

    for mob_image, mob_name in zip(image_cells, name_cells):
        name_tag = mob_name.find("a")
        name = name_tag.text.strip()
        url = BASE_URI % name_tag["href"].lstrip("/")
        head_image = BASE_URI % mob_image.find("img")["src"].split("?")[0].lstrip("/")
        mob = parse_mob(BASE_URI, url, name, head_image)
        print(f"{mob.name} / {mob.identifier}")

        db.session.add(mob)
    db.session.commit()
