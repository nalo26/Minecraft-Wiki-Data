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
    raw_info_table = soup.find("table", {"class": "infobox-rows"})
    tool_list: Tag = None
    info_table = {}
    for row in raw_info_table.find_all("tr"):
        key = row.find("th").text.strip().lower()
        value = row.find("td")
        if key.startswith("tool"):
            tool_list = value.find("p")
            continue
        info_table[key] = value.text.strip().lower()

    return info_table, tool_list


