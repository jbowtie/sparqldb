#! /usr/bin/env python
import sys, os.path

from sparqldb import dbapi
import unittest
from . import testdb

test_select_all = "SELECT user_id, freetext_answer as answer FROM survey"
test_select_order_by = "SELECT user_id FROM survey ORDER BY question_id" #[6,5,4]
test_select_order_by_desc = "SELECT user_id FROM survey ORDER BY user_id DESC" #[6,5,4]
test_select_order_by_asc = "SELECT user_id FROM survey ORDER BY user_id ASC" #[4,5,6]
test_select_limit = "SELECT user_id, freetext_answer as answer FROM survey LIMIT 2"
test_select_offset = "SELECT user_id FROM survey ORDER BY user_id ASC OFFSET 1"
test_select_with_param = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = %s"
test_select_with_string_param = "SELECT user_id FROM survey WHERE freetext_answer = %s"
test_select_with_named_param = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = %(id)s"
test_select_literal_value = "SELECT 10, user_id FROM survey WHERE question_id = 8"
test_select_only_literals = "SELECT 10 FROM survey WHERE question_id = 8"
test_select_only_literals_with_no_rows_returned = "SELECT 10 FROM survey WHERE question_id = 47"
test_select_with_table_names = "SELECT survey.user_id, survey.freetext_answer as answer FROM survey ORDER BY user_id LIMIT 1"

class selectSuite(unittest.TestCase):
    def setUp(self):
        self.conn = testdb.setup_test_db()

    def testSelectExplicitColumnsFromTable(self):
        cur = self.conn.cursor()
        cur.execute(test_select_all)
        results = cur.fetchall()
        self.assertEqual(3, len(results))

    def testOrderBy(self):
        """Ordering by question_id will return descending user_id values"""
        cur = self.conn.cursor()
        cur.execute(test_select_order_by)
        results = cur.fetchall()
        self.assertEqual(3, len(results))
        self.assertEqual(6, results[0][0])
        self.assertEqual(5, results[1][0])
        self.assertEqual(4, results[2][0])

    def testOrderByDesc(self):
        """Ordering by user_id DESC values"""
        cur = self.conn.cursor()
        cur.execute(test_select_order_by_desc)
        results = cur.fetchall()
        self.assertEqual(6, results[0][0])
        self.assertEqual(5, results[1][0])
        self.assertEqual(4, results[2][0])

    def testOrderByAsc(self):
        """Ordering by user_id ASC values"""
        cur = self.conn.cursor()
        cur.execute(test_select_order_by_asc)
        results = cur.fetchall()
        self.assertEqual(4, results[0][0])
        self.assertEqual(5, results[1][0])
        self.assertEqual(6, results[2][0])

    def testSelectLimit(self):
        """Limit to 2 rows"""
        cur = self.conn.cursor()
        cur.execute(test_select_limit)
        results = cur.fetchall()
        self.assertEqual(2, len(results))

    def testSelectOffset(self):
        """Offset to skip first row"""
        cur = self.conn.cursor()
        cur.execute(test_select_offset)
        results = cur.fetchall()
        self.assertEqual(2, len(results))
        self.assertEqual(5, results[0][0])
        self.assertEqual(6, results[1][0])

    def testSelectWithIntParam(self):
        cur = self.conn.cursor()
        cur.execute(test_select_with_param, [8])
        results = cur.fetchall()
        self.assertEqual(1, len(results), "exactly one result expected, got %d" % len(results))
        self.assertEqual(5, results[0][0])

    def testSelectWithNamedParam(self):
        cur = self.conn.cursor()
        cur.execute(test_select_with_named_param, {"id":8})
        results = cur.fetchall()
        self.assertEqual(1, len(results), "exactly one result expected, got %d" % len(results))
        self.assertEqual(5, results[0][0])

    def testSelectWithStringParam(self):
        cur = self.conn.cursor()
        cur.execute(test_select_with_string_param, [u'result 3'])
        #print cur.sparql
        results = cur.fetchall()
        self.assertEqual(1, len(results), "exactly one result expected, got %d" % len(results))
        self.assertEqual(6, results[0][0], "first value in first row is 6")

    def testSelectLiteralValue(self):
        cur = self.conn.cursor()
        cur.execute(test_select_literal_value)
        self.assertEqual(1, len(cur.results))
        row = cur.fetchone()
        self.assertEqual(10, row[0])
        self.assertEqual(5, row[1])

    def testSelectOnlyLiteralValues(self):
        cur = self.conn.cursor()
        cur.execute(test_select_only_literals)
        self.assertEqual(1, len(cur.results))
        row = cur.fetchone()
        self.assertEqual(10, row[0])

    def testSelectOnlyLiteralValuesWithNoRowsReturned(self):
        cur = self.conn.cursor()
        cur.execute(test_select_only_literals_with_no_rows_returned)
        self.assertEqual(0, len(cur.results))

    def testSelectWithTableNames(self):
        """Include explicit table names in the select clause"""
        cur = self.conn.cursor()
        cur.execute(test_select_with_table_names)
        results = cur.fetchall()
        self.assertEqual(4, results[0][0])
        self.assertEqual("response 1", results[0][1])

if __name__ == "__main__":
    unittest.main()

