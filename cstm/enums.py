from enum import Enum


class TransactionType(Enum):
    PURCHASE = "Purchase"
    SALE = "Sale"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class State(Enum):
    DELAWARE = "DE"
    PENNSYLVANIA = "PA"
    NEW_JERSEY = "NJ"
    GEORGIA = "GA"
    CONNECTICUT = "CT"
    MASSACHUSETTS = "MA"
    MARYLAND = "MD"
    SOUTH_CAROLINA = "SC"
    NEW_HAMPSHIRE = "NH"
    VIRGINIA = "VA"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    RHODE_ISLAND = "RI"
    VERMONT = "VT"
    KENTUCKY = "KY"
    TENNESSEE = "TN"
    OHIO = "OH"
    LOUISIANA = "LA"
    INDIANA = "IN"
    MISSISSIPPI = "MS"
    ILLINOIS = "IL"
    ALABAMA = "AL"
    MAINE = "ME"
    MISSOURI = "MO"
    ARKANSAS = "AR"
    MICHIGAN = "MI"
    FLORIDA = "FL"
    TEXAS = "TX"
    IOWA = "IA"
    WISCONSIN = "WI"
    CALIFORNIA = "CA"
    MINNESOTA = "MN"
    OREGON = "OR"
    KANSAS = "KS"
    WEST_VIRGINIA = "WV"
    NEVADA = "NV"
    NEBRASKA = "NE"
    COLORADO = "CO"
    NORTH_DAKOTA = "ND"
    SOUTH_DAKOTA = "SD"
    MONTANA = "MT"
    WASHINGTON = "WA"
    IDAHO = "ID"
    WYOMING = "WY"
    UTAH = "UT"
    OKLAHOMA = "OK"
    NEW_MEXICO = "NM"
    ARIZONA = "AZ"
    ALASKA = "AL"
    HAWAII = "HI"

    def __str__(self) -> str:
        return self.name.title().replace('_', ' ')

    def __repr__(self) -> str:
        return self.name.title().replace('_', ' ')

    def abbrev(self) -> str:
        return self.value

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in cls._value2member_map_
