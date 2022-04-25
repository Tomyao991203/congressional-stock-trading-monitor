import unittest
from cstm.enums import State


class StateToStringTestCase(unittest.TestCase):

    def test_strings_all_words_capitalized(self):
        for state in State:
            for word in str(state).split(' '):
                self.assertTrue(word[0].isupper())
                for char in word[1:]:
                    self.assertTrue(char.islower())

    def test_abbrev_is_two_letters(self):
        for state in State:
            self.assertEqual(len(state.abbrev()), 2)
