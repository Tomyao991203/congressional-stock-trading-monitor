from cstm.enums import State
from datetime import datetime
from datetime import date as Date
from dataclasses import dataclass


@dataclass
class District:
    """
    This class is responsible for storing information about a state congressional district
    """
    state: State
    number: int

    def __str__(self):
        return state.abbrev() + str(number)


@dataclass
class Representative:
    """
    This class is responsible for holding information about a member of the House of Representatives
    as well as facilitating computations using this data
    """
    name: str
    district: str
    trade_count: int
    purchase_count: int
    sale_count: int
    avg_transaction_value: int
    total_purchase_range: tuple[int, int]
    total_sale_range: tuple[int, int]


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
    type: str
    date: Date
    value_range: tuple[float, float]
    description: str

    def get_average_value(self) -> float:
        """
        :return: The average value of this transaction, which is the midpoint between its value bounds
        """
        return sum(self.value_range) / len(self.value_range)
