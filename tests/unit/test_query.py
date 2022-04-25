from cstm.query import where_condition, equal_condition, expression_wrapper, cases_str
import unittest


class WhereConditionTestCase(unittest.TestCase):
    def test_empty_value(self):
        self.assertTrue(where_condition('a', None) == 'True')
        self.assertTrue(where_condition('a', '') == 'True')

    def test_simple_value(self):
        self.assertTrue(where_condition('a', 1000) == 'a = 1000')
        self.assertTrue(where_condition('a', 'a') == 'a = \'a\'')


class ExpressionWrapperTestCases(unittest.TestCase):
    def test_empty_value(self):
        self.assertEqual(expression_wrapper("", is_str=True), "")
        self.assertEqual(expression_wrapper("", is_str=False), "")

    def test_is_str_True(self):
        self.assertEqual(expression_wrapper("a", is_str=True), "\'a\'")
        self.assertEqual(expression_wrapper("0", is_str=True), "\'0\'")

    def test_is_str_False(self):
        self.assertEqual(expression_wrapper("a", is_str=False), "a")
        self.assertEqual(expression_wrapper("0", is_str=False), "0")
        self.assertEqual(expression_wrapper("0 > -1", is_str=False), "0 > -1")


class EqualConditionTestCases(unittest.TestCase):
    def test_empty_value(self):
        self.assertEqual(equal_condition("", "a"), "TRUE")
        self.assertEqual(equal_condition("", ""), "TRUE")
        self.assertEqual(equal_condition("b", ""), "TRUE")

    def test_string_value(self):
        self.assertEqual(equal_condition("a", "a"), "a = \'a\'")

    def test_non_string_value(self):
        self.assertEqual(equal_condition("a", "a", value_is_string=False), "a = a")


class CasesStrTestCases(unittest.TestCase):
    def test_empty_case_value_pairs_throw_exception(self):
        with self.assertRaises(Exception):
            cases_str(expression="", case_value_pairs=dict(), else_value=0, key_is_str=True,
                      value_is_str=True, as_var_name='var_name')

    def test_one_case(self):
        run_result_no_expression = cases_str(expression="", case_value_pairs={'a > 10': 'a is bigger than 10'},
                                             else_value='a <= 10',
                                             key_is_str=False, value_is_str=True, as_var_name='var_name')

        expect_result_1 = 'CASE  WHEN a > 10 THEN \'a is bigger than 10\' ELSE \'a <= 10\' END AS var_name'

        run_result_has_expression = cases_str(expression="A", case_value_pairs={'10': 'A is 10'},
                                              else_value='A does not equals to 10',
                                              key_is_str=False, value_is_str=True, as_var_name='var_name')

        expect_result_2 = 'CASE A WHEN 10 THEN \'A is 10\' ELSE \'A does not equals to 10\' END AS var_name'

        run_result_key_string_value = cases_str(expression="A", case_value_pairs={'10': 'A is 10'},
                                                else_value='A does not equals to 10',
                                                key_is_str=True, value_is_str=True, as_var_name='var_name')
        expect_result_3 = 'CASE A WHEN \'10\' THEN \'A is 10\' ELSE \'A does not equals to 10\' END AS var_name'

        run_result_value_non_string_value = cases_str(expression="A", case_value_pairs={'10': 'B'},
                                                      else_value='C',
                                                      key_is_str=True, value_is_str=False, as_var_name='var_name')
        expect_result_4 = 'CASE A WHEN \'10\' THEN B ELSE C END AS var_name'

        self.assertEqual(run_result_no_expression, expect_result_1)
        self.assertEqual(run_result_has_expression, expect_result_2)
        self.assertEqual(run_result_key_string_value, expect_result_3)
        self.assertEqual(run_result_value_non_string_value, expect_result_4)

    def test_one_plus_conditions(self):
        key_value_pairs = dict()
        for i in range(1,4):
            key_value_pairs[f'A_{i}'] = f'V_{i}'
        run_result = cases_str(expression="expression", case_value_pairs=key_value_pairs,
                               else_value='V_n', key_is_str=False, value_is_str=False, as_var_name='var_name')
        expect_result = 'CASE expression WHEN A_1 THEN V_1 ' \
                        'WHEN A_2 THEN V_2 ' \
                        'WHEN A_3 THEN V_3 ELSE V_n END AS var_name'
        self.assertEqual(run_result, expect_result)


if __name__ == '__main__':
    unittest.main()
