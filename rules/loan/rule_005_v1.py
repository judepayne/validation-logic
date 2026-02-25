"""Warn when outstanding balance exceeds 85% of principal"""

from rules.base import ValidationRule


class Rule(ValidationRule):
    """Warns when a loan's outstanding balance is more than 85% of its original principal."""

    def validates(self) -> str:
        return "loan"

    def required_data(self) -> list:
        return []

    def description(self) -> str:
        return "Outstanding balance must not exceed 85% of principal"

    def set_required_data(self, data: dict) -> None:
        pass

    def run(self) -> tuple:
        """Warn if balance / principal > 0.85 (loan barely repaid)."""
        principal = self.entity.principal
        balance = self.entity.balance

        if principal is None:
            return ("NORUN", "Cannot access principal amount")
        if balance is None:
            return ("NORUN", "Outstanding balance is absent")

        ratio = balance / principal
        if ratio > 0.85:
            pct = round(ratio * 100, 1)
            return ("WARN", f"Outstanding balance is {pct}% of principal — loan has barely been repaid")

        return ("PASS", "Balance repayment ratio is acceptable")
