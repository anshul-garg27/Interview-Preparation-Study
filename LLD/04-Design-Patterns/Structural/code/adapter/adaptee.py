"""Adaptee - legacy XML data system with incompatible interface."""


class LegacyXMLSystem:
    """Old system that only provides XML data."""

    def __init__(self):
        self._data = (
            "<users>"
            "<user><name>Alice</name><age>30</age></user>"
            "<user><name>Bob</name><age>25</age></user>"
            "</users>"
        )

    def fetch_xml(self) -> str:
        return self._data

    def get_xml_record_count(self) -> int:
        return self._data.count("<user>")
