import requests as rq
from bs4 import BeautifulSoup, ResultSet, Tag
from flask_sqlalchemy import SQLAlchemy

from src.database.models import Block, Tool

from .constants import ADDED_RE, EXTRACT_NUMBER_RE, IGNORES, IMAGE_BLOCK_LINK_RE, REMOVE_PARENTHESES_RE, TOOL_LINK_RE
from .utils import get_identifier, get_info_table, get_inventory_image


def get_version(soup: BeautifulSoup, name: str) -> str:
    # TODO: get version from history
    table: Tag = soup.find("span", {"id": "History"}).parent.find_next("table")
    version = table.find(text=ADDED_RE).parent.parent.find(["th", "td"]).text.strip()
    return version


def parse_block(BASE_URI: str, db: SQLAlchemy, url: str, name: str, render_image: str) -> Block:
    response = rq.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # head = soup.find("span", {"class": "mw-page-title-main"}).text.strip()
    # if head != name:
    #     pass  # sub categories (e.g. "Acacia Button" in "Wooden Button" page)
    identifier = get_identifier(soup, name)
    # version = get_version(soup, name)
    if name == "Light Block":
        inventory_image = render_image
    else:
        inventory_image = BASE_URI % get_inventory_image(soup, name)

    info_table, tool_list = get_info_table(soup)

    stackable = info_table.get("stackable", "1").replace("no", "1")
    stack_size = int(EXTRACT_NUMBER_RE.findall(stackable)[0])
    blast_resistance = float(EXTRACT_NUMBER_RE.findall(info_table.get("blast resistance", "0"))[0])
    hardness = float(EXTRACT_NUMBER_RE.findall(info_table.get("hardness", "0"))[0])
    # TODO: Handle more case (e.g : Berries)
    luminous = int((EXTRACT_NUMBER_RE.findall(info_table.get("luminous", "0").replace("no", "0")) or [0])[0])
    flammable: bool = info_table.get("flammable", "no") == "yes"
    waterloggable: bool = w == "yes" if (w := info_table.get("waterloggable")) else None

    if tool_list:
        if len(tools := tool_list.find_all("a")) > 0:
            tools = [TOOL_LINK_RE.findall(tool["href"])[0] for tool in tools]
        else:
            tools = [tool_list.text.strip().replace("Any tool", "Any")]
            if tools[0] == "None":
                tools = []
    else:
        tools = []

    block = Block(
        identifier=identifier,
        name=name,
        render_image=render_image,
        inventory_image=inventory_image,
        # version_id=version_id,
        stack_size=stack_size,
        blast_resistance=blast_resistance,
        hardness=hardness,
        luminous=luminous,
        # transparency_id=transparency_id,
        flammable=flammable,
        waterloggable=waterloggable,
    )

    for tool_name in tools:
        tool = Tool.query.get(tool_name)
        if tool is None:
            tool = Tool(name=tool_name)
            db.session.add(tool)
        tool.blocks.append(block)

    return block


def fetch_blocks(BASE_URI: str, db: SQLAlchemy):
    URL = BASE_URI % "w/Block"
    response = rq.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    block_tags: ResultSet[Tag] = (
        soup.find("span", {"id": "List_of_blocks"}).parent.find_next("div").find("ul").find_all("li")
    )

    for block_tag in block_tags:
        image_tag, name_tag = block_tag.find_all("a", limit=2)
        name = REMOVE_PARENTHESES_RE.sub("", name_tag.text.strip())
        if name in IGNORES:
            continue
        url = BASE_URI % name_tag["href"].lstrip("/")
        render_image = BASE_URI % ("images/" + IMAGE_BLOCK_LINK_RE.sub(r"\1", image_tag["href"]))
        block = parse_block(BASE_URI, db, url, name, render_image)
        print(f"{block.name} / {block.identifier}")

        db.session.add(block)
    db.session.commit()
