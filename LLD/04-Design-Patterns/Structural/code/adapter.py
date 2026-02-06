"""
Adapter Pattern - Converts the interface of a class into another
interface that clients expect. Lets incompatible interfaces work together.

Examples:
1. Legacy XML payment system adapted to modern JSON interface
2. Temperature adapter (Celsius/Fahrenheit/Kelvin)
"""
import json


# --- Payment Adapter ---
class LegacyXMLPayment:
    """Old system that only processes XML."""
    def process_xml_payment(self, xml_data: str) -> str:
        return f"  [Legacy] Processed XML payment: {xml_data[:60]}..."

    def get_xml_receipt(self) -> str:
        return "<receipt><status>OK</status><id>TXN-001</id></receipt>"


class ModernPaymentInterface:
    """Modern interface the client expects."""
    def pay(self, data: dict) -> dict:
        raise NotImplementedError

    def get_receipt(self) -> dict:
        raise NotImplementedError


class PaymentAdapter(ModernPaymentInterface):
    """Adapts LegacyXMLPayment to ModernPaymentInterface."""

    def __init__(self, legacy_system: LegacyXMLPayment):
        self._legacy = legacy_system

    def _dict_to_xml(self, data: dict) -> str:
        xml = "<payment>"
        for key, val in data.items():
            xml += f"<{key}>{val}</{key}>"
        xml += "</payment>"
        return xml

    def _xml_to_dict(self, xml: str) -> dict:
        result = {}
        import re
        for match in re.finditer(r"<(\w+)>(.*?)</\1>", xml):
            result[match.group(1)] = match.group(2)
        return result

    def pay(self, data: dict) -> dict:
        xml_data = self._dict_to_xml(data)
        result = self._legacy.process_xml_payment(xml_data)
        return {"status": "success", "message": result}

    def get_receipt(self) -> dict:
        xml_receipt = self._legacy.get_xml_receipt()
        return self._xml_to_dict(xml_receipt)


# --- Temperature Adapter ---
class CelsiusSensor:
    def __init__(self, temp: float):
        self.temperature = temp

    def get_temperature(self) -> float:
        return self.temperature


class FahrenheitAdapter:
    def __init__(self, sensor: CelsiusSensor):
        self._sensor = sensor

    def get_temperature(self) -> float:
        return self._sensor.get_temperature() * 9 / 5 + 32


class KelvinAdapter:
    def __init__(self, sensor: CelsiusSensor):
        self._sensor = sensor

    def get_temperature(self) -> float:
        return self._sensor.get_temperature() + 273.15


if __name__ == "__main__":
    print("=" * 60)
    print("ADAPTER PATTERN DEMO")
    print("=" * 60)

    # Payment Adapter
    print("\n--- Payment Adapter (XML -> JSON) ---")
    legacy = LegacyXMLPayment()
    adapter = PaymentAdapter(legacy)

    payment_data = {"amount": 99.99, "currency": "USD", "card": "****1234"}
    print(f"  Client sends JSON: {json.dumps(payment_data)}")
    result = adapter.pay(payment_data)
    print(f"  Result: {result}")
    receipt = adapter.get_receipt()
    print(f"  Receipt (as dict): {receipt}")

    # Temperature Adapter
    print("\n--- Temperature Adapter ---")
    sensor = CelsiusSensor(100.0)
    fahrenheit = FahrenheitAdapter(sensor)
    kelvin = KelvinAdapter(sensor)

    print(f"  Celsius:    {sensor.get_temperature():.1f} C")
    print(f"  Fahrenheit: {fahrenheit.get_temperature():.1f} F")
    print(f"  Kelvin:     {kelvin.get_temperature():.2f} K")

    print("\n  Boiling point verified:")
    print(f"    100C == {fahrenheit.get_temperature()}F == {kelvin.get_temperature()}K")
