from collections import defaultdict
from datetime import date
from statistics import mean

from cstm.database_helpers import get_transactions_between
from cstm.dataclasses import Representative
from cstm.enums import TransactionType


def representative_list(date_lower: date, date_upper: date) -> list[Representative]:
    """
    This method make a database query for all Representatives that were in office at some point in the
    given date range

    :param date_lower: The lower bound of the query
    :param date_upper: The upper bound of the query
    :return: A dictionary mapping strings (State Names) to a list of all members who served in that state. Each entry
             in that list will be a dictionary with the following fields: Name, District, Number of Trades, Number of
             Purchases, Number of Sales, Average Transaction Value, Total Purchase Value Lower/Upper Bound, Total Sale
             Value Lower/Upper Bound.
             If the year range is not valid, the empty dictionary is returned.
    """
    transactions = get_transactions_between(date_lower, date_upper)
    if not transactions:
        return []

    representatives_by_name: dict[str, Representative] = {}
    avg_values_by_name: dict[str, list[float]] = defaultdict(lambda: [])

    for transaction in transactions:
        curr_rep = representatives_by_name.get(transaction.member_name)
        name = transaction.member_name
        district = transaction.member_district
        year = transaction.date.year
        if curr_rep is None:
            curr_rep = Representative(name, {year: district}, 0, 0, 0, 0, (0, 0), (0, 0))
        # Update fields with current transaction
        if year not in curr_rep.district_by_year.keys():
            curr_rep.district_by_year[year] = district

        curr_rep.trade_count += 1
        if transaction.type == TransactionType.SALE:
            curr_rep.sale_count += 1
            curr_rep.total_purchase_range = tuple(x+y for x, y in zip(curr_rep.total_purchase_range,
                                                                      transaction.value_range))
        elif transaction.type == TransactionType.PURCHASE:
            curr_rep.purchase_count += 1
            curr_rep.total_sale_range = tuple(x+y for x, y in zip(curr_rep.total_purchase_range,
                                              transaction.value_range))

        avg_values_by_name[name].append(transaction.get_average_value())
        representatives_by_name[name] = curr_rep

    # Populate Average Transaction Values
    for representative in representatives_by_name.keys():
        avg_values = avg_values_by_name[representative]
        representatives_by_name[representative].avg_transaction_value = mean(avg_values)

    return list(representatives_by_name.values())
