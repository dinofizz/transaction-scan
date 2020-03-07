import logging
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    date: datetime.date = None
    amount: int = 0
    description: str = ""
    account: str = ""
    category: str = "unknown"
    reference: str = ""
    _income_expense: str = "E"

    @property
    def income_expense(self) -> str:
        return self._income_expense

    @income_expense.setter
    def income_expense(self, s: str) -> None:
        s = s.upper()
        if s not in ["I", "E"]:
            logging.error("Unsupported string for income/expense.")
        else:
            self._income_expense = s
