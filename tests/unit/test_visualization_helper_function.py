from visualization.helper_functions import purchase_sale_conversion_query, purchase_sale_sum_on_time
from cstm.database_helpers import get_db_connection, table_name, db_file_path
import unittest
from datetime import datetime

class PurchaseSaleConversionQueryTestCase(unittest.TestCase):
    def test_query_work_as_expected(self):
        connection = get_db_connection(db_file_path)
        expected_query = "SELECT company, ticker, id, member_name, transaction_date," \
                         " CASE transaction_type WHEN 'P' THEN value_lb ELSE 0 END AS purchase_lb," \
                         " CASE transaction_type WHEN 'P' THEN value_ub ELSE 0 END AS purchase_ub," \
                         " CASE transaction_type WHEN 'S' THEN -1*value_lb ELSE 0 END AS sale_lb," \
                         " CASE transaction_type WHEN 'S' THEN -1*value_ub ELSE 0 END AS sale_ub" \
                         " FROM all_transaction"
        query = purchase_sale_conversion_query()
        cursor = connection.cursor()
        data_1 = cursor.execute(expected_query)
        data_1 = data_1.fetchall()
        data_1 = [tuple(entry) for entry in data_1]
        data_2 = cursor.execute(query)
        data_2 = data_2.fetchall()
        data_2 = [tuple(entry) for entry in data_2]
        self.assertEqual(len(data_1), len(data_2))
        for data in data_1:
            self.assertIn(data, data_2)


class PurchaseSaleSumOnTimeQueryTestCase(unittest.TestCase):
    def test_query_work_as_expected(self):
        connection = get_db_connection(db_file_path)
        expected_query = f"WITH temp as ({purchase_sale_conversion_query()}) " \
                         f"SELECT COUNT(id) AS num_transactions, " \
                         f"COUNT(DISTINCT member_name) AS num_members, " \
                         f"SUM(purchase_lb) as purchase_lb, " \
                         f"SUM(purchase_ub) as purchase_ub, " \
                         f"SUM(sale_lb) as sale_lb, " \
                         f"SUM(sale_ub) as sale_ub, " \
                         f"transaction_date " \
                         f"FROM temp " \
                         f"WHERE ((transaction_date BETWEEN '2013-01-01' AND '2022-05-10') " \
                         f"AND ticker like '%e%' AND member_name like '%e%' AND company like '%e%') " \
                         f"GROUP BY transaction_date"
        date_lower = datetime(year=2013, month=1, day=1)
        date_upper = datetime.now()
        query = purchase_sale_sum_on_time(date_lower, date_upper, 'e', 'e', 'e')
        cursor = connection.cursor()
        data_1 = cursor.execute(expected_query)
        data_1 = data_1.fetchall()
        data_1 = [tuple(entry) for entry in data_1]
        data_2 = cursor.execute(query)
        data_2 = data_2.fetchall()
        data_2 = [tuple(entry) for entry in data_2]
        self.assertEqual(len(data_1), len(data_2))
        for data in data_1:
            self.assertIn(data, data_2)



