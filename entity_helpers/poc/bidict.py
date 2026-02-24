"""
BiDict — bidirectional field map with dot-notation navigation.

Stores logical→physical field mappings once and supports lookup in both
directions, plus value retrieval from nested dicts via dot-notation paths.
"""


class BiDict:
    """Bidirectional map between logical field names and physical dot-notation paths.

    Example:
        fields = BiDict([
            ("reference",  "loan_number"),
            ("principal",  "financial.principal_amount"),
            ("maturity",   "dates.maturity_date"),
        ])

        fields.physical("principal")          # → "financial.principal_amount"
        fields.logical("loan_number")         # → "reference"
        fields.get(loan_data, "principal")    # → 500000.0
    """

    def __init__(self, pairs: list):
        self._fwd = dict(pairs)                     # logical → physical path
        self._rev = {v: k for k, v in pairs}        # physical path → logical

    def physical(self, logical: str) -> str:
        """Return the physical dot-notation path for a logical field name."""
        return self._fwd[logical]

    def logical(self, physical: str) -> str:
        """Return the logical field name for a physical dot-notation path."""
        return self._rev[physical]

    def get(self, data: dict, logical: str):
        """Retrieve a value from a nested dict using the logical field name."""
        for key in self._fwd[logical].split("."):
            if not isinstance(data, dict):
                return None
            data = data.get(key)
        return data

    def __contains__(self, logical: str) -> bool:
        return logical in self._fwd

    def logical_keys(self) -> list:
        return list(self._fwd.keys())

    def physical_paths(self) -> list:
        return list(self._rev.keys())
