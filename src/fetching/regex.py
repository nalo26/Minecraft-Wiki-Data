import re

CLEAN_UPDATE_RE = re.compile(r"\s*\(Guide\)")
REMOVE_PARENTHESES_RE = re.compile(r"\s*\(.*\)")

DOUBLE_DATE_RE = re.compile(r"(\w+\s\d{1,2},\s\d{4})")
DOUBLE_DAY_RE = re.compile(r"/\d{1,2}")

INFDEV_RE = re.compile(r"(\w+)\s([\d]{4})([\d]{2})([\d]{2}).*")
INDEV_RE = re.compile(r"(\w+(?:\s\d+.\d+)?)\s([\d]{4})([\d]{2})([\d]{2}).*")

IMAGE_BLOCK_LINK_RE = re.compile(r"/w/File:(.*\.png)")
EXTRACT_NUMBER_RE = re.compile(r"([\d.]+)")

TOOL_LINK_RE = re.compile(r"/w/(.*)")

ADDED_RE = re.compile("Added")
