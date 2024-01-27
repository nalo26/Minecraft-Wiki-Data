from datetime import date, datetime

import requests as rq
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from flask_sqlalchemy import SQLAlchemy

from src.database.models import Version

from .regex import CLEAN_UPDATE_RE, CLEAN_VERSION_RE, DOUBLE_DATE_RE, DOUBLE_DAY_RE, INDEV_RE, INFDEV_RE


def flatten_table(soup: BeautifulSoup, table: Tag) -> list[list[str]]:
    trs: ResultSet[Tag] = table.find_all("tr")
    line_length = len(trs[0].find_all(["td", "th"]))
    formated_table = [[""] * line_length for _ in range(len(trs))]
    for row_num, row in enumerate(trs):
        cols = row.find_all(["td", "th"])
        for td_num, col in enumerate(cols):
            colspan = int(col.get("colspan", 1))
            rowspan = int(col.get("rowspan", 1))
            for _ in range(colspan):
                line = formated_table[row_num]
                line[line.index("")] = col.text.strip()
            if rowspan > 1:  # extend rowspan to next lines
                for i in range(1, rowspan):
                    try:
                        line = trs[row_num + i]
                    except IndexError:
                        continue
                    td = soup.new_tag("td")
                    td.string = col.text.strip()
                    td_childs = line.find_all(["td", "th"])
                    if td_num < len(td_childs):
                        line.insert(list(line.children).index(td_childs[td_num]), td)
                    else:
                        line.append(td)
    return formated_table


def parse_version_table(soup: BeautifulSoup, table: Tag):
    if table.attrs.get("align", "") == "right":
        return None
    formated_table = flatten_table(soup, table)
    header = formated_table[0]
    for row in formated_table[1:]:
        if not all(row):
            continue
        yield dict(zip(header, row))


def extract_date(date: str, format: str = "%B %d, %Y") -> date:
    try:
        return datetime.strptime(date, format).date()
    except ValueError:
        if "note" in date.lower():
            dates = DOUBLE_DATE_RE.findall(date)
            return extract_date(dates[0], format)
        if "/" in date:
            date = DOUBLE_DAY_RE.sub("", date)
            return extract_date(date, format)
        print("[DATE ERROR]", date)
        return None


def parse_full_release(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        update = row.get("Update")
        version = row.get("Version")
        release = extract_date(row.get("Full release"))
        yield update, version, release


def parse_beta(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        update = row.get("Update")
        version = row.get("Version")
        release = extract_date(row.get("Release date", row.get("Full release")))
        yield update, version, release


def parse_alpha(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        update = row.get("Update")
        version = row.get("Client Version")
        if version == "N/A":
            continue
        release = extract_date(row.get("Release date"))
        yield update, version, release


def parse_infdev(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        version = row.get("Version/release date")
        update = INFDEV_RE.sub(r"\1", version)
        release = extract_date(INFDEV_RE.sub(r"\2-\3-\4", version), "%Y-%m-%d")
        yield update, version, release


def parse_indev(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        version = row.get("Version")
        update = INDEV_RE.sub(r"\1", version)
        update = "Minecraft Indev" if update == "Indev" else update
        release = extract_date(INDEV_RE.sub(r"\2-\3-\4", version), "%Y-%m-%d")
        yield update, version, release


def parse_classic(soup: BeautifulSoup, table: Tag):
    update = table.find_previous("h3").find("span", {"class": "mw-headline"}).text.strip()
    for row in parse_version_table(soup, table):
        release = extract_date(row.get("Release date"))
        match update:
            case "Late Classic":
                version = row.get("Client version")
            case "Survival Test":
                version = row.get("Version")
            case "Multiplayer Test":
                version = row.get("Client version")
            case "Early Classic":
                version = row.get("Version")
            case "Private test builds":
                version = row.get("Version")
            case _:
                raise ValueError(f"Unknown update: {update}")

        yield update, version, release


def parse_preclassic(soup: BeautifulSoup, table: Tag):
    for row in parse_version_table(soup, table):
        update = "Pre-classic"
        version = row.get("Version")
        release = extract_date(row.get("Creation date"))
        yield update, version, release


def fetch_versions(BASE_URI, db: SQLAlchemy):
    URL = BASE_URI % "Java_Edition_version_history"
    response = rq.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    h2: ResultSet[Tag] = soup.find_all("h2")
    for h in range(len(h2) - 1):
        current, next = h2[h], h2[h + 1]
        if current.text.strip() == "Contents":
            continue
        head_title = current.find("span", {"class": "mw-headline"}).text.strip()
        after = set(current.find_all_next("table", {"class": "wikitable"}))
        before = set(next.find_all_previous("table", {"class": "wikitable"}))
        tables = after & before

        for table in tables:
            if head_title.startswith("Full release"):
                parsing_method = parse_full_release
            elif head_title.startswith("Beta"):
                parsing_method = parse_beta
            elif head_title.startswith("Alpha"):
                parsing_method = parse_alpha
            elif head_title.startswith("Infdev"):
                parsing_method = parse_infdev
            elif head_title.startswith("Indev"):
                parsing_method = parse_indev
            elif head_title.startswith("Classic"):
                parsing_method = parse_classic
            elif head_title.startswith("Pre-Classic"):
                parsing_method = parse_preclassic

            for update, version, release in parsing_method(soup, table):
                update = CLEAN_UPDATE_RE.sub("", update).strip()
                version = CLEAN_VERSION_RE.sub("", version).strip()
                print(update, "/", version, "/", release)
                if Version.query.get(version) is None:
                    db.session.add(Version(version=version, release_date=release, update=update))

    db.session.commit()
