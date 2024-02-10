from bs4 import BeautifulSoup, ResultSet, Tag

from .constants import EXCEPTIONS, REMOVE_PARENTHESES_RE


def get_identifier(soup: BeautifulSoup, name: str) -> str:
    identifier = EXCEPTIONS.get(name)
    if identifier:
        return identifier

    if name.startswith("Music Disc"):
        cd_name = REMOVE_PARENTHESES_RE.findall(name)[0]
        return "music_disc_" + cd_name.lower().replace(" ", "_")
    if name.startswith("Banner Pattern"):
        name = REMOVE_PARENTHESES_RE.findall(name)[0]

    table = soup.select("h2:has(> span[id^=Data_values i])")[0].find_next("table")
    for row in table.find_all("tr"):
        cells = row.find_all(["td", "th"])
        if cells[0].text.strip() == name:
            identifier = cells[1].text.strip().lower()
            break
    if identifier and identifier.lower() == "identifier":
        return table.find_all("tr")[1].find_all(["td", "th"])[1].text.strip().lower()
    return identifier


def get_info_table(soup: BeautifulSoup) -> tuple[dict, Tag]:
    raw_info_table: Tag = soup.find("table", {"class": "infobox-rows"})
    tool_list: Tag = None
    info_table = {}
    for row in raw_info_table.find_all("tr"):
        key: str = row.find("th").text.strip().lower()
        value: Tag = row.find("td")
        if key.startswith("tool"):
            tool_list = value.find("p")
            continue
        for br in value.find_all("br"):
            br.replace_with("\n")
        info_table[key] = value.text.strip().lower()

    return info_table, tool_list


def get_inventory_image(soup: BeautifulSoup, name: str) -> str:
    search_name = name.replace("(", "").replace(")", "")

    if "Banner Pattern" in search_name:
        search_name = "Banner Pattern"

    if search_name.endswith("Spawn Egg"):
        table: Tag = soup.select("h2:has(> #List_of_spawn_eggs)")[0].find_next("table")
        invslots: ResultSet[Tag] = table.select(".sprite-file:has(> img.pixel-image)")
    else:
        invslots: ResultSet[Tag] = soup.select(".infobox-invimages .invslot-item")

    if len(invslots) == 1:
        return invslots[0].find("img")["src"].split("?")[0].lstrip("/")

    for invslot in invslots:
        img: Tag = invslot.find("img")
        if "Invicon " + search_name in img["alt"]:
            return img["src"].split("?")[0].lstrip("/")

    raise ValueError(f"Inventory image not found for {name}")
