from collections import defaultdict
from datetime import date
from statistics import mean

from cstm.database_helpers import get_transactions_between
from cstm.dataclasses import Representative, Transaction
from cstm.enums import TransactionType


def representative_list(date_lower: date, date_upper: date) -> list[Representative]:
    """
    This method make a database query for all Representatives that were in office at some point in the
    given date range

    :param date_lower: The lower bound of the query
    :param date_upper: The upper bound of the query
    :return: A list of Representative objects populated from all transactions in the given range
    """
    transactions = get_transactions_between(date_lower, date_upper)
    if not transactions:
        return []

    return representatives_from_transactions(transactions)


def representatives_from_transactions(transactions: list[Transaction]) -> list[Representative]:
    """
    This method populates Representative objects with the information found in the
    given list of transactions

    :param transactions: The list of transactions to determine Representative info from
    :return: A list of Representative objects populated from the given transaction list
    """
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
            curr_rep.total_sale_range = (curr_rep.total_sale_range[0] + transaction.value_range[0],
                                         curr_rep.total_sale_range[1] + transaction.value_range[1])
        elif transaction.type == TransactionType.PURCHASE:
            curr_rep.purchase_count += 1
            curr_rep.total_purchase_range = (curr_rep.total_purchase_range[0] + transaction.value_range[0],
                                             curr_rep.total_purchase_range[1] + transaction.value_range[1])

        avg_values_by_name[name].append(transaction.get_average_value())
        representatives_by_name[name] = curr_rep

    # Populate Average Transaction Values
    for representative in representatives_by_name.keys():
        avg_values = avg_values_by_name[representative]
        representatives_by_name[representative].avg_transaction_value = mean(avg_values)

    return list(representatives_by_name.values())
