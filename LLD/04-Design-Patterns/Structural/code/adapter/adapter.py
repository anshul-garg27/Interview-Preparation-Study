"""Adapter - converts XML legacy system to JSON interface."""

import re
from target import JSONDataProvider
from adaptee import LegacyXMLSystem


class XMLtoJSONAdapter(JSONDataProvider):
    """Wraps the legacy XML system, exposing a JSON interface."""

    def __init__(self, xml_system: LegacyXMLSystem):
        self._xml_system = xml_system

    def get_json_data(self) -> dict:
        xml = self._xml_system.fetch_xml()
        users = []
        for match in re.finditer(
            r"<user><name>(.*?)</name><age>(.*?)</age></user>", xml
        ):
            users.append({"name": match.group(1), "age": int(match.group(2))})
        return {"users": users}

    def get_record_count(self) -> int:
        return self._xml_system.get_xml_record_count()
