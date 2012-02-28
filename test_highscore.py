#!/usr/bin/env python

import unittest
import pickle

from highscore import HighScoreTable


class TestAddScore(unittest.TestCase):
    def setUp(self):
        self.table = HighScoreTable()
        self.table.add_score('Bob', 100)
        self.table.add_score('Jake', 500)
        self.table.add_score('Tim', 50)
        self.table.max_length = 5 # only five

    def test_add_not_empty(self):
        """table should not be empty after add"""
        self.assertFalse(self.table.is_empty())

    def test_add_correct_order(self):
        """adding scores should keep list sorted"""
        self.assertEqual(self.table.scores[0][0], 'Jake')
        self.assertEqual(self.table.scores[1][0], 'Bob')
        self.assertEqual(self.table.scores[2][0], 'Tim')

    def test_drop_lowest_score(self):
        """adding more than max_length should drop lowest scores"""
        self.table.add_score('Fung', 1000)
        self.table.add_score('Zutroy', 400)
        self.table.add_score('Dildor', 60)
        # there are now six, Tim should disappear
        self.assertEqual(self.table.scores[4][0], 'Dildor')
        self.assertEqual(len(self.table.scores), self.table.max_length)


class TestSortTable(unittest.TestCase):
    def setUp(self):
        self.table = HighScoreTable()
        # add scores directly, bypass add_score() function ('cause this will
        # sort them)
        self.table.scores.append(('Bob', 100))
        self.table.scores.append(('Joe', 30))
        self.table.scores.append(('Billy', 500))
        self.table.scores.append(('Krog', 5))

    def test_sorted(self):
        """sort() function should sort table in descending order by score"""
        self.table.sort()
        self.assertEqual(self.table.scores[0][0], 'Billy')
        self.assertEqual(self.table.scores[1][0], 'Bob')
        self.assertEqual(self.table.scores[2][0], 'Joe')
        self.assertEqual(self.table.scores[3][0], 'Krog')


class TestWriteTableToFile(unittest.TestCase):
    def setUp(self):
        self.table = HighScoreTable()
        # adding keeps them in order...
        self.table.add_score('Bob', 100)
        self.table.add_score('Jake', 500)
        self.table.add_score('Tim', 50)
        self.table.write_to_file()
    
    def test_file_exists(self):
        """file exists after write, filled with correct data"""
        test_file = open(self.table.file_name, 'rb')
        self.assertEqual(self.table.scores, pickle.load(test_file))
        test_file.close()

    def test_empty_table_doesnt_write(self):
        """an empty high score table shouldn't create a file"""
        pass

    def test_raise_proper_exception(self):
        """if we can't write, the correct exception is raised"""
        pass


class TestReadTableFromFile(unittest.TestCase):
    pass


if  __name__ == "__main__":
    unittest.main()
