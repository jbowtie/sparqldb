#!/usr/bin/env python
# vi:si:et:sw=4:sts=4:ts=4

import unittest
from sparqldb import dbapi

test_create_table_syntax = """CREATE TABLE survey (
    id serial NOT NULL PRIMARY KEY,
    user_id integer NOT NULL,
    question_id integer NOT NULL,
    freetext_answer varchar(20) NOT NULL
);
"""
test_insert_syntax = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(1, 4, 9, 'response 1')"
test_insert_syntax2 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(2, 5, 8, 'response 2')"
test_insert_syntax3 = "INSERT INTO survey(id, user_id, question_id, freetext_answer) VALUES(3, 6, 7, 'response 3')"

test_select_all = "SELECT user_id, freetext_answer as answer FROM survey"
test_select_order_by = "SELECT user_id FROM survey ORDER BY question_id" #[6,5,4]
test_select_order_by_desc = "SELECT user_id FROM survey ORDER BY user_id DESC" #[6,5,4]
test_select_order_by_asc = "SELECT user_id FROM survey ORDER BY user_id ASC" #[4,5,6]
test_select_col_eq_val = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = 8"
test_select_col_compare_val = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id > 8"
test_select_by_id = "SELECT user_id, freetext_answer as answer FROM survey WHERE id = 3"
test_select_limit = "SELECT user_id, freetext_answer as answer FROM survey LIMIT 2"
test_select_offset = "SELECT user_id FROM survey ORDER BY user_id ASC OFFSET 1"
test_select_with_param = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = %s"
test_select_with_string_param = "SELECT user_id FROM survey WHERE freetext_answer = %s"
test_select_with_named_param = "SELECT user_id, freetext_answer as answer FROM survey WHERE question_id = %(id)s"
#TODO returned col is also in select cols
#test_select_with_string_param = "SELECT user_id, freetext_answer as answer FROM survey WHERE freetext_answer = %s"

class InsertSuite(unittest.TestCase):
	def setUp(self):
		#create, insert three records
		self.conn = dbapi.connect(uri="http://example.org/testdb/", create=True)

		cur = self.conn.cursor()

		#create a table
		cur.execute(test_create_table_syntax)
	def testLastRowID(self):
		cur = self.conn.cursor()
		cur.execute(test_insert_syntax2)
		self.assertEqual(2, cur.lastrowid)

class dbapiSuite(unittest.TestCase):
	def setUp(self):
		#create, insert three records
		self.conn = dbapi.connect(uri="http://example.org/testdb/", create=True)
		cur = self.conn.cursor()
		#create a table
		cur.execute(test_create_table_syntax)
		#insert 3 records
		#insert record 2 first to show up any ordering issues!
		cur.execute(test_insert_syntax2)
		cur.execute(test_insert_syntax)
		cur.execute(test_insert_syntax3)

	def testDescribeCursor(self):
		cur = self.conn.cursor()
		cur.execute(test_select_by_id)
		self.assertEqual(1, len(cur.results))
        desc = cur.description
		self.assertEqual(2, len(desc), "2 columns described")
		self.assertEqual('user_id', desc[0][0], "first column name = user_id")
		self.assertEqual('answer', desc[1][0], "second column name = answer")

    def testDescribeEmptyCursor(self):
		cur = self.conn.cursor()
        self.assertFalse(cur.description, "empty cursor returns None for description")

	def testExplicitFetchMany(self):
		"""Select all 3 records, but only fetch 2 at a time"""
		cur = self.conn.cursor()
		cur.execute(test_select_order_by_asc)
		results = cur.fetchmany(2)
		self.assertEqual(2, len(results))
		self.assertEqual(4, results[0][0])
		self.assertEqual(5, results[1][0])
		results = cur.fetchmany(2)
		self.assertEqual(1, len(results))
		self.assertEqual(6, results[0][0])
        
if __name__ == '__main__':
	unittest.main()

