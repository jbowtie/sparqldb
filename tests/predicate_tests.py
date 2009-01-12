#! /usr/bin/env python
import sys, os.path

from sparqldb import dbapi
import unittest,testdb

test_select_col_eq_val = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = 8"
test_select_col_compare_val = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id > 8"
test_select_by_id = "SELECT user_id, freetext_answer as answer FROM survey WHERE id = 3"
test_select_single_in = "SELECT user_id, freetext_answer as answer FROM survey WHERE id IN (3)"
test_select_multi_in = "SELECT user_id, freetext_answer as answer FROM survey WHERE user_id IN (4, 6) ORDER BY user_id"

class predicateSuite(testdb.dbTestCase):
	def testSelectByPrimaryKeyValue(self):
		cur = self.conn.cursor()
		cur.execute(test_select_by_id)
		self.assertEqual(1, len(cur.results))
		row = cur.fetchone()
		self.assertEqual(6, row[0])
		self.assertEqual('response 3', row[1])

	def	testSelectWhereColumnEqValue(self):
		cur = self.conn.cursor()
		cur.execute(test_select_col_eq_val)
		self.assertEqual(1, len(cur.results))
		row = cur.fetchone()
		self.assertEqual((5, u'response 2'), row)

	def	testSelectWhereColumnCompareValue(self):
		cur = self.conn.cursor()
		cur.execute(test_select_col_compare_val)
		print cur.sparql
		self.assertEqual(1, len(cur.results), "exactly one result expected, got %d" % len(cur.results))
		row = cur.fetchone()
		self.assertEqual((6, u'response 3'), row)

	def testSelectSingleUsingInClause(self):
		cur = self.conn.cursor()
		cur.execute(test_select_single_in)
		self.assertEqual(1, len(cur.results))
		row = cur.fetchone()
		self.assertEqual((6, u'response 3'), row)

	def testSelectMultipleUsingInClause(self):
		cur = self.conn.cursor()
		cur.execute(test_select_multi_in)
		row = cur.fetchone()
		self.assertEqual((4, u'response 1'), row)
		row = cur.fetchone()
		self.assertEqual((6, u'response 3'), row)
		# we need to fetchall for accurate count...
		rows = cur.fetchall()
		self.assertEqual(2, len(cur.results))
if __name__ == "__main__":
	unittest.main()

