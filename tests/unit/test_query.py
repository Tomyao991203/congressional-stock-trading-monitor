from cstm.query import where_condition
import unittest
import random

class WhereConditionTestCase(unittest.TestCase):
    def test_empty_value(self):
        self.assertTrue(where_condition('a', None) == 'True')
        self.assertTrue(where_condition('a', '') == 'True')
    
    def test_simple_value(self):
        self.assertTrue(where_condition('a', 1000) == 'a = 1000')
        self.assertTrue(where_condition('a', 'a') == 'a = \'a\'')
        
if __name__ == '__main__':
    unittest.main()