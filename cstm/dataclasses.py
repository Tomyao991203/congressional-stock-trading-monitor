from datetime import date
from dataclasses import dataclass
from statistics import mean
import re

from cstm.enums import State, TransactionType


@dataclass
class District:
    """
    This class is responsible for storing information about a state congressional district
    """
    state: State
    number: int

    def __str__(self):
        return self.state.abbrev() + str(self.number).zfill(2)

    @classmethod
    def from_district_string(cls, district_str: str):
        match = re.match(r'^([A-Z]{2})([0-9]{2})$', district_str)
        if not match:
            raise Exception("Invalid District String")

        state = match.group(1)
        number = int(match.group(2))

        if not State.has_value(state) or number < 1:
            raise Exception("Invalid District String")

        return cls(State(state), number)


@dataclass
class Representative:
    """
    This class is responsible for holding information about a member of the House of Representatives
    as well as facilitating computations using this data
    """
    name: str
    district_by_year: dict[int, District]
    trade_count: int
    purchase_count: int
    sale_count: int
    avg_transaction_value: float
    total_purchase_range: tuple[float, float]
    total_sale_range: tuple[float, float]


@dataclass
class Transaction:
    """
    This class is responsible for holding information about a single Transaction stored in the database.
    Database query functions will return a list of this type, providing a common data type and API system-wide.
    """
    id: int
    member_name: str
    member_district: District
    company: str
    ticker: str
    type: TransactionType
    date: date
    value_range: tuple[float, float]
    description: str or None

    def get_average_value(self) -> float:
        """
        :return: The average value of this transaction, which is the midpoint between its value bounds
        """
        return mean(self.value_range)
