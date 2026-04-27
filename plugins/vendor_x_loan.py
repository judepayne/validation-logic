"""
Example vendor loan plugin.

Converts a small vendor-style loan dict into the canonical loan v1 schema.
This is intentionally simple and is used as a reference implementation for
plugin authors and tests.
"""

from plugins.base import PluginError, ValidationPlugin

LOAN_V1_SCHEMA = (
    "https://raw.githubusercontent.com/judepayne/validation-logic/main/"
    "models/loan.schema.v1.0.0.json"
)


class Plugin(ValidationPlugin):
    """Convert example vendor loan payloads into canonical loan v1 entities."""

    def convert(self, input_data):
        """Convert one vendor payload into one canonical loan entity."""
        if not isinstance(input_data, dict):
            raise PluginError("Vendor loan payload must be a dict")

        required_fields = [
            "vendor_id",
            "loan_ref",
            "facility_ref",
            "amount",
            "currency",
            "rate",
            "origination",
            "maturity",
            "status",
        ]
        missing = [field for field in required_fields if field not in input_data]
        if missing:
            raise PluginError(
                "Vendor loan payload missing required field(s): "
                + ", ".join(missing)
            )

        return {
            "$schema": LOAN_V1_SCHEMA,
            "id": input_data["vendor_id"],
            "loan_number": input_data["loan_ref"],
            "facility_id": input_data["facility_ref"],
            "financial": {
                "principal_amount": input_data["amount"],
                "outstanding_balance": input_data.get(
                    "outstanding_balance", input_data["amount"]
                ),
                "currency": input_data["currency"],
                "interest_rate": input_data["rate"],
            },
            "dates": {
                "origination_date": input_data["origination"],
                "maturity_date": input_data["maturity"],
            },
            "status": input_data["status"],
        }
