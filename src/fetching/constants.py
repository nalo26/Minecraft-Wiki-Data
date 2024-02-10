import re

CLEAN_UPDATE_RE = re.compile(r"\s*\(Guide\)")
REMOVE_PARENTHESES_RE = re.compile(r"\s*\((.*)\)")
REMOVE_NOTE_RE = re.compile(r"\s*\[(.*)\]")

DOUBLE_DATE_RE = re.compile(r"(\w+\s\d{1,2},\s\d{4})")
DOUBLE_DAY_RE = re.compile(r"/\d{1,2}")

INFDEV_RE = re.compile(r"(\w+)\s([\d]{4})([\d]{2})([\d]{2}).*")
INDEV_RE = re.compile(r"(\w+(?:\s\d+.\d+)?)\s([\d]{4})([\d]{2})([\d]{2}).*")

FILE_LINK_RE = re.compile(r"/w/File:(.*\.[png|gif|jpg|jpeg])")
EXTRACT_NUMBER_RE = re.compile(r"([\d.]+)")

TOOL_LINK_RE = re.compile(r"/w/(.*)")

ADDED_RE = re.compile("Added")

HEIGHT_RE = re.compile(r"height:\s?([\d.]+)\s?blocks?")
WIDTH_RE = re.compile(r"width:\s?([\d.]+)\s?blocks?")

SPACE_SEPARATOR = "\u200C"

EXCEPTIONS = {
    "Light Block": "light",
    "Lava": "lava",
    "Oak Trapdoor": "oak_trapdoor",  # table cell does not exists
    "Polished Blackstone Brick Wall": "polished_blackstone_brick_wall",  # typo in table
    "Polished Blackstone Wall": "polished_blackstone_wall",  # typo in table
    "Redstone Wire": "redstone_wire",
    "Water": "water",
    "Disc Fragment": "disc_fragment_5",  # CD name, but not considerd as a CD
    "Echo Shard": "echo_shard",  # ID table does not exists
    "Scute": "scute",  # TODO: change in 1.20.5
}

IGNORES = {"Ominous Banner", "Spawn NPC"}
