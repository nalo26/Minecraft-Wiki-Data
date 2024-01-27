import re

CLEAN_UPDATE_RE = re.compile(r"\s*\(Guide\)")
CLEAN_VERSION_RE = re.compile(r"\s*\(.*\)")

DOUBLE_DATE_RE = re.compile(r"(\w+\s\d{1,2},\s\d{4})")
DOUBLE_DAY_RE = re.compile(r"/\d{1,2}")

INFDEV_RE = re.compile(r"(\w+)\s([\d]{4})([\d]{2})([\d]{2}).*")
INDEV_RE = re.compile(r"(\w+(?:\s\d+.\d+)?)\s([\d]{4})([\d]{2})([\d]{2}).*")
