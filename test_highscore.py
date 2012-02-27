#!/usr/bin/env python

import unittest

from highscore import HighScoreTable


class TestAddScore(unittest.TestCase):
    def setUp(self):
        self.table = HighScoreTable()

    def test_add_not_empty(self):
        """table should not be empty after add"""
        self.table.add_score('Bob', 100)
        self.assertFalse(self.table.is_empty())

    def test_add_correct_order(self):
        """adding scores should keep list sorted"""
        self.table.add_score('Bob', 100)
        self.table.add_score('Jake', 500)
        self.table.add_score('Tim', 50)
        self.assertEqual(self.table.scores[0][0], 'Jake')
        self.assertEqual(self.table.scores[1][0], 'Bob')
        self.assertEqual(self.table.scores[2][0], 'Tim')

    def test_drop_lowest_score(self):
        """adding more than max_length should drop lowest scores"""
        pass


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
        pass
    
    def test_file_exists(self):
        """file exists after write"""
        pass

    def test_empty_table_doesnt_write(self):
        """an empty high score table should create a file"""
        pass


class TestReadTableFromFile(unittest.TestCase):
    pass


if  __name__ == "__main__":
    unittest.main()
